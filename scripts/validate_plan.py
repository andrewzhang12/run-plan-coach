"""CLI for structural plan checks; never a physiological assessment."""
import argparse
import json
from validator import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan_json')
    args = parser.parse_args()
    try:
        with open(args.plan_json, encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError('Plan input must be an object')
        result = validate(data)
        print(json.dumps(result, indent=2))
        return 2 if result['status'] == 'infeasible_or_invalid' else 1 if result['status'] == 'needs_review' else 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps(dict(status='infeasible_or_invalid', input_error=str(exc), physiological_validation='not_assessed'), indent=2))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
