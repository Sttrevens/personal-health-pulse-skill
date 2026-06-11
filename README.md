# Personal Health Pulse Skill

A local-first health pulse for personal agents: record daily check-ins, preserve
structured health context, and reply with warm coaching instead of shame.

Personal Health Pulse helps an agent ingest health check-ins from any supported conversation channel, maintain local structured records, and produce warm daily/weekly coaching around fat loss, muscle retention, sleep/recovery, alcohol-risk control, and self-review.

It is intentionally **not** tied to any specific messaging transport. Use it with the channel your agent already supports: an agent chat, webhook, email flow, local CLI, desktop thread, or another adapter.

## 10-Second Proof

Give the skill a food, training, sleep, alcohol, mood, or body-metric check-in.
It decides whether the message should be persisted, writes or updates local
records, and returns a short coaching reply.

The default local project shape is:

```text
data/
├── daily.csv
├── workouts.csv
├── body_measurements.csv
├── life_notes.md
├── pending_ai_messages.jsonl
├── daily_assessments.jsonl
└── food_references.jsonl
```

The visible artifact is not a dashboard. It is a durable personal health memory:
daily logs, weekly reviews, recovery-debt notes, reminder intents, and replies
that future agent sessions can continue from.

## Why Install It

One-off health advice is easy. A useful personal health agent needs continuity:
what the user ate, how they slept, whether training happened, where alcohol or
late-night food risk appears, and what tone keeps them moving without guilt.
This skill turns those recurring check-ins into local structured state.

## What It Provides

- A reusable `personal-health-pulse` skill folder.
- Local-first data schemas for daily records, workouts, body measurements, life notes, message queues, lookup caches, and derived assessments.
- Coaching principles for ADIME, recovery debt, standard drinks, score bands, and damage-control replies.
- A channel adapter contract so host agents can connect their own message transport.
- A light/heavy review workflow for simple questions versus record updates, images, product lookups, scoring, and system changes.
- A reminder planning workflow that designs morning, check-in, evening, weekly, and risk-triggered reminders without assuming any specific scheduler.

## Minimum Run

```text
Use personal-health-pulse to set up a local health pulse project for me.

Goal: fat loss while keeping training performance.
Main risks: late-night food, poor sleep, and alcohol on social nights.
Preferred channel: [chat / webhook / CLI / current agent thread].
```

For an existing project:

```text
Use personal-health-pulse to record this check-in:
Lunch was beef rice, coffee, and a protein yogurt. Slept 6h. Training planned
tonight but energy is low.
```

## Safety Boundary

This skill is for coaching and self-review, not diagnosis or treatment. It
should keep records local by default, avoid hard-coded user/channel IDs, avoid
shaming language, and encourage professional support for medical symptoms,
eating disorders, severe alcohol dependence, self-harm risk, or other
high-stakes situations.

## Verification Assets

- [`personal-health-pulse/examples/test-prompts.md`](personal-health-pulse/examples/test-prompts.md)
  covers project setup, daily check-ins, low-confidence food lookup, reminder
  planning, and high-stakes safety boundaries.

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
  examples/test-prompts.md
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
