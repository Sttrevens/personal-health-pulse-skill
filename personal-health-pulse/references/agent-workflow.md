# Agent Workflow

Use this workflow when building or operating a Health Pulse agent behind any chat/channel.

## Roles

- Channel adapter: receives user messages and sends replies through the host agent's existing channel.
- Ingest layer: deduplicates messages, stores raw records, extracts resources, and queues work.
- Review worker: reads queued messages and local context, writes health records, and produces replies.
- Renderer: generates scheduled morning, check-in, evening, score, and weekly summaries.
- Reminder planner: turns the user's real schedule and risk windows into scheduler-agnostic reminder intents.

## Routing

Classify each queued message:

- `simple_qa`: ordinary question, low risk, no data write, no image, no product lookup.
- `record_update`: food, training, sleep, alcohol, body data, daily behavior, or mood report.
- `rich_review`: image, menu/package/product, brand/restaurant lookup, formal score, weekly review, nuanced coaching.
- `system_request`: request to modify the Health Pulse project.

Use a light path for `simple_qa`; use a heavier path for all other categories.

If the light path discovers it needs a data write, image interpretation, lookup, scoring, or project edit, move the item back to `pending` with a heavy route and do not send a premature answer.

## State Lifecycle

Use a queue such as `data/pending_ai_messages.jsonl`.

```text
pending -> processing -> processed
pending -> processing -> needs_clarification
pending -> processing -> failed
failed -> pending, while attempt_count is below the retry limit
processing -> pending, if stale after a timeout window
```

Rules:

- Increment `attempt_count` when a worker marks a message `processing`.
- Recover stale `processing` records before selecting new work.
- Requeue `failed` records only while under an attempt limit, usually 2.
- After the attempt limit, keep `failed` for manual inspection.
- Send a short fallback reply on timeout/error if the channel supports it.

## Recent Context

For event-driven channels, each queued record should carry a bounded context snapshot:

- same conversation/channel when possible,
- last 90 minutes by default,
- max 12 prior messages,
- content summaries, resource summaries, processed status, and reply summaries,
- no full image blobs,
- no full project history.

This keeps replies coherent without forcing the agent to scan history while idle.

## Scheduled Messages

Common renderers:

- morning: yesterday/recent status and today's focus; do not force a score if yesterday is not closed.
- fit-check: afternoon prompt for missing weight/training/protein/waist/alcohol risk.
- evening: record template and closure checklist.
- score-yesterday: manual or post-closure score, provisional if incomplete.
- weekly: trends, ADIME summary, largest recovery debt, next-week targets.

For reminder design, use `reminder-planning.md`. Keep reminder intent separate from platform implementation.

## Verification

When modifying an implementation:

- Add tests before behavior changes where possible.
- Test routing, stale recovery, failed retry, scoring timing, and weekly summaries.
- Verify JSONL remains parseable and CSV headers remain stable.
- Render at least one sample morning/check-in/weekly message.
