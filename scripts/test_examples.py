"""Exercise the shipped quick-start fixtures, not their prose."""
import json
from pathlib import Path
import unittest
from intake import assess
from validator import validate

EXAMPLES=Path(__file__).resolve().parent.parent/'examples'


def load(name):
    return json.loads((EXAMPLES/name).read_text())


class QuickStartExamplesTests(unittest.TestCase):
    def test_incomplete_runner_prompts_for_material_gaps(self):
        r=assess(load('athlete-incomplete.json'))
        self.assertEqual(r['stage'],'intake')
        self.assertFalse(any(q['group']=='evidence' for q in r['questions']))
    def test_no_results_or_device_can_enter_provisional_planning(self):
        r=assess(load('athlete-effort-only.json'))
        self.assertEqual(r['stage'],'provisional_planning')
        self.assertEqual(r['exact_pace_supported'],'not_assessed')
    def test_structural_fixture_is_not_a_physiological_pass(self):
        r=validate(load('plan-structural.json'))
        self.assertEqual(r['status'],'structurally_consistent')
        self.assertEqual(r['windows'][0]['required_km'],10)
        self.assertEqual(r['physiological_validation'],'not_assessed')
    def test_guide_suggested_time_conflict_is_detected(self):
        p=load('plan-structural.json')
        p['sessions'][0]['end']='2027-01-05T07:01:00+00:00'
        r=validate(p)
        self.assertEqual(r['status'],'infeasible_or_invalid')
        self.assertIn('outside_availability',{f['code'] for f in r['findings']})
    def test_guide_suggested_mileage_mismatch_is_reviewed(self):
        p=load('plan-structural.json')
        p['windows'][0]['target_km']=[20,25]
        r=validate(p)
        self.assertEqual(r['status'],'needs_review')
        self.assertIn('target_mismatch',{f['code'] for f in r['findings']})

if __name__=='__main__':unittest.main()
