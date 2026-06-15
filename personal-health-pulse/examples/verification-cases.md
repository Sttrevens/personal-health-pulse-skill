# Verification Cases

Use these prompts or fixtures to check a Health Pulse implementation after
changing routing, scoring, reminders, or adapter behavior.

## Queue And Adapter

1. No pending messages exist.
   Expected: the supervisor exits without starting a model run.

2. A message arrives with both event ID and message ID already seen.
   Expected: no duplicate pending record is queued.

3. Two quick messages arrive within the debounce window.
   Expected: both are processed in one review batch.

4. A new message arrives while the worker is preparing a reply.
   Expected: the worker merges the late pending message before sending, then
   sends one combined reply.

5. A worker times out.
   Expected: active records become `failed`, a short fallback is sent if the
   channel supports replies, retryable records are requeued immediately, and the
   retry limit prevents an infinite loop.

## Scoring

1. Scheduled morning runs before yesterday's late food/alcohol/sleep context is
   known.
   Expected: no invented official score; show stored official score if present
   or say closure is pending.

2. User reports lunch and a planned training session during an open day.
   Expected: give a clearly provisional live score or range; do not require
   dinner, final steps, no-alcohol confirmation, or tonight's sleep first.

3. Yesterday's drinking and short sleep were already counted in yesterday's
   official score. Today the user reports hydration, protein, and adjusted
   training.
   Expected: mention carryover readiness debt, but score today's response rather
   than deducting yesterday's drinks again.

4. A closed-day review includes restaurant food and an unmeasured drink.
   Expected: nutrition and energy estimates use ranges and confidence labels.

5. User asks an unrelated tool or safety question with no health-record intent.
   Expected: answer directly without a forced score or data write.

## Coaching

1. User says they want to drink after a stressful event.
   Expected: reflect the urge, preserve choice, and offer 2-3 small damage
   control options.

2. User reports overeating or alcohol the night before.
   Expected: no punishment fasting; use water/electrolytes, protein,
   vegetables/fiber, moderate carbohydrates, no alcohol, and normal sleep target.

3. User names a brand, packaged product, restaurant, or menu dish.
   Expected: verify against reliable matching sources when possible; mark
   uncertainty instead of guessing across same-name items.

