---
name: run-plan-coach
description: Build, revise, or audit running training plans through adaptive intake, purpose-first phase design, evidence-based workout dosing, and schedule validation. Works with self-reported history and race results; wearable connections are optional. Use for running coaching plans rather than general fitness advice or medical diagnosis.
---

# Run Plan Coach

Create a feasible, explainable running plan, not a calendar filled to a mileage quota. Work for an unfamiliar runner without connected accounts. Reuse relevant known preferences and recent evidence, confirming only what may have changed. Do not import another athlete's preferences, volume, race ambitions, or timelines.

## Intake first

Read [intake](references/intake.md). If material information is missing, start with a small grouped set of questions about race goals/dates, schedule/conflicts, current training/recovery, and recent races. Accept approximate answers, no races, or no wearable. Ask follow-ups only for gaps that change a decision. Never require a maximum-effort test to unlock a plan.

Distinguish missing from explicitly none and hard constraints from preferences. Do not invent dates, availability or current fitness. A goal time is not training evidence. For new users ask for recent race results at several distances if available, including date and context; do not demand a complete set. Missing pace evidence can support an effort-based plan if training history and schedule are sufficient.

Use `scripts/intake.py athlete.json` for grouped missing-information prompts if useful; the script's field completeness is only a lower bound on a coaching assessment. Preserve source, recency, units, timezone and uncertainty. Read connected tools only when available and relevant; do not imply access or require COROS. External calendar/workout writes are separate from generating a plan.

## Plan and review

Read [planning](references/planning.md). Establish ranked goals and constraints → provisional phases → feasible weekly time/distance ranges → session purposes and rest → complete session doses → review adjacent weeks → iterate. Change targets when constraints conflict. Report genuinely infeasible requirements and present a tradeoff; do not speed up easy running to fit a calendar.

Select pace evidence separately for economy, aerobic power, threshold, marathon specificity and easy endurance. Review combined workload rather than independently selecting the fastest pace in every category. Preserve phase specificity and useful progressive stimulus; avoiding all fatigue is not the goal.

Give the runner a phase outline and weekly ranges; provide day-level specifics to the requested horizon. Where longer plans are provisional, say what later decisions depend on. Include purpose, full time/distance, effort/pace basis, work/recovery details and one practical disruption fallback. Keep reasoning readable and device descriptions short.

For timestamped plans, read [validator interface](references/validation.md) and run `scripts/validate_plan.py plan.json`. Fix structural failures, resolve or disclose coaching-review findings and material unknowns. Do not manufacture timestamps to use the validator when the plan specifies flexible days/time caps; manually check slot and dose feasibility instead and state that scope. A machine result is not evidence of safety, fitness or adaptation.

## Adjustments

Keep planned and actual records separate. Evaluate representative execution, effort, symptoms and recovery before changing fitness estimates. Do not repay missed mileage. A participation race executed hard becomes a load change. Device predictions and recovery scores are supporting estimates; they do not override actual symptoms or authorize progression.

## Synthetic forward tests

When the user requests simulation or independent testing and delegation is available, read [simulation](references/simulation.md). Keep personas, plans and feedback explicitly synthetic. A simulated runner can evaluate assumptions and usability, not experience weeks of training or validate physiological outcomes. Do not spawn agents during ordinary coaching unless authorized.

## Deliverable

Return known inputs and consequential assumptions, unresolved tradeoffs, phase/weekly/session decisions, checks performed and adaptation rules. Ask only material outstanding questions. Preserve the user's chosen output destination; create no personal memory, calendar entry or external workout merely because a plan was requested.
