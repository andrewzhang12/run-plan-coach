"""Progressive choice-based intake; use --audit for internal field completeness."""
import argparse
import json

GROUPS = (
 ('goals', ('goal', 'start_date', 'event_date', 'other_key_dates'),
  'What is the goal and date, when can the block start, and what other races, travel or unavailable dates matter?'),
 ('schedule', ('availability', 'rest_preferences', 'timezone', 'units'),
  'Which days/time windows can you run, what rest/long-run preferences matter, and what timezone/units do you use? Do caps include transitions?'),
 ('training', ('recent_training', 'longest_recent', 'running_limitations'),
  'What have you actually run in the last 4–6 weeks, what was the longest comfortable run, and are there current symptoms or recent running limitations?'),
 ('evidence', ('race_results',),
  'Any recent race/time-trial results at different distances? Include dates, effort and course/conditions if known. None is fine; we can use effort instead of exact pace.'),
)


PREFERENCE_GROUPS = (
 ('workout_load', ('quality_frequency',),
  'How many faster or structured workouts would you prefer per week: none, one, two, or unsure? We will also count a demanding long run when reviewing total load.'),
 ('timing', ('long_run_days', 'workout_days'),
  'Would you prefer long runs on weekends, weekdays, or either? Which days suit workouts, and are longer weekday sessions possible within your stated time limits?'),
 ('format', ('workout_style', 'schedule_style'),
  'Do you prefer continuous efforts, repetitions, simple effort cues or detailed pace targets? Would you rather have fixed days or a movable weekly sequence?'),
 ('method', ('method_preference',),
  'Any training approach you have liked or disliked, or no preference? You do not need to know named plans; we can explain a fit after reviewing your answers.'),
)


def preference_questions(profile):
    preferences = profile.get('preferences')
    if preferences == 'no_preference':
        return []
    if preferences is None:
        preferences = {}
    if not isinstance(preferences, dict):
        raise ValueError('preferences must be an object or "no_preference"')
    result = []
    for group, fields, question in PREFERENCE_GROUPS:
        missing = [f for f in fields if not present(preferences, f)]
        if missing:
            result.append(dict(group=group, missing=missing, question=question, required=False))
    return result


def present(profile, key):
    return key in profile and profile[key] is not None and profile[key] != ''


def assess(profile):
    if not isinstance(profile, dict):
        raise ValueError('Athlete input must be a JSON object')
    questions = []
    for name, fields, question in GROUPS:
        missing = [f for f in fields if not present(profile, f)]
        if missing:
            questions.append(dict(group=name, missing=missing, question=question))
    optional_fields = {'race_results', 'timezone', 'units'}
    if profile.get('horizon_weeks') is not None:
        optional_fields.add('event_date')
    if profile.get('calendar_export'):
        optional_fields.discard('timezone')
    if profile.get('distance_prescriptions'):
        optional_fields.discard('units')
    blocking = [q for q in questions if any(f not in optional_fields for f in q['missing'])]
    # Evidence and representation fields are conditional; completeness is not adequacy.
    return dict(stage='intake' if blocking else 'provisional_planning', questions=questions,
                preference_questions=preference_questions(profile),
                exact_pace_supported='not_assessed',
                note='Reuse known answers; ask only missing material parts of each group. Field presence does not establish adequacy or verified fitness.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('athlete_json')
    parser.add_argument('--continue-survey', action='store_true', help='Continue optional rounds after the preview checkpoint')
    parser.add_argument('--audit', action='store_true', help='Internal completeness report, not a runner questionnaire')
    parser.add_argument('--answer', action='append', default=[], metavar='QUESTION=ANSWER', help='Record a choice code or short answer; may repeat')
    parser.add_argument('--save', help='Explicit destination for updated profile; no file is changed by default')
    args = parser.parse_args()
    try:
        with open(args.athlete_json, encoding='utf-8') as f:
            profile=json.load(f)
        if args.audit:
            if args.answer or args.save or args.continue_survey:
                raise ValueError('--audit cannot be combined with --answer or --save')
            result=assess(profile)
        else:
            from survey import answer, next_round
            for entry in args.answer:
                key, separator, reply=entry.partition('=')
                if not separator:raise ValueError('--answer needs QUESTION=ANSWER')
                profile=answer(profile,key,reply)
            result=next_round(profile, continue_survey=args.continue_survey)
            if args.save:
                from pathlib import Path
                out=Path(args.save);out.parent.mkdir(parents=True,exist_ok=True)
                out.write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(result,indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'{exc}\n')

if __name__ == '__main__':
    main()
