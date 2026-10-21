import unittest
from intake import assess


def complete():
    return dict(goal='finish 10K',start_date='2027-01-04',event_date='2027-03-07',other_key_dates=[],availability={'variable':True},rest_preferences=[],timezone='Europe/London',units='km',recent_training={'minutes':[40,50,45]},longest_recent={'minutes':25},running_limitations=False,race_results=[])


class IntakeTests(unittest.TestCase):
    def test_new_runner_gets_grouped_questions(self):
        r=assess({});self.assertEqual(len(r['questions']),4);self.assertEqual(r['stage'],'intake')
    def test_explicit_no_races_not_blocking(self):
        self.assertEqual(assess(complete())['questions'],[])
    def test_missing_results_optional(self):
        p=complete();del p['race_results'];r=assess(p);self.assertEqual(r['stage'],'provisional_planning');self.assertEqual(r['questions'][0]['group'],'evidence')
    def test_reuse_known_schedule(self):
        p=complete();del p['event_date'];r=assess(p);self.assertEqual(r['questions'][0]['missing'],['event_date'])
    def test_no_limitations_is_known(self):
        self.assertFalse(any(q['group']=='training' for q in assess(complete())['questions']))
    def test_unknown_limitations_remains_question(self):
        p=complete();p['running_limitations']=None;self.assertEqual(assess(p)['stage'],'intake')
    def test_no_inferred_pace(self):
        self.assertEqual(assess(complete())['exact_pace_supported'],'not_assessed')
    def test_reject_non_object(self):
        with self.assertRaises(ValueError):assess([])

class ConditionalIntakeTests(unittest.TestCase):
    def test_effort_only_does_not_block_on_units_or_timezone(self):
        p=complete();del p['units'];del p['timezone'];self.assertEqual(assess(p)['stage'],'provisional_planning')
    def test_calendar_requires_timezone(self):
        p=complete();del p['timezone'];p['calendar_export']=True;self.assertEqual(assess(p)['stage'],'intake')
    def test_distance_requires_units(self):
        p=complete();del p['units'];p['distance_prescriptions']=True;self.assertEqual(assess(p)['stage'],'intake')
    def test_horizon_can_replace_race_date(self):
        p=complete();del p['event_date'];p['horizon_weeks']=8;self.assertEqual(assess(p)['stage'],'provisional_planning')

if __name__ == '__main__':unittest.main()
