# Progressive intake for runners

## Interaction contract

Start with a consumer questionnaire, not a request to write an autobiography. Show **one or two short questions per reply**, with lettered options or native multiple-choice controls when available. Tell the runner they can reply `1B, 2A`, use their own words, or choose not sure/skip. Do not display the entire question bank or internal completeness audit.

Reuse material facts from the conversation. If a runner volunteers several answers at once, accept them without making them repeat selections. For an unfamiliar runner, open with goal and priority; for a known runner skip directly to the next unresolved decision.

After a reply, acknowledge one useful fact briefly (“Got it—three days and simple effort cues”), then advance. Use plain progress labels such as **Goal → Current running → Your week → Preferences → Plan preview**. Do not promise an exact number of rounds because branches vary. Do not interpret a missing answer as a choice.

## First-round example

**1. What are you working toward?**
A. 5K/10K · B. Half marathon · C. Marathon · D. Fitness/consistency · E. Something else · F. Not sure

**2. What matters most?**
A. Finish feeling good · B. Improve a time · C. Build a habit · D. Help me decide

“Reply `1B, 2A`, or use your own words.” Stop and wait. Do not append the next round in the same message.

## Question design

- Ask one concept per question. Do not bundle dates, paces, injury history and commitments into one paragraph.
- Offer meaningful nonoverlapping ranges, simple day pickers, none/not sure and a free-text escape. Asking for exact race dates or result times is appropriate only after the user says those exist.
- Ask in the runner's units before distance bands. Support minutes/run-walk when distance is unknown. A distance band is approximate evidence, not permission to prescribe its midpoint.
- Separate preference, current behavior and hard availability. “I want two workouts” is not the same as having done two or being ready for them.
- Do not require a watch, a new maximal test, age, body mass, HRmax or a branded-plan choice to unlock ordinary effort-based guidance.
- Skip irrelevant branches. No results means no result-detail questions. No other sport means no other-sport essay. No weekday availability means no weekday-cap questions.
- Accept “not sure” or “skip” and move on; flag material uncertainty for review instead of trapping the runner in a repeated question. Do not convert a declined injury question into “no injury.”

## Adaptive question bank

The [survey helper](../scripts/survey.py) supplies these as one/two-question rounds; an agent can conduct the same conversation without running code. It is not necessary to ask every item if answers are known or a decision does not depend on them.

| Topic | Easy answers | Follow-up only when useful |
|---|---|---|
| Goal and priority | Race type/fitness; finish/time/consistency/unsure | Goal detail if “something else” matters |
| Time span | Under 8 / 8–12 / 13–18 / 19+ weeks / no date | Exact booked date before a dated plan; approximate goal supports a rough outline |
| Recent frequency | Not running / 1–2 / 3–4 / 5+ days / varies | Clarify actual frequency only if prescribing needs it |
| Weekly volume | Distance bands in km/mi, or time bands | Ask a narrower typical recent week if a broad band changes the initial dose |
| Longest comfortable run | Under 30 / 30–59 / 60–89 / 90–119 / 120+ minutes / unsure | Confirm effort and recovery when it affects progression |
| Current limitations | None / yes / returning-unsure / discuss later | Brief relevant description, not a diagnosis or compulsory medical essay |
| Weight training | None / less than weekly / 1–2 / 3–4 / 5+ days / unsure | Leg-heavy sessions and timing if they affect recovery |
| Other exercise | None / mostly gentle / demanding / varies | Sport and frequency only for substantial relevant load |
| Available days | Mon–Sun multiselect, or changing days | Shift-based sequence if fixed weekdays do not work |
| Time caps | 20 / 30 / 45 / 60 / more / varies | Running-only versus door-to-door; actual remaining running time if needed; different caps by day |
| Long-run timing | Weekend / weekday / either / no preference | Actual day/window if the preference conflicts with availability |
| Long-day cap | 45 / 60 / 90 / 120 / more / unsure minutes | Exact usable cap for a dated detailed plan; race-day exception when relevant |
| Conflicts | None / travel-dates-races / changing schedule / unsure | Short date list, event priority and race recovery when relevant |
| Faster-workout preference | None / one / two / help me decide | Count a demanding long run in total load, not as invisible extra quality |
| Workout timing/style | Weekday/weekend/either; effort/continuous/reps/mix/choose | Detailed pace targets or fixed rhythm only if desired |
| Recent results | Several / one / none / use effort | Distance + time + approximate date, then representative/controlled/compromised/unsure |

Method familiarity is optional and should not become another mandatory survey. Ask only when the runner expresses interest; otherwise explain a suitable concept after reviewing answers. Use [preference-fit explanations](training-methods.md#explain-the-fit-from-preferences) without claiming a name proves suitability.

## Turn answers into progress, not an endless survey

As soon as core goal/history/schedule/limitations are sufficiently known for a rough outline, offer a preview rather than exhausting optional questions. The default helper stops at this checkpoint; use `--continue-survey` only when the runner wants more preference questions. The outline is general/provisional, not permission to skip important checks before exact workouts. After the relevant rounds, show a brief summary of known goals, recent training bands, time constraints, other exercise and preferences. Separate unresolved points from known facts. Offer a provisional phase outline and say which **one or two** missing details matter before assigning precise sessions. It is fine to show a generic architecture earlier when enough is known; no unsupported personal mileage, pace or recovery claim.

Minimum for concrete initial doses: meaningful goal/horizon, usable day/time constraints, approximate recent completed load/longest run and relevant running limitations. Broad bands may justify a provisional range or a targeted clarification—not a false exact baseline. Incomplete history or declined limitations can require a more general outline rather than a supposedly individualized plan. Do not hold all useful discussion hostage to optional race evidence, method preferences or wearable data.

Examples of targeted follow-ups:

- “You chose 20–under 40 km. Which is closer to your usual completed week: A. 20–25, B. 26–30, C. 31–under 40, D. Unsure?”
- “Is that 45 minutes A. Running only, B. Everything door to door?”
- “Do your longer runs leave you A. Normal next day, B. Heavy legs but ordinary walking is fine, C. Pain/limping or unusually wiped out, D. Unsure?”

A fitness goal with no date can use an agreed block length. A named race needs its actual date before committing a calendar. Race result context helps compare evidence without invented weather/fatigue corrections. A time ambition is not current fitness evidence.

## Script and state

`python3 scripts/intake.py athlete.json` now returns **only the next one/two choice-based questions**, a running summary, unresolved items and the profile state. Record answers with `--answer QUESTION_ID=LETTER` (repeat for multiple answers); `--save local-data/intake.json` explicitly persists state. Nothing is written by default. Day selections use comma-separated letters. Short free-text answers are accepted; event dates use YYYY-MM-DD or a skip/not-booked option.

Common short replies such as “not running,” “no results,” and “not sure” are normalized for branching. Other free-text replies remain self-reports for the agent to interpret; the helper does not provide general natural-language understanding. The profile's `survey_answers` preserves selected labels/values and unknowns. It does not fabricate an exact weekly distance, automatically choose a method, or certify readiness. `intake_summary` means review the summary, not cleared for training. Existing profile facts are reused when their corresponding structured fields are present; the agent still needs to understand conversation context and any free-text ambiguity.

`--audit` retains the older internal field-completeness view for developers. Its compound `questions` and `preference_questions` are diagnostics, **not runner-facing prompts**. Do not paste them into a chat. `preferences: "no_preference"` suppresses optional preference follow-ups; essential day/time feasibility still matters.
