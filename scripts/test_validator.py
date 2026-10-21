import copy
import unittest
from datetime import datetime, timedelta
from validator import validate


def fixture():
    return dict(mode='planned', history_review=True, goal_review=True,
        availability=[dict(start='2027-01-04T06:00:00-05:00',end='2027-01-04T08:00:00-05:00')],
        windows=[dict(id='w',start='2027-01-04T00:00:00-05:00',end='2027-01-11T00:00:00-05:00',target_km=[10,10])],
        sessions=[dict(id='a',state='planned',start='2027-01-04T06:00:00-05:00',end='2027-01-04T07:00:00-05:00',
                       purpose='aerobic',effort='easy',constraint_review=True,components=[dict(km=10)])])


def codes(p):
    return {x['code'] for x in validate(p)['findings']}


class ValidationTests(unittest.TestCase):
    def test_consistent_is_not_physiological_pass(self):
        r=validate(fixture());self.assertEqual(r['status'],'structurally_consistent');self.assertEqual(r['physiological_validation'],'not_assessed')
    def test_time_conflict_and_boundary(self):
        p=fixture();p['availability'][0]['end']='2027-01-04T07:00:00-05:00';self.assertNotIn('outside_availability',codes(p))
        p['availability'][0]['end']='2027-01-04T06:59:59-05:00';self.assertIn('outside_availability',codes(p))
    def test_duplicate_and_overlap(self):
        p=fixture();p['sessions']*=2;self.assertTrue({'session_id','session_overlap'}<=codes(p))
    def test_cross_provider_duplicate(self):
        p=fixture();p['sessions'][0]['source_id']='canonical-activity';b=copy.deepcopy(p['sessions'][0]);b.update(id='b',start='2027-01-04T07:00:00-05:00',end='2027-01-04T08:00:00-05:00');p['sessions'].append(b);self.assertIn('duplicate_source',codes(p))
    def test_optional_not_required(self):
        p=fixture();p['sessions'][0]['optional']=True;r=validate(p);self.assertEqual(r['windows'][0]['required_km'],0);self.assertEqual(r['windows'][0]['optional_km'],10);self.assertIn('target_mismatch',codes(p))
    def test_actual_not_added_to_plan(self):
        p=fixture();b=copy.deepcopy(p['sessions'][0]);b.update(id='actual',state='actual');p['sessions'].append(b);self.assertEqual(validate(p)['windows'][0]['required_km'],10);self.assertNotIn('session_overlap',codes(p))
    def test_missing_is_not_zero(self):
        p=fixture();p['sessions'][0].pop('components');self.assertIsNone(validate(p)['windows'][0]['required_km']);self.assertIn('weekly_distance_unknown',codes(p))
    def test_invalid_numbers(self):
        for value in [-1,float('nan'),float('inf'),True]:
            with self.subTest(value=value):
                p=fixture();p['sessions'][0]['components'][0]['km']=value;self.assertIn('distance_invalid',codes(p))
    def test_repeated_work_requires_recovery(self):
        p=fixture();p['sessions'][0].update(effort='interval',reps=10,pace_basis='goal');self.assertTrue({'pace_evidence','rep_recovery_missing','recovery_unreviewed'}<=codes(p))
    def test_timezone_required(self):
        p=fixture();p['sessions'][0]['start']='2027-01-04T06:00:00';self.assertIn('session_time',codes(p))
    def test_end_after_start(self):
        p=fixture();p['sessions'][0]['end']=p['sessions'][0]['start'];self.assertIn('session_time',codes(p))
    def test_component_totals_include_recovery(self):
        p=fixture();p['sessions'][0]['components']=[dict(km=2),dict(km=4),dict(km=2),dict(km=2)];self.assertEqual(validate(p)['windows'][0]['required_km'],10)
    def test_cross_week_gap_end_to_start(self):
        p=fixture();p['sessions'][0].update(substantial=True,start='2027-01-10T19:00:00-05:00',end='2027-01-10T20:00:00-05:00');b=copy.deepcopy(p['sessions'][0]);b.update(id='b',start='2027-01-12T07:00:00-05:00',end='2027-01-12T08:00:00-05:00');p['sessions'].append(b);self.assertEqual(validate(p)['substantial_gaps'][0]['hours'],35)
    def test_missing_history_stays_unknown(self):
        p=fixture();p.pop('history_review');self.assertIn('history_unreviewed',codes(p))
    def test_effort_overrides_participation_label(self):
        p=fixture();p['sessions'][0].update(purpose='participation',effort='hard');self.assertIn('participation_effort',codes(p))
    def test_reordering_invariance(self):
        p=fixture();b=copy.deepcopy(p['sessions'][0]);b.update(id='b',start='2027-01-04T07:00:00-05:00',end='2027-01-04T08:00:00-05:00');p['sessions'].append(b);before=validate(p);p['sessions'].reverse();self.assertEqual(before,validate(p))
    def test_optional_outside_availability_still_conflicts(self):
        p=fixture();p['sessions'][0].update(optional=True,end='2027-01-04T09:00:00-05:00');self.assertIn('outside_availability',codes(p))
    def test_deterministic_generated_boundaries(self):
        for minutes in range(1,181):
            with self.subTest(minutes=minutes):
                p=fixture();start=datetime.fromisoformat(p['sessions'][0]['start']);p['sessions'][0]['end']=(start+timedelta(minutes=minutes)).isoformat()
                self.assertEqual('outside_availability' in codes(p), minutes>120)
    def test_generated_component_partition_invariance(self):
        for i in range(101):
            with self.subTest(split=i):
                p=fixture();p['sessions'][0]['components']=[dict(km=i/10),dict(km=(100-i)/10)];self.assertAlmostEqual(validate(p)['windows'][0]['required_km'],10)

class AdversarialInputTests(unittest.TestCase):
    def test_empty_input_not_pass(self):
        self.assertEqual(validate({})['status'],'needs_review')
    def test_malformed_target_returns_error(self):
        for target in [70, '70', [20], [30,20], [0,float('nan')]]:
            with self.subTest(target=target):
                p=fixture();p['windows'][0]['target_km']=target;self.assertIn('target_invalid',codes(p))
    def test_bad_reps_returns_error(self):
        for reps in ['10',0,-1,True,2.5]:
            with self.subTest(reps=reps):
                p=fixture();p['sessions'][0].update(effort='interval',reps=reps);self.assertIn('reps_invalid',codes(p))
    def test_bad_recovery_returns_error(self):
        p=fixture();p['sessions'][0].update(effort='interval',reps=2,recovery_seconds=-60);self.assertIn('recovery_invalid',codes(p))
    def test_decimal_roundoff_not_mileage_mismatch(self):
        p=fixture();p['sessions'][0]['components']=[dict(km=0.1),dict(km=0.2)];p['windows'][0]['target_km']=[0.3,0.3];self.assertNotIn('target_mismatch',codes(p))
    def test_utc_offset_changes_use_elapsed_time(self):
        p=fixture();p['sessions'][0].update(start='2027-03-14T01:30:00-05:00',end='2027-03-14T03:30:00-04:00');p['windows'][0].update(start='2027-03-14T00:00:00-05:00',end='2027-03-15T00:00:00-04:00');self.assertEqual(validate(p)['windows'][0]['scheduled_minutes'],60)

if __name__=='__main__':unittest.main(verbosity=2)
