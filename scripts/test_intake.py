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

class PreferenceIntakeTests(unittest.TestCase):
    def test_optional_preferences_do_not_block_planning(self):
        r=assess(complete());self.assertEqual(r['stage'],'provisional_planning');self.assertEqual(len(r['preference_questions']),4)
    def test_explicit_no_preference_skips_questions(self):
        p=complete();p['preferences']='no_preference';self.assertEqual(assess(p)['preference_questions'],[])
    def test_zero_workouts_and_weekday_limits_are_known(self):
        p=complete();p['preferences']={'quality_frequency':0,'long_run_days':['Sunday'],'workout_days':[]};r=assess(p)
        self.assertFalse(any(q['group'] in ('workout_load','timing') for q in r['preference_questions']))
    def test_only_missing_timing_detail_is_flagged(self):
        p=complete();p['preferences']={'long_run_days':['Wednesday']};r=assess(p)
        q=next(q for q in r['preference_questions'] if q['group']=='timing');self.assertEqual(q['missing'],['workout_days'])
    def test_complete_preference_profile_reuses_answers(self):
        p=complete();p['preferences']={'quality_frequency':'unsure','long_run_days':[],'workout_days':[],'workout_style':'simple effort','schedule_style':'flexible','method_preference':'no_preference'}
        self.assertEqual(assess(p)['preference_questions'],[])
    def test_method_request_is_not_a_fitness_clearance(self):
        p=complete();p['preferences']={'method_preference':'Daniels 2Q','quality_frequency':2};del p['recent_training']
        r=assess(p);self.assertEqual(r['stage'],'intake');self.assertEqual(r['exact_pace_supported'],'not_assessed')
    def test_malformed_preference_container_has_clear_error(self):
        p=complete();p['preferences']=[]
        with self.assertRaises(ValueError):assess(p)

if __name__ == '__main__':unittest.main()
