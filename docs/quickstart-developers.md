# Quick start for developers

Requirements: Python 3 standard library. No API token, model dependency or wearable connection is required. Run commands from the repository root. The conversational skill still needs a host LLM; these scripts do not generate training plans.

## Run the tests

```bash
python3 -m unittest discover -s scripts -v
```

## Inspect intake gaps

```bash
python3 scripts/intake.py examples/athlete-incomplete.json
python3 scripts/intake.py examples/athlete-effort-only.json
```

The first returns grouped missing-information questions. The second can enter provisional planning despite having no race results. Field presence is not proof of adequate history; the agent must inspect values and ask relevant follow-ups. Timezone and units are conditional on calendar and distance outputs. No tool infers a training pace here.

## Check a structural example

```bash
python3 scripts/validate_plan.py examples/plan-structural.json
```

Expected exit code: 0, status `structurally_consistent`, physiological validation `not_assessed`. This two-session fixture demonstrates arithmetic and available-time bookkeeping only. It is not a complete training week or recommended plan. Boolean review markers are audit metadata, not clinical evidence.

Exit codes are 0 for structural consistency, 1 for missing information/review, and 2 for invalid/infeasible input. Changing a session's end beyond its availability window should produce an error. Changing a weekly target without changing scheduled distance should produce a review finding.

Read [the interface](../references/validation.md) before extending records. Method selection and hybrid compatibility are currently agent-side decisions described in [training methods](../references/training-methods.md), not a physiological model or code-enforced certification.

## Extend the skill

- Keep [SKILL.md](../SKILL.md) as a concise router; add detailed guidance in linked references.
- Introduce a new method only with a source, intended context, assumptions, terminology and failure modes; distinguish that source's philosophy from this project's adaptations.
- Add executable tests for observable software behavior, not tests that assert prose sounds right.
- Keep synthetic evaluation fixtures explicitly artificial. Never add a real runner's health data or credentials to public test cases.
- For authorized role-play, follow [the simulation procedure](../references/simulation.md). Role-play feedback tests usability, not actual training response.
- Recheck documentation examples and links after changing the interface.

The repository is public but has no open-source license at present. Consult [the disclaimer](../DISCLAIMER.md) before redistribution or reuse beyond permissions you hold.
