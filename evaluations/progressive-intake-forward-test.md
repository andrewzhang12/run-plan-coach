# Progressive intake usability revision

October 22, 2026. Trigger: real user reported that the question-heavy intake was difficult to answer and requested a consumer-style questionnaire with options and incremental progress. The following scripted/persona checks are synthetic; they do not measure broad user satisfaction or training outcomes.

## Product changes

The runner-facing default CLI and skill instructions now show at most two atomic questions per round, with lettered options, unit-aware volume/time bands, day multiselect, explicit weight-training frequencies, and none/not-sure/skip paths. Common short answers are normalized selectively; other free text remains a self-report for the agent. Exact data is requested only on relevant branches. The earlier compound completeness prompts remain available only through developer `--audit`.

The profile summary retains ranges and unknowns rather than turning bands into exact prescriptions. Material intake can end at an early outline checkpoint; optional questions resume only when the runner chooses to continue. `intake_summary` and `preview_available` never imply readiness for individualized training doses.

## Independent first pass

An independent evaluator read the instructions/code and exercised an option-only novice path. It observed <=2 questions per round but 11 rounds/19 selections to exhaust that path. It found that typed 'not running' and 'no results' did not drive expected branches, typed 'not sure' could be omitted from unresolved items, skipping days suppressed weekday caps, and date questions appeared without a confirmed booking.

Corrections: limited common-answer aliases and consistent unknown tracking; cap questions retained for unknown/declined days; exact date gated on a booked-date choice; default early preview when the core goal/history/schedule/limitations are available. Optional exercise/preference/result details remain available after that checkpoint. The agent must still resolve material ambiguities before detailed workouts.

## Independent second pass

The evaluator confirmed the corrected branches, <=2-question limit, retained `not_assessed` status and explicit optional continuation. Its tested path reached a preview after 8 rounds with 7 optional/review items deferred. A local reproducible path reached the same checkpoint after 13 selections. This is one artificial path, not an average completion time or a guarantee for all users.

It then found two more issues: unknown units fell through to mile bands, and '10K' was not normalized as a short-race goal. Both were fixed with targeted regression tests. Unknown/unrecognized units now use the minutes path rather than guessing miles; 5K/10K common spellings drive race-goal branches. These final two fixes were covered by code regression tests, not a claimed third independent behavioral pass.

## Verification and limits

92 software test methods pass, including progressive branching, state save/resume, skip/unknown handling, unit-specific bands, zero-workout paths, nonmutation, preview gating, and the existing structural checks. The three documented multi-round CLI commands were exercised with a temporary state file. No files are persisted by the intake CLI without explicit `--save`.

This is still an agent-operated survey, not a full browser form, general NLU engine or standalone coaching app. The host agent renders concise options/controls, accepts shorthand such as `1B, 2A`, and maps those replies to stable question IDs. The Python helper accepts `--answer QUESTION_ID=ANSWER`. Code does not automatically translate arbitrary conversation into fitness records or training prescriptions.
