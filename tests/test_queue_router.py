import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from personal_health_pulse_examples import queue_router


class QueueRouterTest(unittest.TestCase):
    def write_records(self, records):
        path = Path(self.tmp.name) / "pending_ai_messages.jsonl"
        path.write_text(
            "\n".join(json.dumps(record) for record in records) + "\n",
            encoding="utf-8",
        )
        return path

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_marks_all_pending_records_processing_for_route(self):
        path = self.write_records(
            [
                {"message_id": "m1", "status": "pending", "category": "simple_qa"},
                {"message_id": "m2", "status": "pending", "category": "record_update"},
                {"message_id": "m3", "status": "processed", "category": "record_update"},
            ]
        )

        selected = queue_router.mark_processing(path, route="heavy")

        self.assertEqual(selected, 2)
        records = queue_router.read_jsonl(path)
        self.assertEqual([record["status"] for record in records], ["processing", "processing", "processed"])
        self.assertEqual(records[0]["route"], "heavy")
        self.assertEqual(records[1]["attempt_count"], 1)

    def test_recovers_stale_processing_and_requeues_retryable_failed(self):
        stale_time = (datetime.now(timezone.utc) - timedelta(minutes=45)).isoformat()
        path = self.write_records(
            [
                {"message_id": "m1", "status": "processing", "processing_started_at": stale_time},
                {"message_id": "m2", "status": "failed", "attempt_count": 1},
                {"message_id": "m3", "status": "failed", "attempt_count": 2},
            ]
        )

        recovered = queue_router.recover_stale_processing(path, stale_minutes=30)
        requeued = queue_router.requeue_failed(path, max_attempts=2)

        self.assertEqual(recovered, 1)
        self.assertEqual(requeued, 1)
        records = queue_router.read_jsonl(path)
        self.assertEqual([record["status"] for record in records], ["pending", "pending", "failed"])

    def test_merge_pending_into_processing_promotes_late_messages(self):
        path = self.write_records(
            [
                {"message_id": "m1", "status": "processing", "route": "heavy"},
                {"message_id": "m2", "status": "pending", "category": "record_update"},
            ]
        )

        merged = queue_router.merge_pending_into_processing(path, route="heavy")

        self.assertEqual(merged, 1)
        records = queue_router.read_jsonl(path)
        self.assertEqual(records[1]["status"], "processing")
        self.assertEqual(records[1]["route"], "heavy")


if __name__ == "__main__":
    unittest.main()
