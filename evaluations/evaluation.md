# Run Plan Coach prototype evaluation

## Scope

Version 0.1.0, October 21, 2026. Portable skill with prompt/rules, intake helper and structural validator. No real plan generation or connected data use. Source package: `.`. Run tests from that folder with `python3 -m unittest discover -s scripts -v`.

## Independent runner interaction

An independent agent was asked to invent a stable recreational-runner profile and start with a natural short request. Parent conducted intake, delivered a 12-week synthetic phase/session outline, received a travel disruption, revised, then provided a consolidated calendar and requested an audit. The profile was revealed after the first revision. Two later questions added injury-location and route-access details; these were not secretly present from the start. See synthetic_runner.json, synthetic_plan.md and selected verbatim runner_feedback.md. The conversation itself is the full transcript; excerpts here are explicitly not a verbatim reconstruction.

Observed successes: intake elicited three versus optional-four-day preference; Tuesday door-to-door distinction; confounded race results; current load; past soreness; confirmed course/date; normal recovery; commute; initial holiday. Follow-up detected a race-day exemption from the usual two-hour cap. The runner later introduced a work trip. The response removed the missed long run and reduced subsequent load rather than adding catch-up. No pace was inferred from the older compromised half.

Observed failures and revisions: initial plan used week labels rather than explicit Sunday dates; effort cue 'controlled quicker' was unclear; shortened-run response was underspecified; first revision required merging patches; symptom fallback was vague; winter route access and equipment were not elicited; race-result years were initially assumed. Final follow-up confirmed years, clarified route access, and exposed hotel treadmill uncertainty. The final audit still requested a lower-duration selection rule, unsafe-footing fallback and clarification that normal required sessions are not obligations overriding illness/symptoms. All are incorporated into the final skill and consolidated scenario artifact. The persona did not re-review those final three textual changes, so those remain parent-reviewed corrections rather than an independently passed retest.

## Independent novice cold-start pass

A second independent agent read the skill and received a different fictional request: novice 10K, variable shifts, no smartwatch/results, 20-minute walk/jogs. It produced three grouped questions on race/date/goal, time/shift flexibility and actual training/limitations. It did not invent paces or demand a watch/race test. This pass tested only the first reply, not a complete novice plan.

Its ambiguity report prompted optional timezone/units for time-only guidance, explicit horizon support without a terminal race, and clearer instructions on interim advice while basic intake is incomplete. Changed intake logic now has boundary tests for those conditions.

## Mechanical results

41 test methods pass, including 180 generated availability boundaries and 101 component partitions, plus tests of optional/no-race intake, reuse of known information, time-only versus calendar/distance needs, plan/actual separation, duplicate canonical activities, missing versus zero data, timezone offsets, invalid values and rounding. CLI exit/status contracts also pass. Standard-library Python only. Skill frontmatter/scaffold validation passes.

## Limits

One multi-turn persona and one novice first reply do not establish universal effectiveness. No weeks of exercise occurred and no simulated race result was used. The validator does not model physiological adaptation, sufficient stimulus, overtraining or injury risk. Boolean review markers are audit notes, not proof. Wearable ingestion, automatic cross-provider identity matching, full schema hardening, multi-language usability and prospective real-runner evaluation remain unimplemented.

Next useful scenarios: changing shift calendars across a complete plan, trail time/elevation goals, no-race consistency blocks, missing history, competing priority races, and actual data adapter checks before personalized use. Do not optimize only for these two personas.
