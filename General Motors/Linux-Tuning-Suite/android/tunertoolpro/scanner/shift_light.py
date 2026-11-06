"""The shift light: ten LEDs that fill as the engine speed climbs to the shift point. No Kivy, no I/O.

The LEDs fill from the start RPM to the shift RPM. The lit ones take the colour of their zone: the first five are
the low zone, the next three the middle and the last two the high zone. Inside the warning window before the shift
the lit LEDs blink, and at the shift point every LED flashes. A chime sounds while either is happening.

Ported from the Torque Pro shift light plugin, whose rules these are. The colours in THEMES are close to the
plugin's four themes, not copied from it.
"""

import math
import struct
import wave

LEDS = 10
LOW_ZONE_LAST = 4          # LEDs 0 to 4 (the first five) are the low zone
MID_ZONE_LAST = 7          # LEDs 5 to 7 are the middle zone, 8 and 9 the high zone
WARNING_BLINK = 0.15       # seconds per half blink inside the warning window
SHIFT_FLASH = 0.10         # seconds per half flash at the shift point
CHIME_EVERY = 0.30         # seconds between chimes while the warning or the shift is on
STRIP_MID, STRIP_HIGH = 0.5, 0.8   # the strip changes colour at these fractions of the way to the shift point

STYLES = ('bar', 'centre', 'outside', 'strip')
STYLE_NAMES = {'bar': 'Bar', 'centre': 'Centre out', 'outside': 'Outside in', 'strip': 'Strip'}
# The order the LEDs light, as physical positions left to right. Rank 0 is the first LED to light.
ORDER = {'bar': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
         'centre': [4, 5, 3, 6, 2, 7, 1, 8, 0, 9],
         'outside': [0, 9, 1, 8, 2, 7, 3, 6, 4, 5],
         'strip': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}

OFF = (0.18, 0.20, 0.24, 1)
THEMES = {
    'classic': {'name': 'Classic', 'low': (0.20, 0.85, 0.30, 1), 'mid': (1.00, 0.85, 0.15, 1),
                'high': (1.00, 0.20, 0.20, 1)},
    'neon': {'name': 'Neon', 'low': (0.25, 1.00, 0.85, 1), 'mid': (0.55, 0.45, 1.00, 1),
             'high': (1.00, 0.25, 0.75, 1)},
    'race': {'name': 'Race', 'low': (0.95, 0.95, 0.95, 1), 'mid': (1.00, 0.55, 0.10, 1),
             'high': (0.95, 0.10, 0.10, 1)},
    'ice': {'name': 'Ice', 'low': (0.55, 0.85, 1.00, 1), 'mid': (0.75, 0.95, 1.00, 1),
            'high': (1.00, 1.00, 1.00, 1)},
}

# The saved settings. The plugin's ranges: start 1000-6000, shift 3000-7000, warning 100-1000, steps of 100.
DEFAULTS = {'start': 2000, 'shift': 6500, 'margin': 300, 'style': 'bar', 'theme': 'classic', 'chime': True,
            'position': 'top', 'size': 'medium'}
LIMITS = {'start': (1000, 6000), 'shift': (3000, 7000), 'margin': (100, 1000)}
STEP = 100
MIN_GAP = 500              # the shift RPM is at least this far above the start RPM

# The bar the LEDs sit in, over every screen of the app: at the top or the bottom, in one of three heights (dp).
POSITIONS = ('top', 'bottom')
SIZES = ('small', 'medium', 'large')
SIZE_NAMES = {'small': 'Small', 'medium': 'Medium', 'large': 'Large'}
BAR_HEIGHTS = {'small': 22, 'medium': 32, 'large': 46}
MIN_BAR_WIDTH = 160        # dp: narrower than this beside the full-screen buttons, the bar goes under them

# The screens of the Android app. Only Scan polls the adapter itself; every other one leaves it to the Live reader.
SCREENS = ('shift', 'dyno', 'live', 'scan', 'link', 'sniff', 'agent', 'settings')
SELF_POLLING = ('scan',)
RPM_PID = '010C'
NOTE_NOT_READ = 'RPM not read on this screen'
NOTE_ADAPTER_HELD = 'RPM paused: the sniffer has the adapter'

# The chime: a short 1 kHz sine, like the plugin's built-in beep.
CHIME_RATE = 22050
CHIME_SECONDS = 0.12
CHIME_HZ = 1000
CHIME_LEVEL = 0.8

def clean(settings):
    """The settings with every value inside its range, the style and theme known, and the shift point at least
    MIN_GAP above the start. Anything missing or wrong falls back to the default."""
    out = dict(DEFAULTS)
    if isinstance(settings, dict):
        for key, (low, high) in LIMITS.items():
            value = settings.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
                out[key] = min(high, max(low, int(round(value))))
        if settings.get('style') in STYLES:
            out['style'] = settings['style']
        if settings.get('theme') in THEMES:
            out['theme'] = settings['theme']
        if isinstance(settings.get('chime'), bool):
            out['chime'] = settings['chime']
        if isinstance(settings.get('position'), str) and settings['position'] in POSITIONS:
            out['position'] = settings['position']
        if isinstance(settings.get('size'), str) and settings['size'] in SIZES:
            out['size'] = settings['size']
    if out['shift'] - out['start'] < MIN_GAP:
        out['start'] = out['shift'] - MIN_GAP   # the start moves down, never the shift point
    return out


def bar_height(size):
    """The bar's height in dp for a size choice. An unknown size gets the medium height."""
    return BAR_HEIGHTS.get(size if isinstance(size, str) else None, BAR_HEIGHTS['medium'])


def other_position(position):
    """Where a long press on the bar moves it: top to bottom and back. An unknown place reads as the top."""
    return 'top' if position == 'bottom' else 'bottom'


def bar_insets(position, fullscreen, mirrored, reserved):
    """(left, right) space in dp the bar leaves empty so the full-screen Record, HUD and Exit buttons stay clear.

    Those buttons float over the top right corner, outside the HUD mirror. The bar sits inside the mirror, so while
    the picture is mirrored its gap goes on the left: flipped, that lands under the buttons. Only a top bar in full
    screen needs a gap; elsewhere the header or nothing is there.
    """
    if position != 'top' or not fullscreen:
        return 0, 0
    return (reserved, 0) if mirrored else (0, reserved)


def bar_gaps(position, fullscreen, mirrored, width, reserved, below):
    """(left, right, top) space in dp around the bar, so it never covers the full-screen buttons.

    `width` is the screen width, `reserved` the width the buttons take at the top right and `below` their height.
    Beside the buttons when that leaves the bar at least MIN_BAR_WIDTH (see bar_insets); on a narrow screen the bar
    keeps its full width and sits under the buttons instead.
    """
    left, right = bar_insets(position, fullscreen, mirrored, reserved)
    if left == right == 0:
        return 0, 0, 0
    if width - reserved >= MIN_BAR_WIDTH:
        return left, right, 0
    return 0, 0, below


def rpm_source(screen, holds_adapter, light_on, scan_reads_rpm=False):
    """Where the shift light gets engine speed on this screen: 'live', 'scan' or 'none'.

    The rule keeps one conversation with the adapter at a time:
    - 'live': the Live StreamRunner keeps reading on this screen, and the light uses its latest '010C'.
    - 'scan': the Scan screen polls the adapter on its own thread, so the Live reader stands aside; the light uses
      Scan's own readings, but only if Scan is reading '010C'.
    - 'none': no reading for the light. That is the case with the light off, while another part holds the adapter
      (`holds_adapter`: the sniffer listening, starting or running its car check), on Scan when Scan does not read
      RPM, and on any screen not in SCREENS, since a screen this rule does not know may use the adapter itself.
    The Elm327 lock also keeps each command whole; this rule decides who may start talking at all.
    """
    if not light_on or holds_adapter or screen not in SCREENS:
        return 'none'
    if screen in SELF_POLLING:
        return 'scan' if scan_reads_rpm else 'none'
    return 'live'


def runner_runs(screen, holds_adapter, light_on):
    """True when the Live StreamRunner may read the adapter: on the Live screen as always, and on the other screens
    the rule above gives to it while the shift light is on. Never while another part holds the adapter, and never
    on Scan or an unknown screen, whose own polling would otherwise run beside it."""
    if holds_adapter or screen not in SCREENS or screen in SELF_POLLING:
        return False
    return screen == 'live' or rpm_source(screen, holds_adapter, light_on) == 'live'


def rpm_note(screen, holds_adapter, light_on, scan_reads_rpm=False):
    """The short reason shown on a dimmed bar, or '' when the light has a reading source (or is off)."""
    if not light_on or rpm_source(screen, holds_adapter, light_on, scan_reads_rpm) != 'none':
        return ''
    return NOTE_ADAPTER_HELD if holds_adapter else NOTE_NOT_READ


def fraction(rpm, start, shift):
    """How far the engine is from the start RPM to the shift RPM, from 0 to 1. None reads as 0."""
    if rpm is None:
        return 0.0
    return min(1.0, max(0.0, (rpm - start) / (shift - start)))


def lit_count(part):
    """How many of the ten LEDs are lit for a fraction of the way to the shift point."""
    return min(LEDS, int(part * LEDS))


def zone_of_rank(rank):
    """The zone of the LED that lights at this rank: the first five low, the next three middle, the last two high."""
    if rank <= LOW_ZONE_LAST:
        return 'low'
    return 'mid' if rank <= MID_ZONE_LAST else 'high'


def zone_of_fraction(part):
    """The strip's colour: low below half way, middle to 80 per cent, high after that."""
    if part < STRIP_MID:
        return 'low'
    return 'mid' if part < STRIP_HIGH else 'high'


def phase_of(rpm, shift, margin):
    """'shift' at or past the shift point, 'warning' inside the window before it, otherwise 'off'."""
    if rpm is None:
        return 'off'
    if rpm >= shift:
        return 'shift'
    return 'warning' if rpm >= shift - margin else 'off'


def frame(rpm, settings, now):
    """What the LEDs show for this RPM at time `now` (seconds, any steady clock).

    Returns (zones, fraction, phase). zones lists the LEDs left to right, so the widget does not need the style.
    """
    s = clean(settings)
    part = fraction(rpm, s['start'], s['shift'])
    phase = phase_of(rpm, s['shift'], s['margin'])
    zones = [None] * LEDS
    for rank in range(lit_count(part)):
        zones[ORDER[s['style']][rank]] = zone_of_fraction(part) if s['style'] == 'strip' else zone_of_rank(rank)
    if phase == 'shift':
        zones = ['high' if int(now / SHIFT_FLASH) % 2 == 0 else None] * LEDS
    elif phase == 'warning' and int(now / WARNING_BLINK) % 2 == 1:
        zones = [None] * LEDS
    return tuple(zones), part, phase


class ChimeTimer:
    """Says when a chime is due: at once when the warning starts, then every CHIME_EVERY seconds while it lasts."""

    def __init__(self):
        self._last = None

    def due(self, active, now):
        if not active:
            self._last = None
            return False
        if self._last is None or now - self._last >= CHIME_EVERY:
            self._last = now
            return True
        return False


def chime_samples():
    """One chime as 16-bit mono samples."""
    count = int(CHIME_RATE * CHIME_SECONDS)
    return [int(CHIME_LEVEL * 32767 * math.sin(2 * math.pi * CHIME_HZ * i / CHIME_RATE)) for i in range(count)]


def write_chime(path):
    """Write the chime as a WAV file, so the phone's audio player can play it."""
    samples = chime_samples()
    with wave.open(path, 'wb') as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(CHIME_RATE)
        out.writeframes(struct.pack(f'<{len(samples)}h', *samples))
