import unittest
from survey import next_round,answer,candidates


def choose(p,key,text):return answer(p,key,text)


class SurveyTests(unittest.TestCase):
    def test_first_round_is_two_easy_choices(self):
        r=next_round({});self.assertEqual(len(r['questions']),2)
        self.assertTrue(all(q['options'] for q in r['questions']))
    def test_answers_advance_without_repeating(self):
        p=choose({},'goal_kind','B');p=choose(p,'priority','A')
        self.assertEqual(next_round(p)['questions'][0]['id'],'units')
    def test_units_before_mileage_and_minutes_path(self):
        p=choose({},'units','C');p=choose(p,'runs','B')
        self.assertIn('weekly_minutes',[q['id'] for q in candidates(p)])
        self.assertNotIn('weekly_distance',[q['id'] for q in candidates(p)])
    def test_known_minutes_unit_is_not_miles(self):
        self.assertIn('weekly_minutes',[q['id'] for q in candidates({'units':'minutes'})])
    def test_mile_options_do_not_use_km(self):
        p=choose({},'units','B');q=next(q for q in candidates(p) if q['id']=='weekly_distance')
        self.assertIn('mi',q['options'][0]['label'])
    def test_band_is_not_converted_to_exact_mileage(self):
        p=choose({},'units','A');p=choose(p,'weekly_distance','C')
        self.assertEqual(p['survey_answers']['weekly_distance']['value'],'20 to under 40 km')
    def test_no_race_results_skips_details(self):
        p=choose({},'race_history','C')
        self.assertNotIn('race_detail',[q['id'] for q in candidates(p)])
    def test_yes_result_branches_to_short_entry(self):
        p=choose({},'race_history','B')
        self.assertIn('race_detail',[q['id'] for q in candidates(p)])
    def test_no_other_exercise_skips_followup(self):
        p=choose({},'other_sport','A')
        self.assertNotIn('other_sport_detail',[q['id'] for q in candidates(p)])
    def test_strength_frequencies_have_distinct_values(self):
        q=next(q for q in candidates({}) if q['id']=='strength')
        self.assertEqual(len({o['value'] for o in q['options']}),len(q['options']))
    def test_symptoms_branch(self):
        p=choose({},'limitations','B')
        self.assertIn('limitation_detail',[q['id'] for q in candidates(p)])
    def test_no_symptoms_does_not_request_medical_essay(self):
        p=choose({},'limitations','A')
        self.assertNotIn('limitation_detail',[q['id'] for q in candidates(p)])
    def test_weekend_only_skips_weekday_cap(self):
        p=choose({},'days','F,G')
        self.assertNotIn('weekday_cap',[q['id'] for q in candidates(p)])
    def test_multiselect_and_variable_are_exclusive(self):
        with self.assertRaises(ValueError):choose({},'days','A,H')
    def test_single_choice_rejects_multiple_letters(self):
        with self.assertRaises(ValueError):choose({},'units','A,B')
    def test_no_faster_workouts_skips_workout_preferences(self):
        p=choose({},'quality_frequency','A')
        self.assertNotIn('workout_days',[q['id'] for q in candidates(p)])
        self.assertNotIn('workout_style',[q['id'] for q in candidates(p)])
    def test_door_to_door_needs_running_time(self):
        p=choose({},'caps_include','B')
        self.assertIn('running_cap',[q['id'] for q in candidates(p)])
    def test_decline_is_not_reasked_or_treated_as_none(self):
        p=choose({},'limitations','skip');r=next_round(p)
        self.assertIn('limitations',r['unresolved'])
        self.assertNotIn('limitations',[q['id'] for q in candidates(p)])
    def test_exact_race_date_validation(self):
        p=choose({},'goal_kind','B');p=choose(p,'timing','A')
        with self.assertRaises(ValueError):choose(p,'event_date','March sometime')
        p=choose(p,'event_date','2027-03-21')
        self.assertEqual(p['survey_answers']['event_date']['value'],'2027-03-21')
    def test_persisted_known_profile_is_reused(self):
        p={'goal':'fitness','recent_training':{'minutes':[60]},'longest_recent':{'minutes':25},'running_limitations':False}
        ids=[q['id'] for q in candidates(p)]
        self.assertFalse(set(['goal_kind','priority','runs','weekly_minutes','longest_minutes','limitations'])&set(ids))
    def test_unknown_question_not_written(self):
        with self.assertRaises(ValueError):choose({},'not_a_question','A')
    def test_full_survey_can_complete_with_skip_without_loop(self):
        p={}
        for _ in range(40):
            r=next_round(p)
            self.assertLessEqual(len(r['questions']),2)
            if not r['questions']:break
            p=choose(p,r['questions'][0]['id'],'skip')
        self.assertEqual(next_round(p)['stage'],'intake_summary')
        self.assertTrue(next_round(p)['unresolved'])
    def test_dynamic_round_rechecks_branches(self):
        p={}
        for _ in range(40):
            r=next_round(p)
            if not r['questions']:break
            first=r['questions'][0]
            p=choose(p,first['id'],'A' if first['options'] else 'skip')
        self.assertEqual(next_round(p)['stage'],'intake_summary')
    def test_invalid_letter_does_not_become_evidence(self):
        with self.assertRaises(ValueError):choose({},'units','Z')
    def test_broken_saved_state_has_clear_error(self):
        with self.assertRaises(ValueError):next_round({'survey_answers':{'units':'B'}})
    def test_summary_never_certifies_readiness(self):
        self.assertEqual(next_round({})['readiness'],'not_assessed')
    def test_preview_can_precede_optional_questions(self):
        p={'goal':'fitness','recent_training':{'minutes':[60]},'availability':{'days':['Tue','Sun']},'running_limitations':False}
        r=next_round(p);self.assertTrue(r['preview_available']);self.assertFalse(r['questions']);self.assertGreater(r['remaining_optional_or_review_count'],0)
    def test_no_preview_fitness_inferred_from_uncertain_history(self):
        p={'goal':'fitness','availability':{'days':['Tue']},'running_limitations':False}
        self.assertFalse(next_round(p)['preview_available'])
    def test_preview_not_a_detailed_plan_clearance(self):
        p={'goal':'fitness','recent_training':{'minutes':[60]},'availability':{'days':['Tue']},'running_limitations':False}
        r=next_round(p);self.assertTrue(r['preview_available']);self.assertEqual(r['readiness'],'not_assessed')
    def test_typed_not_running_skips_volume(self):
        p=choose({},'runs','not running')
        self.assertFalse({'weekly_minutes','weekly_distance','longest_minutes'} & {q['id'] for q in candidates(p)})
    def test_typed_no_results_and_no_other_sport_skip_details(self):
        p=choose({},'race_history','no results');p=choose(p,'other_sport','none')
        self.assertNotIn('race_detail',{q['id'] for q in candidates(p)})
        self.assertNotIn('other_sport_detail',{q['id'] for q in candidates(p)})
    def test_typed_unknown_remains_unresolved(self):
        p=choose({},'units','not sure');self.assertIn('units',next_round(p)['unresolved'])
    def test_declined_days_do_not_suppress_caps(self):
        p=choose({},'days','skip');self.assertIn('weekday_cap',{q['id'] for q in candidates(p)})
    def test_exact_date_requires_known_booking(self):
        p=choose({},'goal_kind','B');p=choose(p,'timing','C')
        self.assertNotIn('event_date',{q['id'] for q in candidates(p)})
    def test_optional_rounds_can_resume_after_preview(self):
        p={'goal':'fitness','recent_training':{'minutes':[60]},'availability':{'days':['Tue','Sun']},'running_limitations':False}
        self.assertFalse(next_round(p)['questions']);self.assertTrue(next_round(p,continue_survey=True)['questions'])
    def test_empty_availability_does_not_unlock_preview(self):
        p={'goal':'fitness','recent_training':{'minutes':[60]},'availability':{},'running_limitations':False}
        self.assertFalse(next_round(p)['preview_available'])
    def test_unknown_units_fall_back_to_minutes_not_miles(self):
        p=choose({},'units','not sure');ids={q['id'] for q in candidates(p)}
        self.assertIn('weekly_minutes',ids);self.assertNotIn('weekly_distance',ids)
    def test_short_race_words_drive_goal_branch(self):
        p=choose({},'goal_kind','10K');self.assertEqual(p['survey_answers']['goal_kind']['value'],'short_race')
        p=choose(p,'timing','A');self.assertIn('event_date',{q['id'] for q in candidates(p)})
    def test_profile_input_not_mutated(self):
        p={};choose(p,'units','A');self.assertEqual(p,{})

if __name__=='__main__':unittest.main()
