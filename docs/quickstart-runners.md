# Quick start for runners

This is an experimental LLM-based aid, not professional coaching or medical advice. Read [the limitations](../DISCLAIMER.md). No watch, race history, subscription to a training platform, or Python installation is required for the conversational workflow.

## 1. Start a conversation

In an agent with this skill installed, paste:

> Use run-plan-coach to help me build a running plan. Ask only one or two easy multiple-choice questions at a time, reuse anything I have already told you, and progress through goals, recent running and schedule. Use effort rather than exact pace when the evidence is insufficient. Show the phase outline before detailed workouts.

If the skill is not installed, follow the [agent setup guide](quickstart-agents.md). This repository is a skill/instruction package, not a hosted chatbot or standalone training app. Merely pasting the repository URL does not ensure an assistant has read it.

## 2. Answer a few easy choices at a time

You should get lettered choices, not a long form to fill in. Reply with letters such as `1B, 2A`, select the available controls, or use your own words. “Not sure” and “skip” are valid. The next round should adapt to what you said.

For example, weight training can be answered as none, occasionally, 1–2, 3–4 or 5+ days weekly; running volume can be a range in your preferred units. You do not need to reconstruct an exact training log to begin.

The assistant will collect relevant parts of the following over the conversation—not all in one reply:

Approximate answers are fine:

- What you want to achieve and by when; other races and which are serious efforts versus participation; travel and no-run dates.
- Available days and time per day, whether time includes preparation/travel, preferred long-run/rest days, and units.
- Completed running over the last 4–6 weeks, typical run durations, longest comfortable run, interruptions, relevant symptoms, and other substantial exercise.
- Recent race/time-trial dates, distances and results, if available. Note whether all-out, controlled, hilly, hot or interrupted. Several distances help reveal different strengths; none are mandatory.
- Any training-method preferences. “No preference,” “simple three-day routine,” or “explain the options” are useful answers.

Do not share credentials or unnecessary sensitive information. Your chosen assistant provider handles what you enter; local code does not make the chat confidential.

## 3. State how you like to train

The assistant should ask about missing preferences before selecting a framework: desired number of faster/structured sessions, long runs on weekdays versus weekends, suitable workout days, continuous work versus repetitions, simple effort versus pace targets, and fixed versus flexible scheduling. “No preference—explain a sensible starting point” is a complete answer. A demanding long run also counts when reviewing load.

Ask for the reasoning in everyday terms:

> Based on my preferences and actual time windows, which structure fits and why? Connect each recommendation to a specific concept, explain the tradeoff, and tell me what would be adapted. Don’t recommend a named system just because it sounds authoritative.

## 4. Review the outline

Ask the assistant to explain the goal priority, phase purposes, weekly time/distance ranges, and why the schedule fits your actual starting point. Challenge an assumption before it becomes a workout.

Examples:

> I have only three reliable run days. Keep Saturday genuinely optional; don't use it to meet the baseline mileage.

> Compare a Pfitzinger-inspired aerobic structure with a Daniels-informed approach. Explain tradeoffs before choosing one; don't combine both complete schedules.

## 5. Get usable workouts

Each session should have a purpose, total time/distance including easy running, and clear effort or evidence-supported pace. Repeated work needs recovery instructions. Ask for simple effort cues if watch programming is unwanted. The plan should specify what to drop first when life intervenes and what information would justify progression.

## 6. Report what actually happened

> I shortened Sunday's run because of time, not fatigue. I also have a work trip next week. Revise the affected weeks and return one consolidated current schedule; don't make me catch up mileage.

Distinguish time conflicts from fatigue or symptoms. No plan requires running through illness, injury concerns or unsafe conditions. Improvements and race times are not guaranteed.

For method comparisons, see [training philosophies and hybrids](../references/training-methods.md). Their names are not certifications or endorsements.
