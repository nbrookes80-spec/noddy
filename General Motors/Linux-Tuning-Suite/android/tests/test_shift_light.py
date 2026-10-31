import json
import sys
import tempfile
import unittest
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import prefs  # noqa: E402
from scanner import shift_light  # noqa: E402

SETTINGS = {'start': 2000, 'shift': 6500, 'margin': 300, 'style': 'bar', 'theme': 'classic', 'chime': True}


class LitTests(unittest.TestCase):
    def test_the_fill_runs_from_the_start_rpm_to_the_shift_rpm(self):
        self.assertEqual(shift_light.fraction(2000, 2000, 6500), 0.0)
        self.assertEqual(shift_light.fraction(6500, 2000, 6500), 1.0)
        self.assertEqual(shift_light.fraction(1000, 2000, 6500), 0.0)
        self.assertEqual(shift_light.fraction(9000, 2000, 6500), 1.0)
        self.assertEqual(shift_light.fraction(None, 2000, 6500), 0.0)

    def test_one_led_per_tenth_of_the_way(self):
        self.assertEqual([shift_light.lit_count(p) for p in (0, 0.09, 0.1, 0.55, 0.99, 1.0)], [0, 0, 1, 5, 9, 10])

    def test_the_zones_are_five_low_three_middle_two_high(self):
        self.assertEqual([shift_light.zone_of_rank(r) for r in range(10)], ['low'] * 5 + ['mid'] * 3 + ['high'] * 2)

    def test_the_strip_changes_colour_at_half_and_eighty_per_cent(self):
        self.assertEqual([shift_light.zone_of_fraction(p) for p in (0.49, 0.5, 0.79, 0.8)],
                         ['low', 'mid', 'mid', 'high'])

    def test_the_phases(self):
        self.assertEqual(shift_light.phase_of(5000, 6500, 300), 'off')
        self.assertEqual(shift_light.phase_of(6200, 6500, 300), 'warning')
        self.assertEqual(shift_light.phase_of(6500, 6500, 300), 'shift')
        self.assertEqual(shift_light.phase_of(None, 6500, 300), 'off')


class FrameTests(unittest.TestCase):
    def test_the_bar_lights_from_the_left(self):
        zones, _part, phase = shift_light.frame(5300, SETTINGS, now=0.0)   # 7 of 10 lit, not yet in the warning
        self.assertEqual(zones, ('low',) * 5 + ('mid', 'mid', None, None, None))
        self.assertEqual(phase, 'off')

    def test_the_centre_style_lights_from_the_middle_out(self):
        zones, _part, _phase = shift_light.frame(2450, dict(SETTINGS, style='centre'), now=0.0)
        self.assertEqual(zones, (None, None, None, None, 'low', None, None, None, None, None))

    def test_the_outside_style_lights_from_both_edges_in(self):
        zones, _part, _phase = shift_light.frame(2450, dict(SETTINGS, style='outside'), now=0.0)
        self.assertEqual(zones[0], 'low')                                  # one LED: the left edge
        zones, _part, _phase = shift_light.frame(2900, dict(SETTINGS, style='outside'), now=0.0)   # two LEDs
        self.assertEqual(zones, ('low', None, None, None, None, None, None, None, None, 'low'))

    def test_the_strip_takes_one_colour_from_how_far_up_it_is(self):
        zones, _part, _phase = shift_light.frame(6000, dict(SETTINGS, style='strip'), now=0.0)
        lit = [z for z in zones if z]
        self.assertEqual((len(lit), set(lit)), (8, {'high'}))

    def test_the_warning_blinks_the_lit_leds(self):
        on, _part, phase = shift_light.frame(6300, SETTINGS, now=0.0)
        off, _part, _phase = shift_light.frame(6300, SETTINGS, now=0.15)
        self.assertEqual(phase, 'warning')
        self.assertEqual(sum(1 for z in on if z), 9)
        self.assertEqual(off, (None,) * 10)

    def test_the_shift_point_flashes_every_led(self):
        self.assertEqual(shift_light.frame(6500, SETTINGS, now=0.0)[0], ('high',) * 10)
        self.assertEqual(shift_light.frame(6500, SETTINGS, now=0.10)[0], (None,) * 10)

    def test_no_engine_speed_means_no_leds(self):
        self.assertEqual(shift_light.frame(None, SETTINGS, now=0.0), ((None,) * 10, 0.0, 'off'))


class ChimeTests(unittest.TestCase):
    def test_a_chime_is_due_at_once_then_every_0_3_seconds_while_active(self):
        timer = shift_light.ChimeTimer()
        due = [timer.due(True, t) for t in (0.0, 0.1, 0.29, 0.31, 0.45, 0.65)]
        self.assertEqual(due, [True, False, False, True, False, True])

    def test_leaving_the_warning_means_the_next_one_chimes_at_once(self):
        timer = shift_light.ChimeTimer()
        timer.due(True, 0.0)
        self.assertFalse(timer.due(False, 0.1))
        self.assertTrue(timer.due(True, 0.15))

    def test_the_chime_file_is_a_mono_120_ms_tone_at_22050_hz(self):
        path = Path(tempfile.mkdtemp()) / 'chime.wav'
        shift_light.write_chime(str(path))
        with wave.open(str(path)) as sound:
            self.assertEqual((sound.getframerate(), sound.getnchannels(), sound.getsampwidth()), (22050, 1, 2))
            self.assertEqual(sound.getnframes(), int(22050 * 0.12))

    def test_the_tone_peaks_at_the_built_in_level(self):
        samples = shift_light.chime_samples()
        self.assertLessEqual(max(samples), int(0.8 * 32767) + 1)
        self.assertGreater(max(samples), 25000)


class SettingsTests(unittest.TestCase):
    def test_no_settings_gives_the_defaults(self):
        self.assertEqual(shift_light.clean(None), shift_light.DEFAULTS)

    def test_values_are_kept_inside_their_ranges(self):
        got = shift_light.clean({'start': 9999, 'shift': 100, 'margin': 5})
        self.assertEqual((got['shift'], got['start'], got['margin']), (3000, 2500, 100))

    def test_the_start_moves_down_to_keep_a_gap_before_the_shift(self):
        got = shift_light.clean({'start': 6000, 'shift': 6200})
        self.assertEqual((got['start'], got['shift']), (5700, 6200))

    def test_bad_choices_fall_back_to_the_defaults(self):
        got = shift_light.clean({'style': 'disco', 'theme': None, 'chime': 'yes', 'start': True})
        self.assertEqual((got['style'], got['theme'], got['chime'], got['start']), ('bar', 'classic', True, 2000))


class PrefsTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / 'prefs.json'

    def test_a_new_install_has_the_light_off_with_the_defaults(self):
        loaded = prefs.load(self.path)
        self.assertFalse(loaded['light_on'])
        self.assertEqual((loaded['light_start'], loaded['light_shift'], loaded['light_margin']), (2000, 6500, 300))

    def test_the_choices_survive_a_save_and_load(self):
        choices = dict(prefs.DEFAULTS, light_on=True, light_style='strip', light_theme='ice', light_start=2500,
                       light_chime=False)
        prefs.save(self.path, choices)
        loaded = prefs.load(self.path)
        self.assertEqual((loaded['light_on'], loaded['light_style'], loaded['light_theme'], loaded['light_start'],
                          loaded['light_chime']), (True, 'strip', 'ice', 2500, False))

    def test_damaged_light_choices_fall_back_or_are_pulled_into_range(self):
        self.path.write_text(json.dumps({'light_style': 'x', 'light_shift': 1, 'light_on': 'yes'}))
        loaded = prefs.load(self.path)
        self.assertEqual((loaded['light_on'], loaded['light_style'], loaded['light_shift']), (False, 'bar', 3000))


if __name__ == '__main__':
    unittest.main()
