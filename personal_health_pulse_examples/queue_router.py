"""Minimal JSONL queue router for event-driven Health Pulse adapters.

This example intentionally knows nothing about any chat provider. An adapter can
append records to ``pending_ai_messages.jsonl``; a worker can use these helpers
to select work, recover stale attempts, and merge late-arriving messages before
sending a final reply.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


PENDING_STATUSES = {"pending"}
HEAVY_CATEGORIES = {"record_update", "rich_review", "system_request"}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def now_text() -> str:
    return utc_now().isoformat()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(record, ensure_ascii=False) for record in records)
    path.write_text((text + "\n") if text else "", encoding="utf-8")


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def pending_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in records if record.get("status") in PENDING_STATUSES]


def classify_message(record: dict[str, Any]) -> str:
    category = record.get("category")
    if category in {"simple_qa", "record_update", "rich_review", "system_request"}:
        return str(category)

    if record.get("resources"):
        return "rich_review"

    content = str(record.get("content") or "").lower()
    record_terms = ("food", "meal", "training", "workout", "sleep", "alcohol", "weight", "waist")
    question_terms = ("why", "how", "should i", "can i", "is it okay")
    if any(term in content for term in record_terms):
        return "record_update"
    if any(term in content for term in question_terms):
        return "simple_qa"
    return "record_update"


def choose_route(records: list[dict[str, Any]]) -> str:
    categories = {classify_message(record) for record in pending_records(records)}
    if not categories:
        return "none"
    if categories & HEAVY_CATEGORIES:
        return "heavy"
    return "light"


def mark_processing(path: Path, route: str) -> int:
    records = read_jsonl(path)
    selected = 0
    timestamp = now_text()

    for record in records:
        if record.get("status") != "pending":
            continue
        record["status"] = "processing"
        record["route"] = route
        record["processing_started_at"] = timestamp
        record["attempt_count"] = int(record.get("attempt_count") or 0) + 1
        selected += 1

    if selected:
        write_jsonl(path, records)
    return selected


def merge_pending_into_processing(path: Path, route: str) -> int:
    records = read_jsonl(path)
    merged = 0
    timestamp = now_text()

    for record in records:
        if record.get("status") != "pending":
            continue
        record["status"] = "processing"
        record["route"] = route
        record["processing_started_at"] = timestamp
        record["attempt_count"] = int(record.get("attempt_count") or 0) + 1
        record["merged_into_active_review_at"] = timestamp
        merged += 1

    if merged:
        write_jsonl(path, records)
    return merged


def recover_stale_processing(path: Path, *, stale_minutes: int = 30) -> int:
    records = read_jsonl(path)
    cutoff = utc_now() - timedelta(minutes=stale_minutes)
    recovered = 0

    for record in records:
        if record.get("status") != "processing":
            continue
        started_at = parse_datetime(record.get("processing_started_at"))
        if started_at is None or started_at <= cutoff:
            record["status"] = "pending"
            record["recovered_at"] = now_text()
            record.pop("processing_started_at", None)
            recovered += 1

    if recovered:
        write_jsonl(path, records)
    return recovered


def requeue_failed(path: Path, *, max_attempts: int = 2) -> int:
    records = read_jsonl(path)
    requeued = 0

    for record in records:
        if record.get("status") != "failed":
            continue
        attempt_count = int(record.get("attempt_count") or 0)
        if attempt_count < max_attempts:
            record["status"] = "pending"
            record["requeued_at"] = now_text()
            requeued += 1

    if requeued:
        write_jsonl(path, records)
    return requeued
