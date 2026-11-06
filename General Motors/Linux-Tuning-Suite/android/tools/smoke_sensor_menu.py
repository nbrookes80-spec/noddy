"""Headless smoke test of the long-press sensor menu. Needs Kivy; not part of the normal pytest run.

Run from the android/ folder:

    KIVY_NO_ARGS=1 SDL_VIDEODRIVER=dummy /home/nathan/TunerToolPro-Android/.venv/bin/python tools/smoke_sensor_menu.py

It builds the Scan and Live screens in demo mode, long presses a card, checks the menu's buttons, then does a
move, a move to a page and a move on the Live screen the way main.py does (merge into the saved order, configure,
redraw), and checks `dashboard_layout.ORDER` and the arranged order each time. Exits non-zero on the first failure.
"""

import os
import sys
import tempfile

os.environ.setdefault('KIVY_NO_ARGS', '1')
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.clock import Clock  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.modalview import ModalView  # noqa: E402

import pid_card  # noqa: E402
from live_ui import LiveScreen, StreamRunner  # noqa: E402
from scan_ui import ScanScreen  # noqa: E402
from tunertoolpro.scanner import dashboard_layout, pid_view  # noqa: E402
from tunertoolpro.scanner.session import Session  # noqa: E402


def check(condition, message):
    if not condition:
        print('FAIL:', message)
        sys.exit(1)
    print('ok  :', message)


def buttons(widget):
    return {w.text: w for w in widget.walk() if isinstance(w, Button)}


def menu_of(card):
    card._long_press(0)
    menus = [w for w in pid_card.Window.children if isinstance(w, pid_card.SensorMenu)]
    check(menus and menus[0].card is card, 'a long press opens the sensor menu of that card')
    return menus[0]       # the newest is first; a closed menu can linger while its fade-out finishes


def main():
    folder = tempfile.mkdtemp()
    pid_card.hooks.views = pid_view.PidViews(os.path.join(folder, 'pid_view.json'))
    session = Session()
    session.set_demo(True)
    runner = StreamRunner(session, lambda: None)
    live, scan = LiveScreen(session, runner), ScanScreen(session)
    saved = {'dash_order': []}
    log = {'edit': 0, 'help': 0, 'orders': []}

    def order_changed(arranged):                          # what main.order_changed does, without the app
        order = dashboard_layout.merged_order(dashboard_layout.ORDER, arranged)
        saved['dash_order'] = dashboard_layout.clean_order(order)
        dashboard_layout.configure(saved['dash_order'], dashboard_layout.PAGE_SIZE)
        log['orders'].append(arranged)
        live.render()
        scan.render()

    pid_card.hooks.arranged = lambda scope: [p.pid for p in (live if scope == 'live' else scan).arranged()]
    pid_card.hooks.on_order = order_changed
    pid_card.hooks.on_edit = lambda pid, done: log.__setitem__('edit', log['edit'] + 1)
    pid_card.hooks.on_help = lambda pid: log.__setitem__('help', log['help'] + 1)

    # --- Scan screen ---
    scan.set_view('Live')
    cards = scan.cards
    check(len(cards) >= 2, f'the Scan page has sensors ({len(cards)})')
    card = cards[1]
    first_id = cards[0].pid.pid
    menu = menu_of(card)
    labels = buttons(menu)
    for text in ('Settings, zones and colour...', 'Display: text, digital, graph, histogram, analogue...',
                 'Move earlier', 'Move later', 'Move to top', 'Move to end', 'Move to page...',
                 'Page layout... (coming in the next step)', 'Reset lowest, highest and average',
                 'Ask my AI agent', 'Close'):
        check(text in labels, f'menu has "{text}"')
    check(labels['Page layout... (coming in the next step)'].disabled, 'Page layout is disabled for now')
    labels['Settings, zones and colour...'].dispatch('on_release')
    check(log['edit'] == 1, 'Settings opens the editor hook')
    menu = menu_of(card)
    buttons(menu)['Ask my AI agent'].dispatch('on_release')
    check(log['help'] == 1, 'Ask my AI agent calls the help hook')

    before = [p.pid for p in scan.arranged()]
    moved_id = card.pid.pid
    menu = menu_of(card)
    labels = buttons(menu)
    if not labels['Move earlier'].disabled:
        labels['Move earlier'].dispatch('on_release')
        after = [p.pid for p in scan.arranged()]
        check(after.index(moved_id) == before.index(moved_id) - 1, 'Move earlier moves the sensor one place up')
        check(dashboard_layout.ORDER[:1] != [] and dashboard_layout.ORDER.index(moved_id) < dashboard_layout.ORDER.index(before[before.index(moved_id) - 1]),
              'dashboard_layout.ORDER now has it before its old neighbour')
        check(sorted(after) == sorted(before), 'no sensor was lost or doubled')
    else:
        print('skip: first card is first in its group')

    # a card that is first in its group: move earlier is greyed out
    first_card = scan.cards[0]
    check(buttons(menu_of(first_card))['Move earlier'].disabled, 'the first sensor of a group cannot move earlier')

    # move to end of its group
    card = scan.cards[0]
    group_ids = [p.pid for p in scan.arranged() if dashboard_layout.group_of_id(p.pid) == dashboard_layout.group_of_id(card.pid.pid)]
    menu = menu_of(card)
    labels = buttons(menu)
    if len(group_ids) > 1:
        labels['Move to end'].dispatch('on_release')
        again = [p.pid for p in scan.arranged() if dashboard_layout.group_of_id(p.pid) == dashboard_layout.group_of_id(card.pid.pid)]
        check(again[-1] == card.pid.pid, 'Move to end puts it last in its group')
    else:
        menu.dismiss()

    # move to page
    ids = [p.pid for p in scan.arranged()]
    sizes = len(dashboard_layout.pages(ids))
    check(sizes >= 2, f'the dashboard has {sizes} pages')
    target = next(pid for pid in ids if dashboard_layout.reachable_pages(ids, pid, group=dashboard_layout.group_of_id) and
                  max(dashboard_layout.reachable_pages(ids, pid, group=dashboard_layout.group_of_id)) > dashboard_layout.position(ids, pid)[0])
    card_for = lambda pid: next(c for c in scan.cards + list(live.cards.values()) if c.pid.pid == pid) if any(
        c.pid.pid == pid for c in scan.cards) else None
    # the card may be on another scan page; turn to it
    for page in range(sizes):
        scan.page = page
        scan.render()
        card = card_for(target)
        if card is not None:
            break
    menu = menu_of(card)
    menu.choose_page()
    popups = [w for w in pid_card.Window.children if isinstance(w, ModalView) and not isinstance(w, pid_card.SensorMenu)]
    check(popups, 'Move to page... opens the page chooser')
    last_reachable = max(dashboard_layout.reachable_pages(ids, target, group=dashboard_layout.group_of_id))
    page_buttons = buttons(popups[0])
    check(not page_buttons[f'Page {last_reachable + 1}'].disabled, 'a page that can take the sensor is enabled')
    page_buttons[f'Page {last_reachable + 1}'].dispatch('on_release')
    now = [p.pid for p in scan.arranged()]
    check(dashboard_layout.position(now, target)[0] == last_reachable, f'the sensor is now on page {last_reachable + 1}')
    check(sorted(now) == sorted(ids), 'moving to a page loses no sensor')

    # --- Live screen ---
    live.render()
    live_card = next(iter(live.cards.values()))
    before = [p.pid for p in live.arranged()]
    menu = menu_of(live_card)
    labels = buttons(menu)
    if not labels['Move later'].disabled:
        labels['Move later'].dispatch('on_release')
        after = [p.pid for p in live.arranged()]
        check(after.index(live_card.pid.pid) == before.index(live_card.pid.pid) + 1, 'Move later works on the Live screen')
    else:
        menu.dismiss()

    # --- main.py's own order_changed, on a stand-in app: saves prefs, configures the layout, redraws both screens ---
    import types
    import main as app_main
    from tunertoolpro import prefs
    prefs_path = os.path.join(folder, 'prefs.json')
    link = types.SimpleNamespace(saved=dict(prefs.DEFAULTS), prefs_path=prefs_path)
    stand_in = types.SimpleNamespace(link=link, live=live, scan=scan, sensors_changed=lambda: (live.render(), scan.render()),
                                     _restore_scroll=app_main.TunerToolProApp._restore_scroll)
    ids = [p.pid for p in scan.arranged()]
    mover = next(i for i in ids if dashboard_layout.reorder(ids, i, 'later') != ids)
    app_main.TunerToolProApp.order_changed(stand_in, dashboard_layout.reorder(ids, mover, 'later'))
    check([p.pid for p in scan.arranged()].index(mover) == ids.index(mover) + 1, 'main.order_changed applies the move to Scan')
    check(prefs.load(prefs_path)['dash_order'] == dashboard_layout.ORDER, 'main.order_changed saves dash_order to prefs.json')
    print('SMOKE PASSED')


if __name__ == '__main__':
    main()
