# Channel Adapter

This skill does not prescribe a transport. Use whatever channel the active agent platform already supports.

## Adapter Contract

Map the platform's channel into these capabilities:

- Receive messages with stable IDs, timestamps, conversation IDs, text, and optional resources.
- Send Markdown or plain-text replies.
- Fetch/download image or file resources when available.
- Deduplicate by message ID.
- Preserve enough recent context for coherent replies.

If the platform cannot send replies directly, generate the reply text and clearly tell the caller it should be sent through their channel.

## Examples

Use the same workflow whether the channel is:

- a Clawbot-style agent chat,
- a desktop Codex thread,
- a webhook-backed messaging channel,
- an email or form ingestion flow,
- a local CLI that appends messages to JSONL.

The channel name should not appear in reusable health logic. Keep transport code in an adapter layer.

## Event-Driven Adapter Pattern

When the platform offers message events, webhooks, or a streaming consumer, use that as the primary ingest path instead of scanning recent chat history on a timer.

Adapter responsibilities:

- Maintain the listener, webhook receiver, or stream consumer.
- Wait for an explicit ready signal when the platform provides one.
- Keep any required stream input or connection handle open so the consumer does not exit from end-of-file.
- Filter events before queueing them, using configured conversation IDs, user IDs, or allowlists supplied by the host environment.
- Deduplicate with stable event and message IDs.
- Store raw messages in an inbox log, then queue new messages with resource
  metadata and a bounded recent-context snapshot.
- Trigger the review supervisor only after new work was actually added.
- Use a short fixed debounce window, usually 2-5 seconds, to batch rapid user messages and related resources without adding noticeable delay.
- If the review worker is already running, do not start another one; leave the message queued.

No-token idle rule:

- No new message means no review worker.
- No review worker means no model call, no history scan, and no project-context read.
- The only idle cost should be the channel listener or webhook process itself.

Failure handling:

- Treat listener startup failure as adapter failure and let the host supervisor restart it.
- Treat message review timeout as worker failure, not channel failure.
- After a worker timeout, send a short "received but processing is slow" fallback only if the channel supports it.
- Requeue retryable failures immediately within the same supervisor chain so one timed-out message does not wait for a future user message.

Before sending the final reply, the review worker should ask the queue whether
new pending messages arrived during the review. If so, merge them into the
active processing batch and generate one combined response.

## Resource Handling

For images or files:

- Store resource metadata in the queued message.
- If the platform provides local paths, use them.
- If downloads fail, mark the failure as a receive/download problem and continue with text.
- Ask the user for a short description only when visual inspection is impossible or uncertain.

## Privacy

Do not hard-code:

- user IDs,
- conversation IDs,
- access tokens,
- local usernames,
- private paths,
- personal names.

Use environment variables, host-agent secrets, or platform configuration for channel credentials.
