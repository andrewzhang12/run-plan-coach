"""Progressive two-question intake. Ranges stay ranges; this does not prescribe load."""
from copy import deepcopy
from datetime import date


def q(key, prompt, labels, *, values=None, multi=False, text=False):
    options=[]
    for i,label in enumerate(labels):
        options.append({'code':chr(65+i),'label':label,'value':values[i] if values else label})
    return {'id':key,'prompt':prompt,'options':options,'multi_select':multi,
            'free_text_allowed':True,'answer_type':'text' if text else 'choice',
            'skip_allowed':True}


GOAL=q('goal_kind','What are you working toward?',
 ['5K or 10K','Half marathon','Marathon','General fitness / consistency','Something else','Not sure'],
 values=['short_race','half','marathon','fitness','other','unsure'])
PRIORITY=q('priority','What matters most?',
 ['Finish feeling good','Improve a time','Build a consistent habit','Help me decide'],values=['finish','time','consistency','unsure'])
UNITS=q('units','How do you prefer to describe your running?',
 ['Kilometres','Miles','Minutes — I do not track distance'],values=['km','mi','minutes'])
TIMING=q('timing','How far away is your goal?',
 ['I have a booked race date','Under 8 weeks','8–12 weeks','13–18 weeks','19+ weeks','No date / not sure'],values=['date_known','under_8','8_12','13_18','19_plus','unsure'])
DATE=q('event_date','If you have a booked race, what is its date?',
 ['Not booked / no exact date','Skip for now'],values=['not_booked','declined'],text=True)
RUNS=q('runs','Over the last month, how often have you usually run?',
 ['Not currently running','1–2 days/week','3–4 days/week','5+ days/week','It varies / not sure'],values=['zero','1_2','3_4','5_plus','unsure'])
DURATION=q('weekly_minutes','About how much running per week over the last month?',
 ['Under 60 minutes','60–119 minutes','120–239 minutes','240+ minutes','Not sure'],values=['under_60','60_119','120_239','240_plus','unsure'])
LONG=q('longest_minutes','Your longest comfortable recent run was roughly…',
 ['Under 30 minutes','30–59 minutes','60–89 minutes','90–119 minutes','120+ minutes','Not sure'],values=['under_30','30_59','60_89','90_119','120_plus','unsure'])
LIMITS=q('limitations','Is pain, illness or an injury currently limiting your running?',
 ['No','Yes','Recovering / returning, but unsure','Prefer to discuss later'],values=['none','yes','unsure','declined'])
LIMIT_DETAIL=q('limitation_detail','What currently limits your running? A few words are enough; we will not diagnose it.',[],text=True)
STRENGTH=q('strength','Do you also lift weights or do resistance training?',
 ['No','Occasionally — less than weekly','1–2 days/week','3–4 days/week','5+ days/week','Not sure / skip'],
 values=['none','occasional','1_2','3_4','5_plus','unsure'])
OTHER=q('other_sport','Any other regular exercise we should allow for?',
 ['None','Mostly gentle walking/cycling','Demanding sport or exercise','It varies / not sure'],values=['none','gentle','demanding','unsure'])
OTHER_DETAIL=q('other_sport_detail','Which sport/exercise, and roughly how often? A short answer is enough.',[],text=True)
DAYS=q('days','Which days could normally fit a run? Pick all that apply.',
 ['Mon','Tue','Wed','Thu','Fri','Sat','Sun','My days change'],values=['Mon','Tue','Wed','Thu','Fri','Sat','Sun','variable'],multi=True)
CAP=q('weekday_cap','On a normal available weekday, how much time can you give running?',
 ['Up to 20 min','Up to 30 min','Up to 45 min','Up to 60 min','More than 60 min','Different by day / not sure'],
 values=[20,30,45,60,'over_60','varies'])
TRANSITIONS=q('caps_include','Do those time limits include getting ready, travel or showering?',
 ['Running time only','Everything door to door','It depends / not sure'],values=['running_only','door_to_door','unsure'])
BUFFER=q('running_cap','How much of that window is actually available for running?',[],text=True)
LONGDAY=q('long_run_days','When would you prefer your longer run?',
 ['Weekend','Weekday','Either','No preference / help me decide'],values=['weekend','weekday','either','no_preference'])
LONGCAP=q('long_cap','How much running time could that longer-run day fit?',
 ['Up to 45 min','Up to 60 min','Up to 90 min','Up to 120 min','More than 120 min','Not sure'],values=[45,60,90,120,'over_120','unsure'])
CONFLICT=q('conflicts','Any dates or commitments the plan needs to work around?',
 ['None that I know of','Travel / no-run dates / other races','My schedule changes a lot','Not sure yet'],values=['none','dates','variable','unsure'])
CONFLICT_DETAIL=q('conflict_dates','Which dates or races? A short list is enough; approximate dates are fine.',[],text=True)
QUALITY=q('quality_frequency','How many faster/structured sessions would you enjoy each week?',
 ['None for now','One','Two','Help me decide'],values=[0,1,2,'unsure'])
WORKDAY=q('workout_days','When would faster/structured sessions fit best?',
 ['Weekdays','Weekends','Either / flexible','No preference'],values=['weekdays','weekends','either','no_preference'])
STYLE=q('workout_style','Which workout style sounds best?',
 ['Simple effort cues, no pace checking','Longer continuous efforts','Shorter repetitions with breaks','A mixture','Help me decide'],values=['effort','continuous','repetitions','mixed','unsure'])
RACE=q('race_history','Do you have recent race or time-trial results to share?',
 ['Yes, more than one distance','Yes, one result','No','Skip — use effort instead'],values=['several','one','none','declined'])
RACE_DETAIL=q('race_detail','Share a result as distance + time + approximate date (for example: 5K, 28:10, last month). More results are optional.',[],text=True)
RACE_CONTEXT=q('race_context','How representative were those results?',
 ['Hard effort, normal conditions','Controlled / not all-out','Heat, hills, stops or other complication','Not sure'],values=['representative','controlled','compromised','unsure'])


def validate_profile(profile):
    if not isinstance(profile,dict):raise ValueError('profile must be an object')
    records=profile.get('survey_answers',{})
    if not isinstance(records,dict):raise ValueError('survey_answers must be an object')
    for key,record in records.items():
        if not isinstance(record,dict) or not {'value','label','kind'} <= record.keys():
            raise ValueError(f'{key}: saved answer must include value, label and kind')


def value(profile,key):
    return profile.get('survey_answers',{}).get(key,{}).get('value')


def known(profile,key):
    return key in profile and profile[key] is not None and profile[key] != ''


def candidates(profile):
    """Branch on answers, reuse supplied profile facts, never ask a skipped question again."""
    items=[]
    def add(question,skip=False):
        if not skip and question['id'] not in profile.get('survey_answers',{}):items.append(question)
    add(GOAL,known(profile,'goal'));add(PRIORITY,known(profile,'goal'))
    add(UNITS,known(profile,'units'))
    add(TIMING,known(profile,'event_date') or known(profile,'horizon_weeks'))
    race_goal=value(profile,'goal_kind') in ('short_race','half','marathon')
    if race_goal and value(profile,'timing')=='date_known':add(DATE,known(profile,'event_date'))
    add(RUNS,known(profile,'recent_training'))
    if value(profile,'runs') != 'zero':
        units=profile.get('units',value(profile,'units'))
        if units not in ('km','mi'):
            add(DURATION,known(profile,'recent_training'))
        else:
            labels=['Under 10 km','10 to under 20 km','20 to under 40 km','40 to under 70 km','70+ km','Not sure'] if units=='km' else ['Under 6 mi','6 to under 13 mi','13 to under 25 mi','25 to under 45 mi','45+ mi','Not sure']
            add(q('weekly_distance','About how much running per week over the last month?',labels),known(profile,'recent_training'))
        add(LONG,known(profile,'longest_recent'))
    add(LIMITS,known(profile,'running_limitations'))
    if value(profile,'limitations') in ('yes','unsure'):add(LIMIT_DETAIL)
    add(DAYS,known(profile,'availability'))
    # Do not force weekday questions on a weekend-only runner.
    days=value(profile,'days')
    if days in (None,'declined','unsure') or 'variable' in days or any(d in days for d in ['Mon','Tue','Wed','Thu','Fri']):
        add(CAP,known(profile,'availability'))
        add(TRANSITIONS,known(profile,'availability'))
    if value(profile,'caps_include')=='door_to_door':add(BUFFER)
    add(LONGCAP,known(profile,'long_run_time_cap'))
    add(CONFLICT,known(profile,'other_key_dates'))
    if value(profile,'conflicts')=='dates':add(CONFLICT_DETAIL)
    add(STRENGTH,known(profile,'strength_training'))
    add(OTHER,known(profile,'other_training'))
    if value(profile,'other_sport')=='demanding':add(OTHER_DETAIL)
    prefs=profile.get('preferences',{})
    if prefs!='no_preference':
        if not isinstance(prefs,dict):raise ValueError('preferences must be an object or no_preference')
        add(LONGDAY,'long_run_days' in prefs)
        add(QUALITY,'quality_frequency' in prefs)
        if value(profile,'quality_frequency')!=0 and prefs.get('quality_frequency')!=0:add(WORKDAY,'workout_days' in prefs)
        add(STYLE,'workout_style' in prefs or value(profile,'quality_frequency')==0 or prefs.get('quality_frequency')==0)
    add(RACE,known(profile,'race_results') or value(profile,'runs')=='zero')
    if value(profile,'race_history') in ('several','one'):
        add(RACE_DETAIL);add(RACE_CONTEXT)
    return items


def answer(profile,key,reply):
    validate_profile(profile)
    p=deepcopy(profile)
    if not isinstance(p.get('survey_answers',{}),dict):raise ValueError('survey_answers must be an object')
    question=next((item for item in candidates(p) if item['id']==key),None)
    if question is None:raise ValueError(f'{key}: not an active unanswered question')
    reply=reply.strip()
    if not reply:raise ValueError('answer cannot be empty')
    normalized=' '.join(reply.lower().replace('’',"'").split())
    aliases={
        'runs':{'not running':'zero','no running':'zero','none':'zero'},
        'race_history':{'no results':'none','no races':'none','none':'none','no':'none'},
        'limitations':{'no':'none','none':'none','yes':'yes'},
        'other_sport':{'no':'none','none':'none'},
        'strength':{'no':'none','none':'none'},
        'quality_frequency':{'none':0,'zero':0,'one':1,'two':2},
        'units':{'km':'km','kilometres':'km','kilometers':'km','miles':'mi','mi':'mi','minutes':'minutes'},
        'goal_kind':{'5k':'short_race','10k':'short_race','5 km':'short_race','10 km':'short_race','half':'half','half marathon':'half','hm':'half','marathon':'marathon','fitness':'fitness'},
    }
    if normalized in ('not sure',"i don't know",'unsure','dont know'):
        record={'value':'unsure','label':'Not sure','kind':'unknown'}
    elif normalized in aliases.get(key,{}):
        v=aliases[key][normalized]
        option=next((o for o in question['options'] if o['value']==v),None)
        record={'value':v,'label':option['label'] if option else reply,'kind':'selection'}
    elif normalized in ('skip','decline'):
        record={'value':'declined','label':'Skipped','kind':'unknown'}
    else:
        options={o['code']:o for o in question['options']}
        codes=[c.strip().upper() for c in reply.split(',')]
        if all(c in options for c in codes):
            if len(codes)>1 and not question['multi_select']:raise ValueError('choose one option')
            codes=list(dict.fromkeys(codes))
            if question['multi_select'] and len(codes)>1 and any(options[c]['value']=='variable' for c in codes):raise ValueError('choose named days OR changing days, not both')
            chosen=[options[c] for c in codes]
            record={'value':[o['value'] for o in chosen] if question['multi_select'] else chosen[0]['value'],
                    'label':', '.join(o['label'] for o in chosen),'kind':'selection'}
        elif question['free_text_allowed']:
            if question['options'] and all(len(c)==1 and c.isalpha() for c in codes):
                raise ValueError('Choose one of the offered letters, or write a short answer in words')
            if question['id']=='event_date':
                try:date.fromisoformat(reply)
                except ValueError:raise ValueError('Use YYYY-MM-DD or choose not booked/skip')
            record={'value':reply,'label':reply,'kind':'self_report'}
        else:raise ValueError('unrecognized option')
    p.setdefault('survey_answers',{})[key]=record
    return p


def next_round(profile, continue_survey=False):
    validate_profile(profile)
    pending=candidates(profile)
    # Resolve branching questions before asking a question that might disappear or change units.
    selected=[]
    for item in pending:
        selected.append(item)
        if item['id'] in ('units','runs','limitations','other_sport','days','caps_include','quality_frequency','race_history'):break
        if len(selected)==2:break
    unknown=[k for k,r in profile.get('survey_answers',{}).items() if r.get('kind')=='unknown' or r.get('value') in ('unsure','declined')]
    goal_known=known(profile,'goal') or value(profile,'goal_kind') in ('short_race','half','marathon','fitness','other')
    history_known=known(profile,'recent_training') or value(profile,'runs')=='zero' or any(
        value(profile,k) not in (None,'unsure','declined','Not sure') for k in ('weekly_distance','weekly_minutes'))
    schedule_known=bool(profile.get('availability')) or (value(profile,'days') not in (None,'declined','unsure') and value(profile,'long_cap') not in (None,'unsure','declined') and (value(profile,'weekday_cap') not in (None,'varies','declined','unsure') or value(profile,'days')==['Sat','Sun'] or value(profile,'days')==['Sat'] or value(profile,'days')==['Sun']))
    limitations_known=known(profile,'running_limitations') or value(profile,'limitations')=='none'
    preview_available=bool(goal_known and history_known and schedule_known and limitations_known)
    remaining_count=len(pending)
    if preview_available and not continue_survey:selected=[]
    return {'stage':'intake_round' if selected else 'intake_summary',
            'message':'Pick letters or answer in your own words. We will take this a couple of questions at a time.' if selected else 'Here is what we have. Confirm the assumptions before detailed workouts.',
            'questions':selected,'answered_count':len(profile.get('survey_answers',{})),
            'remaining_optional_or_review_count':remaining_count if preview_available else None,
            'summary':{k:r['label'] for k,r in profile.get('survey_answers',{}).items()},
            'unresolved':unknown,'profile':deepcopy(profile),
            'preview_available':preview_available,
            'preview_note':'Offer a rough phase outline now. Ask whether the runner wants a preview or a couple more preference choices; use --continue-survey only if they choose to continue.' if preview_available else 'Answer a few core items first, or request a general explanation without personal workout doses.',
            'readiness':'not_assessed',
            'planning_note':'Selections and mileage bands are not exact training doses. Dates, per-day time differences, skipped limitations and conflicts may need a short targeted follow-up. No pace or method is inferred by this script.'}
