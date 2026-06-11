# Personal Health Pulse Skill

A channel-agnostic skill for building personal health tracking and coaching agents.

Personal Health Pulse helps an agent ingest health check-ins from any supported conversation channel, maintain local structured records, and produce warm daily/weekly coaching around fat loss, muscle retention, sleep/recovery, alcohol-risk control, and self-review.

It is intentionally **not** tied to any specific messaging transport. Use it with the channel your agent already supports: an agent chat, webhook, email flow, local CLI, desktop thread, or another adapter.

## What It Provides

- A reusable `personal-health-pulse` skill folder.
- Local-first data schemas for daily records, workouts, body measurements, life notes, message queues, lookup caches, and derived assessments.
- Coaching principles for ADIME, recovery debt, standard drinks, score bands, and damage-control replies.
- A channel adapter contract so host agents can connect their own message transport.
- A light/heavy review workflow for simple questions versus record updates, images, product lookups, scoring, and system changes.
- An event-driven no-token-idle adapter pattern for chat integrations: keep only the listener alive while idle, queue new messages with bounded context, debounce bursts, and retry worker timeouts without waiting for another user message.
- A reminder planning workflow that designs morning, check-in, evening, weekly, and risk-triggered reminders without assuming any specific scheduler.

## Install

For Codex-style skill folders:

```bash
mkdir -p ~/.codex/skills
cp -R personal-health-pulse ~/.codex/skills/
```

Then ask your agent:

```text
Use $personal-health-pulse to design a local health tracking and coaching workflow for my agent channel.
```

For other agents, point the agent at:

```text
personal-health-pulse/SKILL.md
```

and let it load reference files from `personal-health-pulse/references/` as needed.

## Repository Layout

```text
personal-health-pulse/
  SKILL.md
  agents/openai.yaml
  references/
    agent-workflow.md
    channel-adapter.md
    coaching-principles.md
    data-schema.md
    reminder-planning.md
```

## Design Principles

- Channel-agnostic: transport code belongs in an adapter, not in health logic.
- Scheduler-agnostic: reminder intent belongs in the skill; implementation belongs to the host agent or platform.
- Local-first: structured files are the default data store unless the user chooses otherwise.
- Coaching, not diagnosis: this is self-review and behavior support, not medical care.
- Privacy by default: examples use neutral placeholders and do not include real user IDs, private chat IDs, access tokens, or personal data.
- State over hidden memory: persistent rules and long-term facts should be written into docs or data files.

## Safety Note

This skill is for personal tracking and coaching. It is not medical advice. For medical symptoms, eating disorders, severe alcohol dependence, self-harm risk, or other high-stakes situations, agents should encourage professional support and keep guidance conservative.

## License

MIT
