"""Headless smoke test of the Link screen's adapter card. Needs Kivy; not part of the normal pytest run.

Run from the android/ folder:

    KIVY_NO_ARGS=1 SDL_VIDEODRIVER=dummy /home/nathan/TunerToolPro-Android/.venv/bin/python tools/smoke_link_adapter.py

It builds the Link screen against the fake ELM327, then checks: the new controls (protocol list with every choice,
reconnect switch, read rate) save to prefs; the Adapter information button appears only when connected, shows
firmware, volts, protocol and car battery, and sends only ATI/ATRV/ATDP/0142 (through Session.adapter_job); the saved
protocol is re-sent on connect; the Live reader's delay follows the saved rate; and the automatic reconnect
steps 1, 2, 4, 8, 16 s, tells the user each step, can be stopped, gives up after the last, and connects when the
adapter comes back. Everything sent is checked against obd.is_allowed. Exits non-zero on the first failure.
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
from live_ui import StreamRunner  # noqa: E402
from tunertoolpro import prefs  # noqa: E402
from tunertoolpro.link import obd  # noqa: E402
from tunertoolpro.link.testing import FakeElm327  # noqa: E402
from tunertoolpro.scanner.session import Session  # noqa: E402


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
    session = Session()
    runner = StreamRunner(session, lambda: (None, None))
    fake = FakeElm327()
    link = link_ui.LinkScreen(session, path)
    runner.rate = lambda: link.saved['read_rate']
    link.kind = 'Wi-Fi'
    link.wifi_box.text = f'127.0.0.1:{fake.port}'

    # controls and saving
    check(list(link.protocol_box.values) == [link.names[c] for c in obd.PROTOCOLS], 'protocol list has every choice')
    for code in obd.PROTOCOLS:
        link.protocol_box.text = link.names[code]
        check(prefs.load(path)['adapter_protocol'] == code, f'protocol {code} saved from the Link screen')
    link.protocol_box.text = link.names['6']
    link.rate_box.text = '8'
    check(prefs.load(path)['read_rate'] == 8 and link.saved['read_rate'] == 8, 'read rate saved')
    check(abs(obd.round_delay(runner.rate()) - 0.125) < 1e-9, 'Live reader delay follows the saved rate')
    check(link.info_button.parent is None, 'Adapter information hidden while not connected')

    # connect (saved protocol 6 is sent, then probed)
    link.toggle()
    check(pump(lambda: session.elm is not None), 'connected to the fake adapter')
    check(link.info_button.parent is link.adapter_card, 'Adapter information shown when connected')
    check(pump(lambda: fake.received[-2:] == ['ATSP6', '0100']), 'saved protocol re-sent on connect')

    # adapter information
    before = len(fake.received)
    link.show_info()
    check(pump(lambda: link.info_text.text.startswith('Adapter:')), 'information text shown')
    print(link.info_text.text)
    for expect in ('ELM327 v1.5', '12.6V', 'ISO 15765-4 (CAN 11/500)', '12.6 V'):
        check(expect in link.info_text.text, f'info shows {expect}')
    sent = fake.received[before:]
    check({'ATI', 'ATRV', 'ATDP', '0142'} <= set(sent), f'info sent {sent}')
    check(not session.adapter_busy and link.info_button.disabled is False, 'adapter given back after the job')
    check(all(obd.is_allowed(c) for c in fake.received), 'everything sent so far is on the allow list')

    # a drop with auto reconnect off just disconnects
    link.connection_lost('gone')
    check(session.elm is None and link._retry_step is None and 'Connection lost' in link.state.text, 'no retry when off')
    check(link.info_button.parent is None, 'Adapter information removed after a disconnect')

    # a drop with auto reconnect on: 1, 2, 4, 8, 16 s, each step told, then it gives up
    link.saved['auto_reconnect'] = True
    fake.close()                                  # nothing listens now, so each try fails
    link.wifi_box.text = f'127.0.0.1:{fake.port}'
    link.connection_lost('gone')
    for number, delay in enumerate(obd.backoff_schedule(), 1):
        check(f'in {delay} s (try {number} of 5)' in link.state.text, f'step {number} says {delay} s: {link.state.text}')
        check(link.connect_button.text == 'Stop reconnecting', 'button offers to stop')
        link._retry_event.cancel()                # do not wait the real seconds
        link._retry_now()
        check(pump(lambda: not link._connecting and (link._retry_step is None or link._retry_event is not None)),
              f'try {number} failed')
    check(link._retry_step is None and 'Gave up after 5 tries' in link.state.text, 'gives up after the last: ' + link.state.text)
    check(link.connect_button.text == 'Connect', 'button back to Connect')

    # stopping by hand
    link.connection_lost('gone again')
    check(link._retry_step == 0, 'a new drop starts the schedule again')
    link.toggle()
    check(link._retry_step is None and link._retry_event is None and link.state.text == 'Stopped reconnecting.',
          'Stop reconnecting cancels the retry')

    # the adapter comes back
    fake2 = FakeElm327()
    link.wifi_box.text = f'127.0.0.1:{fake2.port}'
    link.connection_lost('third drop')
    link._retry_event.cancel()
    link._retry_now()
    check(pump(lambda: session.elm is not None), 'reconnected when the adapter came back')
    check(link._retry_step is None and link.connect_button.text == 'Disconnect', 'retry state cleared on success')
    check(pump(lambda: fake2.received[-2:] == ['ATSP6', '0100']), 'saved protocol re-sent after the reconnect')
    check(all(obd.is_allowed(c) for c in fake2.received), 'everything the reconnect sent is on the allow list')
    link.disconnect()
    print('ALL OK')


if __name__ == '__main__':
    main()
