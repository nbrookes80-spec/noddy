"""Headless smoke test of the full-page layouts. Needs Kivy; not part of the normal pytest run.

Run from the android/ folder:

    KIVY_NO_ARGS=1 SDL_VIDEODRIVER=dummy /home/nathan/TunerToolPro-Android/.venv/bin/python tools/smoke_page_layout.py

It builds the Scan and Live screens in demo mode, puts them in full screen and checks that the cards of a page sit
where page_layout.slots says; picks layouts through the chooser the way the app does (main.open_layout and
main.layout_picked on a stand-in app) for one page and for all pages; checks that a small cell drops the parts of a
card that do not fit and a tall one gets them back; that the sensor menu's Page layout button reaches the app; that
leaving full screen gives back the scrolling lists; and that the HUD mirror still holds the page. Exits non-zero on
the first failure.
"""

import os
import sys
import tempfile
import types

os.environ.setdefault('KIVY_NO_ARGS', '1')
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.clock import Clock  # noqa: E402
from kivy.metrics import dp  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.button import Button  # noqa: E402
from kivy.uix.gridlayout import GridLayout  # noqa: E402
from kivy.uix.scrollview import ScrollView  # noqa: E402

import pid_card  # noqa: E402
from hud import Mirror  # noqa: E402
from layout_ui import FullPage, LayoutChooser, LayoutPreview, PageBoard  # noqa: E402
from live_ui import LiveScreen, StreamRunner  # noqa: E402
from scan_ui import ScanScreen  # noqa: E402
from tunertoolpro import prefs  # noqa: E402
from tunertoolpro.scanner import dashboard_layout, page_layout, pid_view  # noqa: E402
from tunertoolpro.scanner.session import Session  # noqa: E402

WIDTH, HEIGHT = 800, 480


def check(condition, message):
    if not condition:
        print('FAIL:', message)
        sys.exit(1)
    print('ok  :', message)


def settle():
    for _ in range(4):
        Clock.tick()


def board_of(screen):
    boards = [w for w in screen.walk(restrict=True) if isinstance(w, PageBoard)]
    check(len(boards) == 1, f'{type(screen).__name__} shows one page board in full screen')
    return boards[0]


def rects(board):
    return [(c.x, c.y, c.width, c.height) for c in board.cards]


def overlap(a, b):
    return max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])) * max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))


def check_placed(board, template, label):
    """The cards sit in the cells page_layout gives for the board's own shape, inside the board, apart from each other."""
    expected = page_layout.to_pixels(page_layout.slots(template, len(board.cards), aspect=board.width / board.height),
                                     board.x, board.y, board.width, board.height, dp(8))
    placed = rects(board)
    check(all(abs(a - b) < 1 for got, want in zip(placed, expected) for a, b in zip(got, want)),
          f'{label}: the cards sit in the {template} cells')
    check(all(x >= board.x - 1 and y >= board.y - 1 and x + w <= board.right + 1 and y + h <= board.top + 1
              for x, y, w, h in placed), f'{label}: every card is inside the board')
    check(all(overlap(a, b) < 1 for i, a in enumerate(placed) for b in placed[i + 1:]), f'{label}: no cards overlap')


def tiles_of(chooser):
    return {t.template: t for t in chooser.tiles}


def main():
    folder = tempfile.mkdtemp()
    pid_card.hooks.views = pid_view.PidViews(os.path.join(folder, 'pid_view.json'))
    dashboard_layout.configure([], dashboard_layout.DEFAULT_PAGE_SIZE)
    page_layout.configure('grid', {})
    session = Session()
    session.set_demo(True)
    runner = StreamRunner(session, lambda: None)
    live, scan = LiveScreen(session, runner), ScanScreen(session)
    holder = BoxLayout(size_hint=(None, None), size=(WIDTH, HEIGHT))
    scan_holder = BoxLayout(size_hint=(None, None), size=(WIDTH, HEIGHT))
    holder.add_widget(live)
    scan_holder.add_widget(scan)
    settle()

    # --- the app's side: main.open_layout and main.layout_picked on a stand-in ---
    import main as app_main
    prefs_path = os.path.join(folder, 'prefs.json')
    link = types.SimpleNamespace(saved=dict(prefs.DEFAULTS), prefs_path=prefs_path)
    stand_in = types.SimpleNamespace(link=link, live=live, scan=scan, fullscreen=True,
                                     sensors_changed=lambda: (live.render(), scan.render()))
    stand_in.layout_picked = lambda *args: app_main.TunerToolProApp.layout_picked(stand_in, *args)

    # --- Scan, full screen, the default grid ---
    scan.set_view('Live')
    page_one = [p.pid for p in scan.pages[0]]
    scan.set_full(True)
    settle()
    board = board_of(scan)
    check(isinstance(scan.body.children[0], FullPage), 'Scan full screen shows a FullPage')
    check([c.pid.pid for c in board.cards] == page_one and [c.pid.pid for c in scan.cards] == page_one,
          'the board holds the sensors of page 1, in order, and Scan polls only those')
    check_placed(board, 'grid', 'Scan page 1')
    bar = {w.text: w for w in scan.walk(restrict=True) if isinstance(w, Button) and w.text in ('Previous', 'Next', 'Page layout')}
    check(set(bar) == {'Previous', 'Next', 'Page layout'} and not any(b.disabled for b in bar.values()),
          'the page bar has Previous, Next and Page layout, all usable')

    # --- the chooser, opened the way the app opens it ---
    app_main.TunerToolProApp.open_layout(stand_in, 'scan')
    chooser = next(w for w in pid_card.Window.children if isinstance(w, LayoutChooser))
    check(list(tiles_of(chooser)) == list(page_layout.TEMPLATES), 'the chooser has a tile for each template, in order')
    check(chooser.count == len(page_one) and chooser.page == 0, 'the chooser is for page 1 and its sensor count')
    check(not chooser.all_pages, 'in full screen the chooser starts on "This page"')
    check(all(len([w for w in t.walk(restrict=True) if isinstance(w, LayoutPreview)]) == 1 for t in chooser.tiles),
          'each tile draws one preview')
    tiles_of(chooser)['hero'].dispatch('on_release')
    settle()
    check(link.saved['dash_page_templates'] == {'0': 'hero'} and link.saved['dash_template'] == 'grid',
          'picking for this page saves a choice for page 1 only')
    check(prefs.load(prefs_path)['dash_page_templates'] == {'0': 'hero'}, 'and writes it to prefs.json')
    board = board_of(scan)
    check_placed(board, 'hero', 'Scan page 1 after choosing hero')
    areas = [w * h for _x, _y, w, h in rects(board)]
    check(areas[0] == max(areas) and areas[0] > 1.4 * areas[1], 'the first sensor is the large one')

    scan.turn(1)
    settle()
    check_placed(board_of(scan), 'grid', 'Scan page 2 keeps the default grid')
    scan.turn(-1)

    app_main.TunerToolProApp.open_layout(stand_in, 'scan')
    chooser = next(w for w in pid_card.Window.children if isinstance(w, LayoutChooser))
    chooser.every_page.trigger_action(0)
    check(chooser.all_pages and chooser.this_page.state == 'normal', 'the scope buttons are a pair')
    tiles_of(chooser)['rows'].dispatch('on_release')
    settle()
    check(link.saved['dash_template'] == 'rows' and link.saved['dash_page_templates'] == {},
          'picking for all pages sets the default and drops the page choices')
    check_placed(board_of(scan), 'rows', 'Scan page 1 after choosing rows for all pages')
    scan.turn(1)
    settle()
    check_placed(board_of(scan), 'rows', 'Scan page 2 after choosing rows for all pages')
    scan.turn(-1)

    # --- a card in a small cell, then a tall one ---
    card = board_of(scan).cards[0]
    card.size = (dp(300), dp(60))
    check(card.orientation == 'horizontal' and card.gauge.opacity == 0 and card.stats_line.opacity == 0,
          'a short cell puts the name and number side by side and drops the picture and stats')
    card.size = (dp(300), dp(100))
    check(card.orientation == 'vertical' and card.gauge.opacity == 0 and card.name.height == dp(26),
          'a cell with room for name and number stacks them again (heights restored), still no picture')
    card.size = (dp(300), dp(400))
    check(card.gauge.opacity == 1 and card.gauge.size_hint_y == 1 and card.stats_line.opacity == 1,
          'a tall cell shows the picture, stretched, and the stats line')

    # --- the sensor menu's button reaches the app ---
    menu_card = scan.cards[0]
    menu_card._long_press(0)
    menu = next(w for w in pid_card.Window.children if isinstance(w, pid_card.SensorMenu))
    button = next(w for w in menu.walk(restrict=True) if isinstance(w, Button) and w.text == 'Page layout...')
    check(button.disabled, 'Page layout is greyed out while no chooser is wired')
    menu.dismiss()
    asked = []
    pid_card.hooks.on_layout = asked.append
    menu_card._long_press(0)
    menu = next(w for w in pid_card.Window.children if isinstance(w, pid_card.SensorMenu))
    button = next(w for w in menu.walk(restrict=True) if isinstance(w, Button) and w.text == 'Page layout...')
    check(not button.disabled, 'Page layout is enabled once the app wires it')
    button.dispatch('on_release')
    check(asked == ['scan'], 'it asks the app for the Scan layout chooser')
    pid_card.hooks.on_layout = None

    # --- Live, full screen ---
    live_pages = live.full_pages()
    live.set_full(True)
    settle()
    board = board_of(live)
    check([c.pid.pid for c in board.cards] == [p.pid for p in live_pages[0]] and set(live.cards) == {c.pid.pid for c in board.cards},
          'Live full screen shows page 1 of the Live sensors')
    check_placed(board, 'rows', 'Live page 1 (the all-pages choice applies here too)')
    check(live.light.parent is None, 'in full screen the Live page leaves the shift light to the app-wide bar')
    live.turn(1)
    settle()
    check([c.pid.pid for c in board_of(live).cards] == [p.pid for p in live_pages[1]], 'Next turns to Live page 2')
    check(live.layout_target() == (1, len(live_pages[1])), 'the chooser target follows the page')
    live.refresh(0)
    stand_in.fullscreen = True
    app_main.TunerToolProApp.open_layout(stand_in, 'live')
    chooser = next(w for w in pid_card.Window.children if isinstance(w, LayoutChooser))
    check(chooser.page == 1, 'the Live chooser is for the page being shown')
    tiles_of(chooser)['dials'].dispatch('on_release')
    settle()
    check_placed(board_of(live), 'dials', 'Live page 2 after choosing dials')
    check(link.saved['dash_page_templates'] == {'1': 'dials'}, 'only page 2 got dials')
    live.turn(-1)
    settle()
    check_placed(board_of(live), 'rows', 'Live page 1 is still rows')

    # --- HUD mirror ---
    mirror = Mirror(size_hint=(None, None), size=(WIDTH, HEIGHT))
    mirror.add_widget(holder)
    settle()
    before = rects(board_of(live))
    mirror.flipped = True
    settle()
    check(mirror._scale.x == -1 and rects(board_of(live)) == before, 'the HUD mirror flips the picture, the layout stays put')
    check(mirror.on_touch_down(types.SimpleNamespace(pos=(10, 10))) is True, 'and the mirrored page takes no touches')
    mirror.flipped = False

    # --- leaving full screen gives back the lists ---
    live.set_full(False)
    scan.set_full(False)
    settle()
    check(any(isinstance(w, ScrollView) for w in live.walk(restrict=True)) and not any(isinstance(w, PageBoard) for w in live.walk(restrict=True)),
          'Live outside full screen is the scrolling list again')
    check(len(live.cards) == len(live.arranged()), 'and holds every Live sensor')
    check(all(isinstance(c.parent, GridLayout) and c.size_hint_y is None for c in live.cards.values()),
          'in grids with their own heights')
    check(any(isinstance(w, ScrollView) for w in scan.walk(restrict=True)) and not any(isinstance(w, PageBoard) for w in scan.walk(restrict=True)),
          'Scan outside full screen is the scrolling list again')
    labels = [w.text for w in scan.walk(restrict=True) if isinstance(w, Button)]
    check(all(name in labels for name in ('Previous', 'Next', 'Full screen', 'Page layout')),
          'Scan has Previous, Next, Full screen and Page layout buttons')
    labels = [w.text for w in live.walk(restrict=True) if isinstance(w, Button)]
    check('Page layout' in labels and 'Full screen: live data only' in labels, 'Live has the Page layout button next to Full screen')

    page_layout.configure('grid', {})
    print('SMOKE PASSED')


if __name__ == '__main__':
    main()
