# Adaptive intake

Start from information already present. For unfamiliar runners a useful first message groups four topics, not a long mandatory questionnaire:

1. Goal race date/distance and priority (finish, performance, participation); other races, travel, unavailable dates and uncertain entries.
2. Available days and time per day, hard limits versus flexibility, preferred long-run/rest days, timezone and preferred units. A weekly-hour total alone cannot show whether a long run fits. Separate running time from changing/commuting/showering where relevant.
3. Last 4–6 weeks: rough completed weekly distances or time, runs/week, longest recent run and its duration/effort, consistency/interruptions, current symptoms or recent injury relevant to running. Record other substantial sport/strength work and recovery constraints when they affect design.
4. Recent races/time trials at several distances if available (mile/5K/10K/HM/marathon): date, distance, time, all-out versus controlled, course/weather and notable pauses/fueling. One result, rough estimates or no race results are acceptable. Do not require age/body mass/HRmax for ordinary effort-based scheduling.

Follow up on consequential ambiguities: finish-time aspiration vs evidence; unknown race date; longest run distance without available time; injury status; whether hard schedule caps include transitions. Do not make every informational gap a blocker.

Minimum for a concrete individualized initial plan: meaningful goal/horizon, day/time constraints, approximate recent load/longest run and current running limitations. If these are absent, ask rather than assigning unsupported volume. If precise paces lack evidence, use explained effort ranges and a conservative provisional starting point without pretending that is individualized physiological validation.

For experienced/connected users reuse confirmed preferences; ask about changes in schedule, goals or symptoms. Missing activities are not rest days. Reconcile overlapping COROS/Strava records before totals. Distinguish user report, device measurement, estimate and coaching inference. Do not infer safe return from injury from race times or a watch score.

For novices, time/run-walk and consistency goals may fit better than kilometres or named intensity systems. For trails/hills, use effort/time and terrain-specific demands rather than road-equivalent pace. No requirement for a race at the final day: season planning can include several priorities, but their tradeoffs must be explicit.

## Lessons from forward tests

Use calendar dates in a dated plan, not just week numbers. When exact dates do not matter, variable-shift runners can receive a movable sequence anchored when shifts are known; clarify constraints before filling weekdays. Ask for timezone before calendar exports and units before distance prescriptions, but do not block an effort/time-only conversation on them. A non-race plan may use an explicit horizon rather than a mandatory race date.

Give ordinary-language effort cues tailored to the runner's experience. 'Controlled quicker' alone was unclear to a synthetic novice. Moderate effort might allow a short sentence; this cue is not a measurement of lactate threshold. Avoid complex watch steps when the runner requests simplicity.

Ask whether race day is an exception to routine time limits. A two-hour Sunday cap does not automatically accommodate a half marathon for a runner whose finish may exceed two hours. Do not let the goal time conceal this conflict.

Interim advice while awaiting material intake should explain the process or preserve an already-established routine; do not assign new volume or intensity when the starting point/limitations are unknown.

## Method preferences

Ask about named-system preferences or previous experience when the choice matters; do not require everyone to pick a philosophy. If a runner names Hudson, Hansons, Pfitzinger or Daniels 2Q, consult [the method reference](training-methods.md) and ask about exact edition/tier only when fidelity matters. A preference does not override feasibility or current fitness. Distinguish a desire for simpler workouts, fewer run days, longer aerobic runs or more flexibility from allegiance to a brand.

## Pre-plan preference questions

After the essential intake, ask a short preference follow-up before choosing a framework. Merge it into the earlier scheduling conversation when natural; reuse known answers and do not repeat resolved time-cap questions. Ask about preferences rather than requiring the runner to name a method. Accept “unsure,” “no preference,” and declining to answer; explain any provisional default. A preference is not a hard constraint unless the runner says it is, and it is not evidence of load tolerance.

Suggested questions:

- How many faster/structured workouts would you enjoy per week: none, one, two, or unsure? Clarify what they mean by workout and separately account for demanding long runs, rather than silently promising two hard workouts plus a hard long run.
- Do you prefer long runs at weekends, on weekdays, or either? Which days suit workouts? Can any weekday accommodate a longer session within the running-time caps already supplied?
- Do you like sustained efforts or repetitions, simple effort cues or precise pace instructions? Do you prefer a fixed weekly rhythm or sessions that move around your schedule?
- Have you liked or disliked any previous approach? “No named-method preference” is enough; ask about edition/tier only when exact adherence is requested.

Record desired workout frequency, preferred long-run/workout days, workout format, scheduling flexibility and any method preference. Check conflicts with actual availability, baseline and recovery before recommending. Do not infer that disliking intervals rules out all Daniels concepts, or that having a weekday window uniquely implies Pfitzinger. Use [fit explanations](training-methods.md#explain-the-fit-from-preferences) to connect preferences to a reasoned recommendation and name alternatives when appropriate.

In the optional Python intake helper, missing preference information appears in `preference_questions` separately from essential `questions`; it does not block provisional planning. Ask only the listed missing parts, not the full template if some parts are known. `preferences: "no_preference"` skips this follow-up entirely. The helper does not select a named plan or establish readiness.
