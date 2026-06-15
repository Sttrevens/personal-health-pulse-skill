# Lark CLI Adapter Template

This is an adapter example, not core Health Pulse logic. Keep all channel IDs,
user IDs, app credentials, and local paths in environment variables or the host
secret store.

## Environment

```bash
export HEALTH_PULSE_PROJECT_DIR="/path/to/health-pulse-project"
export HEALTH_PULSE_RUNTIME_DIR="$HOME/.health-pulse-runtime"
export HEALTH_PULSE_ALLOWED_USER_ID="ou_placeholder"
export HEALTH_PULSE_ALLOWED_CHAT_ID="oc_placeholder"
export HEALTH_PULSE_SEND_AS="bot"
```

## Listener Shape

```bash
lark-cli event consume im.message.receive_v1 --as "$HEALTH_PULSE_SEND_AS"
```

The adapter should:

- wait for the stream's ready signal,
- keep stdin or the stream handle open if the CLI requires it,
- accept only configured private chats or allowlisted scopes,
- dedupe by both `event_id` and `message_id`,
- append the raw message to `data/inbox.jsonl`,
- preserve image/file metadata and download resources when supported,
- append a pending record to `data/pending_ai_messages.jsonl`,
- include bounded `recent_context`,
- debounce for 2-5 seconds,
- start the review supervisor only when new work was queued.

## Sending Replies

Send Markdown as a real multiline string. Do not send literal escaped `\n`
sequences unless the channel explicitly expects them.

```bash
lark-cli im +messages-send \
  --as "$HEALTH_PULSE_SEND_AS" \
  --user-id "$HEALTH_PULSE_ALLOWED_USER_ID" \
  --markdown "$message"
```

## Boundaries

- The Lark adapter is transport code. It should not contain scoring rules.
- The review worker owns health interpretation and data writes.
- The adapter may send a short fallback if the worker times out, but it should
  not pretend the health review succeeded.
- Never commit real open IDs, chat IDs, app secrets, message logs, or downloaded
  private images to a reusable skill repository.

