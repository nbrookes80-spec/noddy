"""Dyno and drag simulation for the Android app. No Kivy here, so it can be tested on a desktop.

Two sources of torque curve:

- a dyno CSV you load (rpm, hp, tq), read by the same loader as the desktop app;
- a simulated curve built from the saved parameters, used until a CSV is loaded.

The simulated curve is an estimate shaped from peak power and the shift RPM. It is not a
measurement. Each run uses the shift settings from the Shift Points screen, so changing a ratio,
weight or tire size updates the simulated run straight away.
"""

from tunertoolpro import core
from tunertoolpro.engines.torque_curve import TorqueCurve

import shift_live

SAMPLE_COUNT = 120


def simulated_curve(rwhp, shift_rpm, idle_rpm):
    """Estimate a power curve from the peak power and the shift RPM.

    The shape is set on torque first: torque peaks at about 62% of shift RPM and falls off either
    side. Horsepower follows from torque (hp = tq * rpm / 5252). The curve is then scaled so its
    peak horsepower equals the RWHP entered, which lands at about 89% of shift RPM.
    """
    torque_peak_rpm = 0.62 * shift_rpm
    width = 0.5 * shift_rpm
    top_rpm = 1.1 * shift_rpm
    rpms = [idle_rpm + (top_rpm - idle_rpm) * i / SAMPLE_COUNT for i in range(SAMPLE_COUNT + 1)]
    shape = [max(0.5, 1.0 - 0.45 * ((rpm - torque_peak_rpm) / width) ** 2) for rpm in rpms]
    peak_hp_shape = max(t * r / 5252.0 for t, r in zip(shape, rpms))
    scale = rwhp / peak_hp_shape if peak_hp_shape > 0 else 0.0
    points = []
    for rpm, t in zip(rpms, shape):
        tq = scale * t
        points.append((rpm, tq * rpm / 5252.0, tq))
    return TorqueCurve(points)


def load_curve(path):
    """Read a dyno CSV (rpm, hp, tq). Raises ValueError or OSError with a message the user can act on."""
    return core.load_dyno(path)


def run(values, ratios_text, curve, lead_mode='rpm', stall_lock=False):
    """Simulate a launch to the quarter mile with the shift settings and the curve.

    Returns (result, error). result is the simulator's dict; error is '' when it ran.
    """
    try:
        cfg = shift_live.build_cfg(values, ratios_text, lead_mode, stall_lock)
    except (ValueError, KeyError) as exc:
        return None, str(exc)
    try:
        result = core.run_drag(cfg, curve)
    except (ValueError, ZeroDivisionError, KeyError) as exc:
        return None, f'The simulation could not run: {exc}'
    if result is None:
        return None, 'The simulation needs a torque curve.'
    return result, ''


def chart_series(curve, samples=SAMPLE_COUNT):
    """(rpms, hp, tq) sampled evenly across the curve's RPM range, for drawing."""
    if curve is None or curve.is_empty:
        return [], [], []
    lo, hi = curve.rpm_range
    rpms = [lo + (hi - lo) * i / samples for i in range(samples + 1)]
    return rpms, [curve.hp_at(r) for r in rpms], [curve.tq_at(r) for r in rpms]


def summary_rows(curve):
    """Peak numbers and RPM range as (label, text) pairs."""
    return [(label, str(value)) for label, value in core.dyno_summary(curve)]


def result_rows(result):
    """The drag results as (label, text) pairs, in the same order as the desktop tab."""
    def fmt(value):
        return '—' if value is None else f'{value:.2f}'

    return [
        ('0-30 mph (s)', fmt(result.get('t_0_30'))),
        ('0-60 mph (s)', fmt(result.get('t_0_60'))),
        ('0-100 mph (s)', fmt(result.get('t_0_100'))),
        ('1/8 mile (s)', fmt(result.get('t_eighth'))),
        ('1/8 mile speed (mph)', fmt(result.get('v_eighth'))),
        ('1/4 mile (s)', fmt(result.get('t_quarter'))),
        ('1/4 mile speed (mph)', fmt(result.get('v_quarter'))),
        ('Top speed in run (mph)', fmt(result.get('max_v'))),
    ]
