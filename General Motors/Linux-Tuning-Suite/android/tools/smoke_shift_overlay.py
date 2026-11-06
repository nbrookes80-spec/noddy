"""Headless smoke test of the app-wide shift light bar. Needs Kivy; not part of the normal pytest run.

Run from the android/ folder:

    KIVY_NO_ARGS=1 SDL_VIDEODRIVER=dummy /home/nathan/TunerToolPro-Android/.venv/bin/python tools/smoke_shift_overlay.py

It builds the bar in a column like main.py's (header, screens, tabs), with a real StreamRunner on the demo drive,
then checks: the bar's place and size, that the Live reader runs or stands aside on every screen by the rule,
that RPM reaches the bar on a screen other than Live, that Scan's own readings are used on Scan, the dimmed bar
and its note, the gaps left for the full-screen buttons, taps and long presses, the Live card's settings, and
that the chime fires once per due frame with the Live screen not in front. Exits non-zero on the first failure.
"""

import os
import sys
import tempfile
import time

os.environ.setdefault('KIVY_NO_ARGS', '1')
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.metrics import dp  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.widget import Widget  # noqa: E402

import shift_overlay  # noqa: E402
from live_ui import LiveScreen, StreamRunner  # noqa: E402
from scan_ui import ScanScreen  # noqa: E402
from shift_overlay import DIM, ShiftOverlay  # noqa: E402
from tunertoolpro import prefs  # noqa: E402
from tunertoolpro.scanner import shift_light  # noqa: E402
from tunertoolpro.scanner.session import Session  # noqa: E402

SCREENS = ('shift', 'dyno', 'live', 'scan', 'link', 'sniff', 'agent', 'settings')


def check(condition, message):
    if not condition:
        print('FAIL:', message)
        sys.exit(1)
    print('ok  :', message)


class FakeTouch:
    """Enough of a Kivy touch for the bar: a position and the grab list."""

    def __init__(self, x, y):
        self.pos = (x, y)
        self.grab_list = []
        self.grab_current = None

    def grab(self, widget):
        self.grab_list.append(widget)

    def ungrab(self, widget):
        if widget in self.grab_list:
            self.grab_list.remove(widget)


class Clock_:
    """A clock the smoke moves by hand, so frames and chimes are counted exactly."""

    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


class FakeStream:
    def __init__(self):
        self.latest = {}


def main():
    folder = tempfile.mkdtemp()
    saved = prefs.load(os.path.join(folder, 'prefs.json'))
    saves = []
    state = {'screen': 'shift', 'holds': False, 'scan': (False, None), 'full': False, 'mirrored': False}
    opened = []

    session = Session()
    session.set_demo(True)
    runner = StreamRunner(session, lambda: (None, None))
    session.listeners.append(runner.source_changed)
    runner.source_changed()
    live = LiveScreen(session, runner)
    live.light.attach(saved, lambda: saves.append(dict(saved)), os.path.join(folder, 'chime.wav'))

    column = BoxLayout(orientation='vertical', size=(dp(400), dp(800)))
    header, screens, tabs = Widget(), Widget(), Widget()
    for widget in (header, screens, tabs):
        column.add_widget(widget)
    overlay = ShiftOverlay(saved, lambda: saves.append(dict(saved)), os.path.join(folder, 'chime.wav'), runner,
                           column, header, tabs, screen=lambda: state['screen'],
                           holds_adapter=lambda: state['holds'], scan_rpm=lambda: state['scan'],
                           fullscreen=lambda: state['full'], mirrored=lambda: state['mirrored'],
                           reserved=dp(274), below=dp(44), on_open=lambda: opened.append(True))
    live.light.on_change = overlay.tick

    # --- one owner: the Live screen no longer runs a light clock of its own -------------------------------
    check(not hasattr(live, 'tick_light') and not hasattr(live.light, 'update'),
          'the Live screen and its card have no shift light clock or chime of their own')
    check(not hasattr(live.light, 'strip'), 'the Live card carries the settings only, not a second LED strip')

    # --- light off ------------------------------------------------------------------------------------------
    overlay.tick(0)
    check(overlay.bar.parent is None, 'with the light off the bar is not on the screen')
    for screen in SCREENS:
        state['screen'] = screen
        overlay.apply_runner()
        check(runner.paused == (screen != 'live'), f'light off: the Live reader runs only on Live ({screen})')

    # --- light on, from the Live card -----------------------------------------------------------------------
    state['screen'] = 'shift'
    live.light.switch.state = 'down'
    check(saved['light_on'] is True and saves, 'the Live card switch turns the light on and saves it')
    check(overlay.bar.parent is column and column.children[-1] is overlay.bar,
          'the bar is the top row of the column, above the header, at once')
    check(overlay.bar.height == dp(shift_light.bar_height('medium')), 'a new install has the medium bar')
    for screen in SCREENS:
        for holds in (False, True):
            state['screen'], state['holds'] = screen, holds
            overlay.apply_runner()
            want = shift_light.runner_runs(screen, holds, True)
            check(runner.paused == (not want), f'light on: Live reader {"runs" if want else "stands aside"} '
                                               f'on {screen}{" (sniffer has the adapter)" if holds else ""}')
    state['holds'] = False

    # --- RPM reaches the bar on a screen other than Live, from the real reader on the demo drive ----------------
    state['screen'] = 'dyno'
    overlay.apply_runner()
    check(not runner.paused, 'on Dyno with the light on the Live reader runs')
    runner.start()
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline and '010C' not in runner.stream.latest:
        time.sleep(0.1)
    check('010C' in runner.stream.latest, 'the Live reader read RPM while Dyno was in front')
    source, rpm, note = overlay.reading()
    check(source == 'live' and rpm == runner.stream.latest['010C'][0] and note == '',
          f'the bar takes that RPM on Dyno ({rpm:.0f} rpm)')
    state['screen'] = 'scan'
    overlay.apply_runner()
    check(runner.paused and runner.wait_idle(5), 'on Scan the reader stands aside and finishes its round first')
    runner.stop()

    # --- Scan's own readings, and the dimmed bar ---------------------------------------------------------------
    state['scan'] = (True, 5100.0)
    check(overlay.reading() == ('scan', 5100.0, ''), 'on Scan the bar takes Scan\'s own RPM when Scan reads it')
    state['scan'] = (False, None)
    overlay.tick(0)
    check(overlay.bar.note.text == 'RPM not read on this screen' and overlay.bar.strip.opacity == DIM,
          'on Scan without RPM the bar stays, dimmed, with a short reason')
    check(all(zone is None for zone in overlay.bar.strip._zones), 'and its LEDs are off')
    state['screen'], state['holds'] = 'live', True
    overlay.tick(0)
    check(overlay.bar.note.text == shift_light.NOTE_ADAPTER_HELD and runner.paused,
          'while the sniffer has the adapter the bar is dimmed with its reason, even on Live')
    state['holds'] = False
    overlay.tick(0)
    check(overlay.bar.note.text == '' and overlay.bar.strip.opacity == 1, 'given back, the bar lights again')

    scan = ScanScreen(session)
    reads, value = scan.rpm_reading()
    want = any(card.pid.pid == '010C' for card in scan.cards)
    check(reads == want and value is None, f'ScanScreen.rpm_reading follows the page shown (reads 010C: {reads})')
    if not reads:                               # this demo page has no RPM card: give it one, as a page with RPM would
        class RpmCard:
            pid = type('Pid', (), {'pid': '010C'})()

            def show(self, *_args, **_kwargs):
                pass
        scan.cards.append(RpmCard())
    scan._show({'010C': (4321.0, 'rpm')}, {})
    check(scan.rpm_reading() == (True, 4321.0), 'with an RPM card on the page it gives the RPM of its last poll')
    scan.set_view('Codes')
    check(scan.rpm_reading() == (False, None), 'on the Codes view Scan reads no RPM')

    # --- the chime: once per due frame, with Live not in front ---------------------------------------------------
    state['screen'] = 'shift'
    clock = Clock_()
    shift_overlay.time.monotonic = clock
    fake = FakeStream()
    runner.stream = fake
    reference = shift_light.ChimeTimer()
    settings = shift_light.clean({key: saved.get(f'light_{key}') for key in shift_light.DEFAULTS})
    expected = 0
    overlay.chimes = 0
    for step in range(60):                      # 6 s of frames: below the window, inside it, at the shift, past it
        rpm = 5000 + step * 50
        fake.latest = {'010C': (rpm, 'rpm')}
        clock.now += shift_overlay.LIGHT_TICK
        before = overlay.chimes
        overlay.tick(shift_overlay.LIGHT_TICK)
        _zones, _part, phase = shift_light.frame(rpm, settings, clock.now)
        due = reference.due(phase != 'off' and settings['chime'], clock.now)
        expected += due
        if overlay.chimes - before != (1 if due else 0):
            check(False, f'frame {step}: chimes {overlay.chimes - before}, due {due}')
    check(expected > 5 and overlay.chimes == expected,
          f'the chime fired once per due frame on the Shift screen ({overlay.chimes} chimes in 60 frames)')
    live.light.chime_switch.state = 'normal'
    overlay.chimes = 0
    fake.latest = {'010C': (7000, 'rpm')}
    for _ in range(10):
        clock.now += shift_overlay.LIGHT_TICK
        overlay.tick(shift_overlay.LIGHT_TICK)
    check(overlay.chimes == 0, 'with the chime switched off on the Live card the bar stays silent')
    live.light.chime_switch.state = 'down'

    # --- the flash timing is unchanged -------------------------------------------------------------------------
    fake.latest = {'010C': (7000, 'rpm')}
    lit = []
    for _ in range(4):
        clock.now = round(clock.now / shift_light.SHIFT_FLASH) * shift_light.SHIFT_FLASH + 0.01
        overlay.tick(0)
        lit.append(any(overlay.bar.strip._zones))
        clock.now += shift_light.SHIFT_FLASH
    check(lit in ([True, False, True, False], [False, True, False, True]),
          'at the shift point the LEDs flash every 0.10 s, ticked every LIGHT_TICK = 0.1 s')

    # --- size, position and the full-screen buttons -------------------------------------------------------------
    live.light.size_button.dispatch('on_release')
    check(saved['light_size'] == 'large' and overlay.bar.height == dp(shift_light.bar_height('large')),
          'the Live card size button makes the bar large, at once')
    live.light.position_button.dispatch('on_release')
    check(saved['light_position'] == 'bottom' and column.children[1] is overlay.bar and column.children[0] is tabs,
          'the Live card position button puts the bar at the bottom, just above the tabs')
    live.light.position_button.dispatch('on_release')
    column.width = dp(800)                      # a phone on its side: room for the bar beside the buttons
    state['full'] = True
    overlay.place()
    check(overlay.bar.right_gap == dp(274) and overlay.bar.left_gap == 0,
          'full screen, wide: the bar leaves the right corner free for Record, HUD and Exit')
    state['mirrored'] = True
    overlay.place()
    check(overlay.bar.left_gap == dp(274) and overlay.bar.right_gap == 0,
          'HUD mirrored: the gap is on the left, which the mirror puts under the buttons')
    column.width = dp(360)
    overlay.place()
    check(overlay.bar.top_gap == dp(44) and overlay.bar.left_gap == overlay.bar.right_gap == 0,
          'full screen, narrow: the bar keeps its width and sits under the buttons')
    column.width = dp(400)
    state['full'] = state['mirrored'] = False
    overlay.place()
    check(overlay.bar.left_gap == overlay.bar.right_gap == overlay.bar.top_gap == 0, 'out of full screen: no gaps')

    # --- touches -------------------------------------------------------------------------------------------------
    column.do_layout()
    bar = overlay.bar
    inside = FakeTouch(bar.x + bar.width / 2, bar.y + bar.height / 2)
    check(bar.on_touch_down(inside) is True, 'a touch on the bar is taken by the bar')
    inside.grab_current = bar
    bar.on_touch_up(inside)
    check(opened == [True], 'a tap on the bar opens the shift light settings')
    outside = FakeTouch(bar.x + bar.width / 2, bar.y - dp(20))
    check(bar.on_touch_down(outside) is False, 'a touch below the bar is left for the screen')
    state['full'] = True
    column.width = dp(800)
    overlay.place()
    column.do_layout()
    corner = FakeTouch(bar.right - dp(10), bar.y + bar.height / 2)
    check(bar.on_touch_down(corner) is False, 'in full screen, wide, a touch in the buttons\' corner is not taken')
    column.width = dp(400)
    overlay.place()
    column.do_layout()
    above = FakeTouch(bar.right - dp(10), bar.top - dp(10))
    check(bar.on_touch_down(above) is False, 'in full screen, narrow, a touch in the space under the buttons is not '
                                              'taken')
    state['full'] = False
    overlay.place()
    column.do_layout()
    before = saved['light_position']
    press = FakeTouch(bar.x + bar.width / 2, bar.y + bar.height / 2)
    bar.on_touch_down(press)
    bar._long_press(0)
    press.grab_current = bar
    bar.on_touch_up(press)
    check(saved['light_position'] == shift_light.other_position(before) and saves[-1]['light_position']
          == saved['light_position'], 'a long press moves the bar to the other end and saves it')
    check(opened == [True], 'and does not count as a tap')
    live.light.refresh()
    check(live.light.position_button.text == f'Bar: {saved["light_position"].capitalize()}',
          'the Live card shows where the bar went')

    # --- off again ---------------------------------------------------------------------------------------------
    live.light.switch.state = 'normal'
    check(overlay.bar.parent is None, 'switched off on the Live card, the bar leaves the screen at once')
    shift_overlay.time.monotonic = time.monotonic
    app_check()
    print('shift overlay smoke passed')


def app_check():
    """The same bar inside the whole app, built the way the phone builds it."""
    import main as app_main
    app = app_main.TunerToolProApp()
    data = tempfile.mkdtemp()
    type(app).user_data_dir = property(lambda self: data)
    app.build()
    check(app.overlay.bar.parent is None and app.runner.paused, 'app: starts on Shift with the light off and the '
                                                                  'Live reader standing aside')
    app.live.light.switch.state = 'down'
    check(app.root_box.children[-1] is app.overlay.bar, 'app: the Live card switch puts the bar at the top of the app')
    app.show('dyno')
    check(not app.runner.paused, 'app: on Dyno the Live reader runs for the light')
    app.show('scan')
    check(app.runner.paused, 'app: on Scan it stands aside')
    app.set_fullscreen(True)
    check(app.overlay.bar.parent is app.root_box and (app.overlay.bar.right_gap or app.overlay.bar.top_gap),
          'app: full screen keeps the bar, clear of the Record, HUD and Exit buttons')
    app.set_hud(True)
    check(app.mirror.flipped and app.overlay.bar.parent is app.root_box and app.root_box.parent is app.mirror,
          'app: HUD mode mirrors the bar along with the picture')
    app.set_hud(False)
    app.open_light_settings()
    check(not app.fullscreen and app.manager.current == 'live', 'app: a tap on the bar leaves full screen for Live')
    app.move_light_bar()
    check(app.link.saved['light_position'] == 'bottom' and app.root_box.children[1] is app.overlay.bar,
          'app: a long press moves it above the tabs')
    check(app_main.prefs.load(os.path.join(data, 'prefs.json'))['light_position'] == 'bottom',
          'app: and the move is in prefs.json')
    app.show('shift')
    app.sniff._checking = True
    app.sniff._adapter_changed()
    check(app.runner.paused, 'app: while the sniffer runs its car check the Live reader stands aside on Shift')
    app.sniff._checking = False
    app.sniff._adapter_changed()
    check(not app.runner.paused, 'app: given back, the reader runs again for the light')
    app.overlay.stop()
    app.runner.stop()


if __name__ == '__main__':
    main()
