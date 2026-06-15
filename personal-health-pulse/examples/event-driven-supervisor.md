# Event-Driven Supervisor Example

This example shows how to wire a channel adapter to Health Pulse without paying
model cost while idle.

## Shape

```text
channel event/webhook/stream
  -> adapter filter and dedupe
  -> data/inbox.jsonl
  -> data/pending_ai_messages.jsonl
  -> short debounce
  -> review supervisor
  -> review worker
  -> channel reply
```

## Idle Rule

When there is no new message, keep only the channel listener alive.

Do not:

- scan recent chat history,
- read the Health Pulse project context,
- start a model run,
- send a placeholder response.

## Supervisor Steps

1. Recover stale `processing` records whose `processing_started_at` is older
   than the configured stale window.
2. Requeue `failed` records while `attempt_count` is below the retry limit.
3. Count `pending` records. Exit immediately if there are none.
4. Acquire a lock so only one review worker runs.
5. Choose a route from pending records, or use one unified route if your worker
   prompt handles all categories consistently.
6. Mark selected records `processing` and increment `attempt_count`.
7. Start the review worker with an explicit timeout and latency setting.
8. On timeout/error, mark processing records `failed`, send a short fallback if
   supported, then immediately requeue and retry while under the attempt limit.
9. Before the worker sends a final reply, merge any late `pending` records into
   the active `processing` batch and reread the queue.
10. Mark handled records `processed` or `needs_clarification`, including
    `processed_at` and `reply_summary`.

## Minimal Router

See the runnable Python example at:

```text
personal_health_pulse_examples/queue_router.py
```

That module is intentionally provider-neutral. It can be used behind a webhook,
chat event stream, local CLI, email parser, or any adapter that appends JSONL
records.

