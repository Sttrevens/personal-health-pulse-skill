# Health Pulse Data Schema

Use local plain-text data by default. CSV is good for daily rows and workouts; JSONL is good for message queues, derived assessments, and lookup caches; Markdown is good for long-form notes.

## Required Files

### `data/daily.csv`

One row per day.

```csv
date,weight_kg,sleep_hours,steps,calories,protein_g,trained,training_focus,mood,notes
2026-06-01,79.8,7.2,9000,2100,150,yes,upper,good,"breakfast; lunch; no alcohol"
```

Rules:

- Use ISO dates.
- Leave unknown values blank instead of inventing them.
- Put compact narrative food/alcohol/sleep context in `notes`.
- Avoid stuffing derived coaching fields into this file.

### `data/workouts.csv`

One row per exercise or session component.

```csv
date,session,exercise,sets,reps,weight_kg,rpe,notes
2026-06-01,upper,bench press,4,6,70,8,last set hard
```

### `data/body_measurements.csv`

One row per measurement session.

```csv
date,waist_cm,hip_cm,chest_cm,arm_cm,thigh_cm,photo_note,notes
2026-06-01,87.5,,,,,front/side photos,morning fasted
```

### `data/life_notes.md`

Use dated sections for emotional context, relationship stress, alcohol urges, sleep anxiety, or patterns that should inform coaching.

```markdown
## 2026-06-01

- Mood: felt rejected and wanted a quick relief ritual.
- Alcohol urge: wanted to use alcohol to fall asleep.
```

## Optional JSONL Files

### `data/pending_ai_messages.jsonl`

Queue for channel messages that need agent handling.

```json
{"status":"pending","attempt_count":0,"message_id":"msg_123","created_at":"2026-06-01T12:00:00","content":"Lunch was beef rice and coffee","resources":[],"recent_context":{"messages":[]}}
```

Statuses:

- `pending`: queued and ready.
- `processing`: selected by a worker.
- `processed`: handled successfully.
- `needs_clarification`: agent asked a follow-up.
- `failed`: worker timed out or errored after allowed attempts.

### `data/inbox.jsonl`

Append raw channel messages, sanitized where necessary. Include message ID, timestamp, channel/source, content summary, resources, and any write patches.

### `data/daily_assessments.jsonl`

Derived coaching judgments.

```json
{"date":"2026-06-01","context_risk":"medium","alcohol_standard_drinks":{"value":0,"confidence":"high"},"sleep_debt":"low","alcohol_debt":"low","training_debt":"medium","data_debt":"low","readiness_stage":"action","adime_summary":{"Assessment":"...","Diagnosis":"...","Intervention":"...","Monitoring":"..."}}
```

### `data/food_references.jsonl`

Cache brand/product/restaurant lookup results.

```json
{"query":"example protein latte","type":"product","matched_name":"Example Protein Latte","confidence":"exact","sources":["https://example.com"],"nutrition":{"protein_g":20},"ingredients":[],"notes":"official menu","created_at":"2026-06-01T12:00:00"}
```

Confidence values:

- `exact`: source clearly matches.
- `likely`: source probably matches but minor uncertainty remains.
- `unknown`: same-name ambiguity or no reliable source.

## Privacy

Do not include real user IDs, private chat IDs, personal addresses, or private names in reusable examples. Use neutral placeholders and sanitize logs before sharing.
