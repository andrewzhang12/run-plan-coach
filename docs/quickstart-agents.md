# Quick start for agents and skill users

Read [the disclaimer](../DISCLAIMER.md). The agent generates the plan; the scripts are optional intake and structural helpers, not an autonomous coach or a training optimizer.

## Codex installation

Clone into the normal local skill directory if that destination does not already exist:

```bash
git clone https://github.com/andrewzhang12/run-plan-coach.git ~/.codex/skills/run-plan-coach
```

If a copy already exists, inspect its local changes before updating it; do not overwrite it blindly. Start a new session if the skill is not yet recognized. Then invoke:

> Use $run-plan-coach to help plan my running. Reuse confirmed information and ask for material missing goals, race dates, availability and training evidence first.

A clone does not require GitHub CLI. The project currently has no open-source license; see the repository disclaimer before redistribution or reuse beyond permissions you hold.

## Other assistants

Use an assistant capable of reading local/project files. Load [SKILL.md](../SKILL.md), [DISCLAIMER.md](../DISCLAIMER.md), and only the supporting references routed by the skill. If attachments are needed, provide those actual files rather than expecting an assistant to retrieve a URL automatically. A plain-text assistant can follow the same workflow, but cannot claim to have run scripts or read files it cannot access.

Starter instruction:

> Follow the attached run-plan-coach SKILL.md. Collect only material missing information; recent races at multiple distances are optional. Produce a phase outline and the requested detail horizon, with assumptions, recovery and disruption rules. Consult the training-method reference when comparing or mixing systems. Do not claim physiological validation from structural checks.

No COROS connection, API key or computer-control permission is required. Use available logs only when relevant and authorized. Do not assume access to connected accounts or publish calendar/workout changes merely because planning was requested.

## Intake and delivery

1. Inspect available context and distinguish known facts, estimates and aspirations.
2. Ask grouped questions for material gaps; accept approximate history and effort-based training without races.
3. Resolve conflicting priorities and hard time limits before fixing mileage.
4. Explain the phase structure and selected method principles. When hybridizing, disclose which elements replace which, their prerequisites and the shared workload tradeoff.
5. Prescribe complete sessions; review adjacent weeks and return a single current plan after revisions.
6. For timestamped plans with suitable structured inputs and Python available, run the validator as the skill specifies. For flexible day/time-cap plans, or when execution is unavailable, review the relevant constraints manually and disclose the scope; do not invent timestamps to satisfy a script.

## Example requests

- “I have no races or watch; help me build an eight-week run/walk routine around changing shifts.”
- “Compare Hudson, Hansons, Pfitzinger and Daniels 2Q for my constraints before recommending a structure.”
- “Audit my proposed hybrid: have I kept two Daniels quality sessions and accidentally added a third demanding long run?”

The [developer quick start](quickstart-developers.md) contains executable JSON examples. These examples are artificial and are not workout recommendations.
