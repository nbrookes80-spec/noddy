"""Headless smoke test of the PID packs and the "Allow reads of other modules" switch. Needs Kivy; not part of pytest.

Run from the android/ folder:

    KIVY_NO_ARGS=1 SDL_VIDEODRIVER=dummy /home/nathan/TunerToolPro-Android/.venv/bin/python tools/smoke_packs.py

Builds the Link screen against the fake ELM327 and checks: the switch is off by default and saved; with it off the
connection refuses ATSH7B0 and a catalogued Mode 21 read, sends nothing for it, and a PidCard shows "module access is
off"; with it on (also applied to the open link) the module read and its header switch go out and decode, a header
outside the four and an uncatalogued 21XX are still refused; the Generic OBD-II pack activates. The Mode 21 rows are
made up for this test (TEST ONLY). Exits non-zero on the first failure.
"""

import os
import sys
import tempfile
import time

os.environ.setdefault('KIVY_NO_ARGS', '1')
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.clock import Clock  # noqa: E402

import link_ui  # noqa: E402
from pid_card import PidCard  # noqa: E402
from tunertoolpro import prefs  # noqa: E402
from tunertoolpro.link import obd  # noqa: E402
from tunertoolpro.link.testing import FakeElm327  # noqa: E402
from tunertoolpro.scanner import pids, profiles, torque_csv  # noqa: E402
from tunertoolpro.scanner.session import Session  # noqa: E402

HEAD = ('"Name", "ShortName", "ModeAndPID", "Equation", "Min Value", "Max Value", "Units", "Header", '
        '"startDiagnostic", "stopDiagnostic", "scale","minimumRefreshDelayMillis"\n')
TEST_ROW = '"[TEST]Module value","T","0x2181","A-40",-40,215,"C","7B0","","",1,0\n'


def check(condition, message):
    if not condition:
        print('FAIL:', message)
        sys.exit(1)
    print('ok  :', message)


def pump(until, seconds=5.0):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        Clock.tick()
        if until():
            return True
        time.sleep(0.01)
    return False


def main():
    path = os.path.join(tempfile.mkdtemp(), 'prefs.json')
    found, _ = torque_csv.parse(HEAD + TEST_ROW, source='smoke', modules=True)
    pids.use_extras(found)
    fake = FakeElm327()
    fake.REPLIES = dict(FakeElm327.REPLIES, ATSH7B0='OK', **{'2181': '618178'})
    session = Session()
    link = link_ui.LinkScreen(session, path)
    link.kind = 'Wi-Fi'
    link.wifi_box.text = f'127.0.0.1:{fake.port}'
    check(prefs.load(path)['extra_modules'] is False and link.saved['extra_modules'] is False, 'switch is off by default')

    link.toggle()
    check(pump(lambda: session.elm is not None), 'connected to the fake adapter')
    elm = session.elm
    check(elm.extra_modules is False, 'link built with module access off')
    sent = len(fake.received)
    values, errors = elm.poll(['2181'])
    check(values == {} and 'module access is off' in errors['2181'].lower(), f'module read skipped: {errors}')
    try:
        elm.command('ATSH7B0')
        check(False, 'ATSH7B0 should be refused')
    except obd.UnsafeCommand:
        check(True, 'ATSH7B0 refused while off')
    check(len(fake.received) == sent, 'nothing was sent for the module read')

    card = PidCard(pids.CATALOG['2181'])
    card.show(None, [], idle=obd.module_note(card.pid, elm.extra_modules))
    check(card.value.text == 'module access is off', f'card says: {card.value.text}')

    link._set_extra_modules(True)
    check(prefs.load(path)['extra_modules'] is True and elm.extra_modules is True, 'switch saved and applied to the open link')
    values, errors = elm.poll(['2181'])
    check(errors == {} and values['2181'] == (80.0, 'C'), f'module read decodes: {values} {errors}')
    check(fake.received[sent:sent + 2] == ['ATSH7B0', '2181'], f'sent {fake.received[sent:]}')
    for bad in ('ATSH7B1', '2182', '2E81', '3101', '1003'):
        try:
            elm.command(bad)
            check(False, f'{bad} should be refused')
        except obd.UnsafeCommand:
            check(True, f'{bad} refused while on')
    check(all(obd.is_allowed(c, elm.allow_clear, True) for c in fake.received), 'everything sent passes is_allowed')
    link.disconnect()

    pids.use_extras([])
    generic = next(p for p in profiles.built_in() if p.key == 'generic-obd2')
    summary = profiles.activate(generic)
    check(summary['added'] == 31 and not summary['rejected'], f'generic pack activates: {summary["added"]} added')
    pids.use_extras([])
    print('ALL OK')


if __name__ == '__main__':
    main()
