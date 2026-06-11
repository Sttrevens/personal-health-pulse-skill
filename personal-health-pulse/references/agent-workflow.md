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
- If a timeout or worker error creates a retryable `failed` record, requeue it immediately in the same supervisor run when possible. Do not wait for another user message to accidentally trigger recovery.
- After the attempt limit, keep `failed` for manual inspection.
- Send a short fallback reply on timeout/error if the channel supports it.

## Event-Driven No-Token Idle

For chat or messaging channels, prefer an event-driven adapter over periodic polling when the platform supports it.

Idle behavior:

- Keep only the low-cost channel listener or webhook process alive.
- Do not start the review worker, scan chat history, read project context, or call a model when no new message exists.
- Do not send a template acknowledgement unless the user explicitly wants one; wait for the real coaching reply.

On a new message event:

1. Filter to the configured conversation, user, or allowed scope in the adapter.
2. Deduplicate by both event ID and message ID when both are available.
3. Store the raw message in the inbox log.
4. Download or preserve resource metadata for images/files.
5. Add a pending queue record with a bounded recent-context snapshot.
6. Debounce briefly, usually 2-5 seconds, so a burst of quick messages or message plus images can be handled together.
7. Start the review supervisor only if at least one new message was queued.

Worker behavior:

- Use a lock so only one review worker runs at a time.
- If a worker is already running, leave new messages queued; the current worker or the next supervisor run should drain them.
- A single worker run should process all selected pending messages that belong to its route, not just the first one, unless the host model/tooling requires smaller batches.
- If the route is unified into one heavier path for consistency, explicitly set latency-related options such as model size, reasoning effort, or timeout. Do not accidentally inherit a desktop-wide maximum-effort setting for routine food questions.
- On timeout/error, mark active records `failed`, send a short fallback if supported, immediately requeue retryable failures, and rerun within the attempt limit.
- When the attempt limit is reached, leave the record `failed` with an error summary for manual recovery.

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
