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
{"status":"pending","attempt_count":0,"message_id":"msg_123","event_id":"evt_123","conversation_id":"conv_123","created_at":"2026-06-01T12:00:00","category":"record_update","route":"heavy","content":"Lunch was beef rice and coffee","resources":[],"recent_context":{"messages":[]}}
```

Statuses:

- `pending`: queued and ready.
- `processing`: selected by a worker.
- `processed`: handled successfully.
- `needs_clarification`: agent asked a follow-up.
- `failed`: worker timed out or errored after allowed attempts.

Useful fields:

- `message_id` and `event_id`: stable IDs for deduplication when available.
- `conversation_id`: adapter-specific conversation or channel ID.
- `category`: `simple_qa`, `record_update`, `rich_review`, or `system_request`.
- `route`: worker route such as `light` or `heavy`; implementations may use one
  unified route if consistency matters more than latency.
- `attempt_count`: incremented when a worker marks the item `processing`.
- `processing_started_at`: timestamp used to recover stale work after crashes.
- `failed_at`, `error_type`, `error_message`: failure audit fields.
- `reply_summary`: short summary of the sent reply, useful for later
  `recent_context`.
- `resources`: metadata for images/files; include `local_path` or
  `download_status` when relevant.
- `recent_context`: bounded snapshot, usually same conversation, last 90
  minutes, max 12 summarized messages.

### `data/inbox.jsonl`

Append raw channel messages, sanitized where necessary. Include message ID, timestamp, channel/source, content summary, resources, and any write patches.

### `data/daily_assessments.jsonl`

Derived coaching judgments.

```json
{"date":"2026-06-01","status":"official_closed","score":{"value":82,"confidence":"medium"},"context_risk":"medium","alcohol_standard_drinks":{"value":0,"confidence":"high"},"sleep_debt":"low","alcohol_debt":"low","training_debt":"medium","data_debt":"low","carryover_debt":{"sleep_debt":"low","alcohol_debt":"none"},"readiness_stage":"action","macro_estimate":{"calories":{"low":2100,"high":2400},"protein_g":145,"confidence":"medium"},"expenditure_estimate":{"tdee":2600,"confidence":"low"},"energy_balance_estimate":{"low":-500,"high":-200,"confidence":"low"},"adime_summary":{"Assessment":"...","Diagnosis":"...","Intervention":"...","Monitoring":"..."}}
```

Suggested `status` values:

- `provisional_open`: live score or assessment for an open day.
- `official_closed`: official score after closure context is available.
- `official_closed_revised`: revised official score after late corrections.

Keep derived nutrition estimates, recovery debt, score explanations, and ADIME
fields here. Keep `data/daily.csv` compact and factual.

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
