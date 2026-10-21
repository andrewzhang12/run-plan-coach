"""Synthetic planning checks; no fitness, injury-risk, or recovery prediction.

All units are explicit. Intervals use aware ISO timestamps and half-open bounds.
Clinical/load judgements are review items, never machine safety passes.
"""
from datetime import datetime, timedelta
from math import isfinite, isclose


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value) and value >= 0


def moment(value):
    dt = datetime.fromisoformat(value)
    if dt.utcoffset() is None:
        raise ValueError('timezone required')
    return dt


def validate(plan):
    findings = []
    def add(kind, code, detail):
        findings.append(dict(kind=kind, code=code, detail=detail))
    if not plan.get('sessions'):
        add('unknown', 'sessions_missing', 'No sessions to validate.')
    if not plan.get('windows'):
        add('unknown', 'windows_missing', 'No planning windows or targets to reconcile.')
    sessions, ids, sources = [], set(), set()
    for s in plan.get('sessions', []):
        sid = s.get('id')
        if not sid or sid in ids:
            add('error', 'session_id', str(sid))
        ids.add(sid)
        source = s.get('source_id')
        if source and source in sources:
            add('error', 'duplicate_source', source)
        if source:
            sources.add(source)
        try:
            start, end = moment(s['start']), moment(s['end'])
            if end <= start:
                raise ValueError('nonpositive duration')
        except (KeyError, TypeError, ValueError) as exc:
            add('error', 'session_time', f'{sid}: {exc}')
            continue
        if s.get('state') not in ('planned', 'actual'):
            add('error', 'session_state', str(sid))
        if not s.get('purpose'):
            add('unknown', 'purpose_missing', str(sid))
        components = s.get('components')
        if not components:
            add('unknown', 'dose_missing', str(sid))
            km = None
        elif any(not number(c.get('km')) for c in components):
            add('error', 'distance_invalid', str(sid))
            km = None
        else:
            km = sum(c['km'] for c in components)
        if s.get('effort') in ('threshold', 'interval', 'repetition', 'marathon'):
            if s.get('pace_basis') != 'current_evidence':
                add('unknown', 'pace_evidence', str(sid))
            if not s.get('recovery_review'):
                add('review', 'recovery_unreviewed', str(sid))
            reps = s.get('reps', 1)
            if not isinstance(reps, int) or isinstance(reps, bool) or reps < 1:
                add('error', 'reps_invalid', str(sid))
            elif reps > 1 and s.get('recovery_seconds') is None:
                add('unknown', 'rep_recovery_missing', str(sid))
            if s.get('recovery_seconds') is not None and not number(s['recovery_seconds']):
                add('error', 'recovery_invalid', str(sid))
        if s.get('effort') != 'easy' and s.get('purpose') == 'participation':
            add('review', 'participation_effort', str(sid))
        if not s.get('constraint_review'):
            add('review', 'constraints_unreviewed', str(sid))
        sessions.append((s, start, end, km))
    mode = plan.get('mode', 'planned')
    if mode not in ('planned', 'actual'):
        add('error', 'mode_invalid', str(mode))
    selected = [x for x in sessions if x[0].get('state') == mode]
    ordered = sorted(selected, key=lambda x: x[1])
    for i, a in enumerate(ordered):
        for b in ordered[i+1:]:
            if b[1] >= a[2]:
                break
            add('error', 'session_overlap', f'{a[0]["id"]}/{b[0]["id"]}')
    slots = []
    for slot in plan.get('availability', []):
        try:
            start, end = moment(slot['start']), moment(slot['end'])
            if end <= start:
                raise ValueError('nonpositive slot')
            slots.append((start, end))
        except (KeyError, TypeError, ValueError):
            add('error', 'availability_invalid', str(slot))
    if mode == 'planned':
        for s, start, end, _ in selected:
            if not slots:
                add('unknown', 'availability_missing', str(s['id']))
            elif not any(a <= start and end <= b for a, b in slots):
                add('error', 'outside_availability', str(s['id']))
    summaries = []
    for w in plan.get('windows', []):
        try:
            start, end = moment(w['start']), moment(w['end'])
            if end <= start:
                raise ValueError('nonpositive window')
        except (KeyError, TypeError, ValueError):
            add('error', 'window_invalid', str(w))
            continue
        # Attribute whole sessions to their start; flag straddling windows explicitly.
        rows = [x for x in selected if start <= x[1] < end]
        required = [x for x in rows if not x[0].get('optional', False)]
        if any(x[2] > end for x in rows):
            add('review', 'window_straddle', str(w.get('id')))
        total = None if any(x[3] is None for x in required) else sum(x[3] for x in required)
        optional = None if any(x[3] is None for x in rows) else sum(x[3] for x in rows if x[0].get('optional', False))
        target = w.get('target_km')
        if target is not None:
            if not isinstance(target, (list, tuple)) or len(target) != 2 or not all(number(t) for t in target) or target[0] > target[1]:
                add('error', 'target_invalid', str(w.get('id')))
            elif total is None:
                add('unknown', 'weekly_distance_unknown', str(w.get('id')))
            elif not ((total >= target[0] or isclose(total, target[0], abs_tol=1e-9, rel_tol=0)) and (total <= target[1] or isclose(total, target[1], abs_tol=1e-9, rel_tol=0))):
                add('review', 'target_mismatch', f'{w.get("id")}: {total} vs {target}')
        summaries.append(dict(id=w.get('id'), required_km=total, optional_km=optional,
                              scheduled_minutes=sum((x[2]-x[1]).total_seconds()/60 for x in required)))
    # Display elapsed gaps across week boundaries. No universal safe-gap threshold.
    substantial = [x for x in ordered if x[0].get('substantial')]
    gaps = [dict(before=a[0]['id'], after=b[0]['id'],
                 hours=(b[1]-a[2]).total_seconds()/3600)
            for a, b in zip(substantial, substantial[1:])]
    if not plan.get('history_review'):
        add('unknown', 'history_unreviewed', 'No inference of load tolerance from missing history.')
    if not plan.get('goal_review'):
        add('review', 'goals_unreviewed', 'Priorities and tradeoffs require review.')
    status = 'infeasible_or_invalid' if any(f['kind']=='error' for f in findings) else 'needs_review' if findings else 'structurally_consistent'
    return dict(status=status, findings=findings, windows=summaries, substantial_gaps=gaps,
                physiological_validation='not_assessed')
