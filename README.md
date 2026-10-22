# Run Plan Coach

A portable agentic skill for running-plan intake, purpose-first training design, and structural validation. It works from a conversation and self-reported training history; no wearable or account connection is required.

**Status:** v0.3.0 prototype. The agent designs and reviews the plan; Python checks selected intake, scheduling and bookkeeping rules. It is not a calibrated physiological, medical or performance-prediction model.

> **Experimental LLM-based tool—not professional coaching or medical advice.** AI-generated plans can be wrong or unsuitable. Tests check selected software behavior, not training safety or effectiveness. Read [Important limitations and responsible use](DISCLAIMER.md) before using the skill or its synthetic examples.

## Quick start

- **Runners:** [start a coaching conversation](docs/quickstart-runners.md)—no watch, race results or Python required.
- **Agents and Codex users:** [install/load the skill](docs/quickstart-agents.md).
- **Developers:** [run working JSON examples and checks](docs/quickstart-developers.md).
- **Choosing an approach:** [Hudson, Hansons, Pfitzinger, Daniels 2Q and deliberate hybrids](references/training-methods.md).

## What it does

- Uses a progressive survey: one or two easy multiple-choice questions per round, with distance/time ranges and adaptive follow-ups.
- Reuses known information about goals, dates, scheduling preferences, conflicts and current training.
- Requests recent race results at several distances when available, without making them mandatory.
- Builds phases and weekly ranges before selecting each run's purpose, intensity and complete dose.
- Reviews calendar feasibility, supporting recovery, adjacent weeks, disruptions and conditional race goals.
- Works with effort/time guidance for runners without a watch or representative race results.
- Separates actual, planned, optional, missing and estimated information.
- Asks about workout frequency, long-run/workout timing and format preferences before explaining which concepts fit.
- Explains source-informed training philosophies and allows explicit, workload-aware hybrids rather than stacking complete programs.

## Use the skill

Load [SKILL.md](SKILL.md) and follow its linked references in an agent that supports local skills. A useful starting request is:

> Use run-plan-coach to help plan my running. Ask for missing goals, schedule and training information first.

For Codex, place this repository folder in your skills directory, normally `~/.codex/skills/run-plan-coach`, or copy it there. Invoke `$run-plan-coach` after the skill is recognized; a new session may be needed. Other agents can use the Markdown instructions without the Codex UI metadata.

The skill should not assume the repository owner's personal preferences, race goals or data access. Calendar/workout-platform writes remain separate from generating a plan.

## Python tools

Python 3 standard library only. Run from the repository root:

```bash
python3 -m unittest discover -s scripts -v
python3 scripts/intake.py athlete.json
python3 scripts/validate_plan.py plan.json
```

See [interface and limits](references/validation.md) for inputs. The plan checker returns exit code 0 for structural consistency, 1 for review or missing information, and 2 for invalid/infeasible input. None asserts training safety or efficacy. Intake field presence does not prove that the information is adequate.

## Repository layout

```text
DISCLAIMER.md               LLM, health, validation and privacy limitations
SKILL.md                    Agent instructions and workflow
agents/openai.yaml          Codex display metadata
references/intake.md        Adaptive questions and evidence handling
references/planning.md      Phase/session decisions and revision rules
references/validation.md    Script interface and limitations
references/simulation.md    Authorized synthetic-runner testing procedure
references/training-methods.md  Training concepts, translation and hybrid rules
docs/                       Runner, agent and developer quick starts
examples/                   Artificial runnable JSON fixtures
scripts/                    Intake helper, structural validator, and tests
evaluations/                Artificial runner scenario and feedback
```

## Validation so far

92 software test methods pass, including generated availability and arithmetic cases. One independent synthetic half-marathon persona reviewed a draft, introduced travel and critiqued revisions; a separate agent tested the first reply to a novice without race results. Feedback improved time caps, effort cues, disruption handling and consolidated revisions. A further [synthetic hybrid-method test](evaluations/method-hybrid-forward-test.md) checked that incompatible framework requests trigger clarification rather than workout stacking. Synthetic feedback tests usability and consistency, not physiological outcomes. No exercise or race took place. See the [evaluation report](evaluations/evaluation.md) and [synthetic feedback](evaluations/runner_feedback.md).

## Development priorities

- Broaden full-conversation tests across shifting schedules, run/walk beginners, trails, multi-race seasons and no-race blocks.
- Harden the record schema and add duration/pace consistency and phase-coverage checks.
- Add optional data adapters only after validating units, timezones, source identity and completeness.
- Evaluate individual recommendations prospectively against real execution and recovery.

## Data boundaries

The repository contains no personal runner logs, credentials or live-account integrations. Keep any future personal inputs outside tracked files, for example in ignored `local-data/`. Device predictions are estimates; missing records are unknown, and duplicate provider activities need reconciliation before totals.

This prototype links to source guidance rather than redistributing proprietary training plans.

## Disclaimers and licensing

Read [DISCLAIMER.md](DISCLAIMER.md) for the project’s professional, health, AI-reliability, testing, privacy and affiliation limits. Making this repository public does not grant an open-source license; no such license is included at present.
