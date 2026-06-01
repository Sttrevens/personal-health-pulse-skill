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
