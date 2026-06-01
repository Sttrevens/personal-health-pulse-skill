---
name: personal-health-pulse
description: Build or operate a channel-agnostic personal health tracking and coaching agent for fat loss, muscle retention, sleep/recovery, alcohol-risk control, reminders, and daily/weekly self-review. Use when the user wants an agent to ingest health check-ins from any supported chat/channel, maintain local structured records, produce warm coaching replies, plan reminders, score days, create weekly reviews, or design a Health Pulse-style workflow without binding to a specific messaging transport.
---

# Personal Health Pulse

Use this skill to help an agent become a personal health "pulse" system: it listens through whatever channel the host agent already supports, records user check-ins into local structured files, and replies with concise nutrition-coaching guidance.

This skill is channel-agnostic. Do not assume any specific chat app, inbox, webhook, or CLI. Treat the channel as an adapter that can receive user messages, send replies, and optionally pass image/file resources.

## Core Workflow

1. Identify the user's goal, constraints, and preferred data store.
2. Create or inspect the Health Pulse data files. Use `references/data-schema.md`.
3. Route each incoming message:
   - simple question: reply directly with recent context;
   - record update: write daily/workout/life data, then reply;
   - rich review: use image, brand, restaurant, scoring, or weekly-review logic;
   - system request: modify the user's Health Pulse project.
4. Apply coaching principles from `references/coaching-principles.md`.
5. Use `references/agent-workflow.md` for state, routing, retry, and review lifecycle.
6. Use `references/reminder-planning.md` when the user wants morning, check-in, evening, weekly, or risk-triggered reminders.
7. Use `references/channel-adapter.md` to map the current agent channel into the workflow.

## Operating Rules

- Keep health records local by default unless the user explicitly asks for a remote store.
- Treat generated advice as coaching and self-review, not medical diagnosis.
- Do not shame the user. Reflect, then offer small next actions.
- Avoid hidden state in conversation memory. Persistent rules, preferences, and long-term facts should be written into project docs/data.
- Prefer structured files over free text when the data will be reused for scoring or summaries.
- Use current tools for channel I/O. If the active environment has a messaging connector, use that connector; otherwise generate the reply for the caller to send.
- Never hard-code user IDs, chat IDs, local usernames, private paths, or personal examples into reusable artifacts.

## Message Handling

For each incoming message, decide whether it needs persistence.

- If it reports food, training, sleep, alcohol, body metrics, mood, urges, or body measurements, write to the appropriate data file.
- If it asks "why", "what should I do", or "is this okay" without new recordable facts, answer using recent context.
- If it contains an image or package/menu/restaurant clue, preserve resource metadata and use available vision/search tools only when needed.
- If it mentions a specific brand, packaged product, restaurant, or named dish, verify against reliable sources when possible and record uncertainty.
- If confidence is low, ask one short clarification question instead of pretending precision.

## Scoring And Reviews

Use scores as behavioral reviews, not moral judgments.

- Do not automatically score a day until the day is closed: late-night food/alcohol and sleep context should be available.
- Manual score requests may produce a provisional score if data is incomplete; label it clearly.
- Weekly reviews should summarize trends, largest recovery debts, training execution, alcohol pattern, food quality, and next-week focus.
- For detailed scoring and coaching patterns, read `references/coaching-principles.md`.

## Reminder Planning

When the user wants reminders, design the reminder intent first. Ask about wake time, training windows, work schedule, sleep target, and high-risk food/alcohol windows. Recommend the smallest useful cadence, then let the active agent/platform decide implementation.

Do not assume the environment supports scheduled jobs. If it does, create reminders through the available adapter. If it does not, produce a portable reminder spec or setup instructions. Read `references/reminder-planning.md` for the full chain.

## Resources

- `references/data-schema.md`: recommended local files, fields, and JSONL records.
- `references/coaching-principles.md`: ADIME, recovery debt, standard drinks, scoring bands, and tone.
- `references/agent-workflow.md`: routing, state lifecycle, light/heavy review, retries, and context windows.
- `references/reminder-planning.md`: channel-agnostic reminder design, personalization, and adapter handoff.
- `references/channel-adapter.md`: how to integrate this workflow with any agent-supported conversation channel.
