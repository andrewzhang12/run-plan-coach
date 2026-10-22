# Validation interface and limits

Python 3 standard library only. Run `python3 scripts/intake.py athlete.json`, `python3 scripts/validate_plan.py plan.json`, or `python3 -m unittest discover -s scripts -v` from the skill folder. Paths are relative to the installed/package folder, never an author's personal workspace.

Plan CLI exit codes: 0 structurally consistent, 1 needs review, 2 invalid/infeasible input. No result asserts physiological safety or efficacy. The prototype checks documented records, not every malformed arbitrary JSON shape.

Intake object keys: goal, start_date, event_date, other_key_dates, availability, rest_preferences, timezone, units, recent_training, longest_recent, running_limitations, race_results. An empty race_results list explicitly means no results; it does not block effort-based planning. Optional horizon_weeks can substitute for an event date. Timezone becomes blocking only with calendar_export=true, and units only with distance_prescriptions=true. These two flags describe output needs, not data-source permissions. Values are coaching evidence, not a standardized medical profile. The helper detects missing fields, not semantic completeness: “variable shifts” may require follow-up. Block dates without a final race can use event_date as the requested end date, clearly labelled.

## Interface

`validate(plan)` accepts a dictionary and returns findings, per-window totals, elapsed gaps between declared substantial sessions, and a structural status. See `fixture()` in `test_validator.py` for an example. It is a prototype for the documented fields, not a hardened arbitrary-JSON ingestion API.

- `mode`: planned or actual; these are never summed together.
- `sessions`: stable id, state, aware ISO start/end, purpose, effort, explicit components in km; optional sessions are separate from required totals.
- For repetitions: repetition count and recovery seconds. For quality work: pace-basis and review metadata.
- `availability`: timestamp intervals; sessions must fit completely inside an interval. Optional sessions must also fit. Slots should already include required transition buffers.
- `windows`: timestamp bounds and optional inclusive distance target range. Whole-session attribution uses start time; straddling sessions trigger review. Arbitrary windows permit adjacent-week inspection.
- `source_id`: an already-reconciled canonical activity identity. This catches exact duplicate identities only. Matching COROS and Strava records to a canonical identity remains future adapter work.
- `history_review`, `goal_review`, session `constraint_review` and `recovery_review`: audit markers that a human/coaching review was recorded. A true boolean does not demonstrate that the underlying judgement was correct.

The prototype assumes session start/end covers the whole scheduled session, not only work repetitions. It does not check whether supplied duration matches distance and pace. Duration/pace consistency, phase coverage, coherent progressive stimulus, terrain and fueling appropriateness remain manual review tasks.

An empty input or missing dose cannot pass as fully specified. A structurally consistent result explicitly returns `physiological_validation: not_assessed`. Review findings do not all require asking the user: explain or resolve from existing context when possible.


Review bounds for full session duration at the slower plausible pace; the current script does not calculate duration from pace/repetitions. Phase coverage, stimulus, trail/hill stress, training efficacy and individual recovery remain coaching checks. Flexible day/time-cap plans can be reviewed manually without inventing fixed timestamps.

Future wearable adapters must preserve provenance/units/timezone, reconcile duplicates, and distinguish planned, actual, missing and estimated data. No connector or account is required by this package.

## Optional preference intake

The athlete object may contain `preferences` as an object with `quality_frequency`, `long_run_days`, `workout_days`, `workout_style`, `schedule_style`, and `method_preference`. Values are descriptive preferences reviewed by the agent, not prescribed load. Explicit zero faster workouts, empty day-preference lists, or “unsure” are valid answers. The string `"no_preference"` for the whole preferences value means skip the preference follow-up. Missing fields yield nonblocking `preference_questions` with `required: false`. These do not change the essential-intake gate and do not automatically select a method or determine feasibility. Malformed preference containers are rejected.
