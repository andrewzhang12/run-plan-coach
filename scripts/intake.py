"""Group material intake gaps. None/absent means unknown; False/[] can mean none."""
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
                exact_pace_supported='not_assessed',
                note='Reuse known answers; ask only missing material parts of each group. Field presence does not establish adequacy or verified fitness.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('athlete_json')
    args = parser.parse_args()
    try:
        with open(args.athlete_json, encoding='utf-8') as f:
            print(json.dumps(assess(json.load(f)), indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'{exc}\n')

if __name__ == '__main__':
    main()
