# macOS launchd Adapter Template

Use this when the host environment supports local background jobs and the user
wants Health Pulse reminders or an event listener on macOS.

This is scheduler glue. Keep it outside the reusable coaching logic.

## Recommended Jobs

```text
com.example.healthpulse.listener   KeepAlive=true   event listener
com.example.healthpulse.morning    08:30            morning renderer
com.example.healthpulse.fitcheck   16:30            afternoon fit check
com.example.healthpulse.evening    22:30            evening closure
com.example.healthpulse.weekly     Sunday 20:30     just-finished week review
```

Adjust times to the user's actual wake, training, dinner, and sleep windows.

## Runtime Directory

For macOS privacy and background execution, it is often cleaner to run from a
runtime directory outside synced document folders:

```bash
export HEALTH_PULSE_PROJECT_DIR="/path/to/editable/project"
export HEALTH_PULSE_RUNTIME_DIR="$HOME/.health-pulse-runtime"
```

The installer can copy scripts into the runtime directory while the user keeps
editing records in the project directory.

## Listener Job Rules

- Use `KeepAlive=true` for the event listener.
- Do not install a polling ingest job next to an event listener unless the user
  explicitly wants backfill behavior.
- Listener idle behavior should be cheap: no model call, no chat history scan,
  no project context read.
- If a worker is already running, keep new messages queued and let the active or
  next run drain them.

## Reminder Job Rules

- Morning reminders should not force a score for an unclosed yesterday.
- Weekly reviews should summarize the just-finished week, not the still-open
  current day.
- Use environment variables for channel identity and target recipient.
- Log stdout and stderr separately, and keep logs out of reusable examples.

