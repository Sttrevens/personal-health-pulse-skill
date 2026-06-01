# Reminder Planning

Use this reference when the user wants Health Pulse reminders, scheduled check-ins, recurring nudges, or proactive weekly reviews.

The goal is to design reminder intent, not to assume a scheduler. Let the active agent or host platform decide whether to create automations, calendar events, local jobs, scheduled messages, or manual setup instructions.

## Planning Questions

Ask only what is needed. Good first-pass questions:

- When do you usually wake up?
- When do you usually train, or when could training realistically happen?
- When do you want to be asleep?
- Which window is highest risk for alcohol, overeating, or skipping records?
- Do you prefer fewer reminders or more structure?

If the user is unsure, start conservative and adjust after a week.

## Default Reminder Intents

Use 2-3 daily reminders plus one weekly review at most.

```json
[
  {
    "id": "morning_checkin",
    "cadence": "daily",
    "local_time": "08:30",
    "purpose": "Record weight, sleep, and today's training intent.",
    "message_type": "morning"
  },
  {
    "id": "afternoon_fit_check",
    "cadence": "daily",
    "local_time": "16:30",
    "purpose": "Check protein, training status, dinner plan, and alcohol risk.",
    "message_type": "fit_check"
  },
  {
    "id": "evening_closure",
    "cadence": "daily",
    "local_time": "22:30",
    "purpose": "Close the day: food, alcohol, training, steps, and sleep setup.",
    "message_type": "evening"
  },
  {
    "id": "weekly_review",
    "cadence": "weekly",
    "local_time": "20:30",
    "weekday": "Sunday",
    "purpose": "Review trends, recovery debt, training consistency, and next-week focus.",
    "message_type": "weekly"
  }
]
```

## Personalization Rules

- Morning should happen after the user can weigh in, not before.
- Afternoon check-in should happen before dinner decisions become locked.
- Evening closure should happen early enough to influence sleep, not after the user is already in bed.
- Weekly review should wait until the final weekend sleep/alcohol context is available.
- If reminders feel noisy, drop evening first for consistent users and keep morning plus weekly.
- If alcohol is the main risk, keep afternoon or pre-event reminders.
- If data completeness is the main risk, keep morning and evening.
- If training consistency is the main risk, add a training-window reminder only on planned training days.

## Risk-Triggered Reminders

Risk-triggered reminders should be derived from recent records, not hard-coded assumptions.

Useful triggers:

- two days without training,
- two nights under the sleep target,
- consecutive drinking days,
- missing weight or food records for two days,
- a planned high-risk dinner or event,
- the user explicitly says they want to drink, binge, skip training, or cannot sleep.

For each trigger, send one small intervention, not a lecture.

## Adapter Handoff

After planning, inspect what the host agent can actually do.

Priority order:

1. If the agent has a native automation/reminder tool, create reminders there.
2. If the channel supports scheduled messages, create scheduled messages there.
3. If the environment supports local schedulers, generate local job configuration.
4. If calendar integration exists, create calendar reminders.
5. If none are available, produce a portable reminder spec and manual setup instructions.

Keep implementation-specific details outside reusable health logic. Store the chosen reminder spec in project docs or data so future agent runs can understand the intended schedule.

## Anti-Patterns

- Do not create six daily reminders by default.
- Do not schedule a score before the day is closed.
- Do not make alcohol-risk reminders shame-based.
- Do not assume one timezone if the user's channel or host platform provides another.
- Do not hard-code platform names, user IDs, or channel IDs into reusable reminder logic.
