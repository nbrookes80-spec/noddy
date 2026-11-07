# Gauge controls, global shift light, vehicle PID packs and adapter settings

**Spec:** the owner's request of 2026-11-06 (quoted under "Requirements" below). There is no separate spec file; the
request is the binding authority. Background reading: `docs/linux-live-scan-spec.md` (T1 sharing design).

**Goal:** On the TunerToolPro Android app: (1) a shift light that is always on top of every screen, including full
screen and HUD; (2) a long press on any sensor opens a menu to edit its settings (colour, minimum, maximum, red /
yellow / green zones), move or reorder it, and choose a full-page template; (3) learn from the Torque Pro source
and the owner's Torque PID CSVs and add PID data for other car models; (4) OBD adapter settings and communication
updates; (5) other UI tools that fit.

## Requirements (the owner's words, condensed)

- Shift light "on top of other pages ... at any screen, including a home navigation or full screen display".
- Long click on the outputs: change that sensor's settings: colouring, maximum and minimum, red zones, green zones
  and yellow too, "to create UI visual support for dangerous limits".
- Long press also offers: moving the sensor gauge, reordering, full-page template layouts.
- "Decompile the torque-pro-main files and learn": `/home/nathan/torque-pro-main` is plain Java source (pires OBD
  reader plus the owner's `torque-shiftlight` and `torque-dashboard` plugins), so nothing needed decompiling; it
  was read as source. Clone and add PID data for other car models, adapter settings, communication updates, other
  UI tools that "will work well".

## Global Constraints (every task)

- Repo: `/home/nathan/noddy/General Motors/Linux-Tuning-Suite`, branch `feature/gauge-controls-shift-overlay`
  (a local checkpoint of T1 sits underneath). **Never push. Never touch `main`.** Commit locally per task with the
  message ending `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- **Read-only car.** `link/obd.py` `is_allowed` is the only gate to the wire. Nothing may widen it except where a
  task says so, with a test that the default stays refused. Mode 04 clear stays behind `allow_clear` and the confirm.
- **Where logic lives.** Pure, Kivy-free logic belongs in the shared core, which is a local clone at
  `/home/nathan/TunerToolPro-Linux/tunertoolpro-core` (branch `feature/gauge-zones-layouts`, already created;
  tests: `cd` there and `python3 -m pytest -q`). Kivy widgets stay in `android/*.py`.
  The suite carries a vendored, hash-pinned copy, so after a core change do **all** of:
  1. commit in the core clone (`git add -A && git commit`), then `git tag -f v0.3.0` there (local tag, moves);
  2. in the suite root: `TTP_CORE_REPO=/home/nathan/TunerToolPro-Linux/tunertoolpro-core python3 tools/update_core.py v0.3.0`
     then `python3 android/sync_core.py` (updates `app/tunertoolpro`, `android/tunertoolpro` and `core.lock`);
  3. run `python3 tools/update_core.py --check`, the Android tests (`cd android && python3 -m pytest -q tests`),
     the desktop tests (`cd app && QT_QPA_PLATFORM=offscreen /home/nathan/TunerToolPro-Linux/.venv/bin/python -m pytest -q`;
     if that path differs, find the desktop tests and venv) and the core tests; all must stay green;
  4. commit the suite changes. **Never edit `app/tunertoolpro` or `android/tunertoolpro` by hand.**
  Core must stay Python 3.10 compatible and Qt-free and Kivy-free. A core test must fail before the change.
- Android UI code cannot be seen on a desktop. Keep decisions in core functions that tests cover. Each UI task also
  runs `python3 -m py_compile` on changed files and, where Kivy 2.3.1 is importable
  (`/home/nathan/TunerToolPro-Android/.venv/bin/python`, `KIVY_NO_ARGS=1 SDL_VIDEODRIVER=dummy`), a headless smoke
  that builds the widget(s) and exercises the new code path. If that smoke is impossible, say so in the report.
- Saved choices live in `prefs.json` through `tunertoolpro/prefs.py` (keys must be added to `DEFAULTS` and cleaned
  on load, like the existing `dash_*` and `light_*` keys) or in `pid_view.json`. Old files must still load.
- Do not rename or remove existing public names used by other modules without updating every caller and test.
- Imported (CAN replay) signals in `pids.REPLAY` are never sent to the car. Keep it that way.
- Plain, short UI text. No new third-party dependencies (the APK is built by buildozer; do not change
  `buildozer.spec` requirements).

## File map

- Core (`tunertoolpro-core/tunertoolpro/`): `scanner/pid_view.py`, `scanner/dashboard_layout.py`, new
  `scanner/page_layout.py`, `scanner/shift_light.py`, `prefs.py`, `link/obd.py`, `scanner/predefined.py`,
  `scanner/profiles.py`, `data/*.csv`, new `scanner/alerts.py`.
- Android (`android/`): `pid_card.py`, `gauge_ui.py`, `pid_edit_ui.py`, `live_ui.py`, `scan_ui.py`,
  `shift_light_ui.py`, `main.py`, `link_ui.py`, `menu_pages.py`, `ui_kit.py`, `README.md`, tests in `android/tests`.

---

### Task 1: Zones (red, yellow, green) and a colour for each sensor

**Files:** core `scanner/pid_view.py`, tests `tests/test_pid_view*.py` in core (find the existing zone tests);
Android `gauge_ui.py`, `pid_card.py`, `pid_edit_ui.py`.

Today a sensor has `low`, `high` (minimum and maximum), and three one-sided bands: `cold` (blue below), `good`
(green from) and `redline` (red from). There is no yellow, and nothing for a dangerous LOW limit (oil pressure,
battery volts).

Add, to the saved per-sensor choices (clean/validate in `pid_view.clean`, apply/convert/back in the same place
`redline` and `cold` already are, saved in the sensor's own unit exactly like them):

| key | meaning |
|---|---|
| `red_low` | red at or below this value (danger low) |
| `warn_low` | yellow at or below this value, above `red_low` |
| `good` (exists) | green from this value |
| `good_to` | green up to this value (open if absent) |
| `warn` | yellow from this value up to `redline` |
| `redline` (exists) | red from this value |
| `cold` (exists) | blue below this value |
| `color` | `#RRGGBB` accent for the number and gauge; invalid text is dropped |

`pid_view.zone(value, shown)` returns `'red'`, `'yellow'`, `'good'`, `'cold'` or `None` with this priority:
red (`value >= redline` or `value <= red_low`) first, then yellow (`value >= warn` or `value <= warn_low`), then
green (`good <= value <= good_to`, either end optional), then cold (`value < cold`). Existing behaviour with only the
old keys must be unchanged (keep and extend the existing tests). Add `ZONE_ORDER`, and a function
`zone_problems(entry) -> list[str]` that returns plain-English problems for an inconsistent set (for example
`red_low` must be below `warn_low`, `warn` below `redline`, `good_to` not below `good`, all inside nothing odd),
used by the editor instead of ad hoc checks. Validation is about ordering of the numbers the user typed; it must not
reject a legitimate "only red at the top" setup.

Android: the editor (`pid_edit_ui.py`) gets a "Zones" section with labelled boxes in this order: Red at or below,
Yellow at or below, Blue below, Green from, Green up to, Yellow from, Red from; plus a Colour row with a few
swatch buttons (white default, cyan, green, orange, magenta, none). Each box shows the number in the dashboard units
and saves in the sensor's unit, exactly as the existing boxes do. Errors come from `zone_problems`.
`gauge_ui.py` / `pid_card.py` draw the bands on the dial and bar (red, yellow, green, blue strips; the existing
red/cold/good drawing generalises), colour the number by zone (add `yellow`), and tint the number/gauge with
`color` when no zone applies.

**Tests (core, written first, watched failing):** zone priority table incl. both-ends red; old-key-only entries
unchanged; `clean` drops NaN/bool/str-number/bad hex; `zone_problems` cases; unit conversion round trip for the new
keys (the existing convert/back machinery). **Android:** py_compile + headless smoke that builds `PidCard` and
`PidEditPopup` for one built-in PID with a fake `hooks.views`.

**Expected:** core and Android and desktop suites green; commit core, re-pin, commit suite.

### Task 2: Long press menu: settings, move, reorder, layout entry points

**Files:** core `scanner/dashboard_layout.py` (+ tests), `prefs.py` (+ tests); Android `pid_card.py`, `live_ui.py`,
`scan_ui.py`, `main.py`, `ui_kit.py` if needed.

Today a long press on a sensor card opens the editor directly (`PidCard._long_press` -> `hooks.on_edit`), a tap
opens the display chooser, a triple tap asks the agent. Change the long press to open a **sensor menu** (a
`ModalView` like `choose_display`) titled with the sensor name. Tap and triple tap stay exactly as they are.
Menu entries, in order:

1. **Settings, zones and colour...** (the Task 1 editor)
2. **Display: text, digital, graph, histogram, analogue...** (the existing display chooser)
3. **Move earlier** / **Move later** (one place within the dashboard order)
4. **Move to top** / **Move to end**
5. **Move to page...** (full-screen pages of 4/5/6: choose a page number; the sensor goes to the end of that page)
6. **Page layout...** (opens the Task 3 chooser; for this task show the entry but disabled with the text "coming
   in the next step" - it is wired in Task 3)
7. **Reset lowest, highest and average**
8. **Ask my AI agent**
9. **Close**

Core, in `dashboard_layout.py`: pure functions on a list of PID ids, no Kivy, all returning a new list and never
losing or duplicating an id: `move(order, pid_id, step)`, `move_to_edge(order, pid_id, 'top'|'end')`,
`move_to_page(order, pid_id, page_index, size)`, `position(order, pid_id)` -> `(page_index, index_in_page)`. The
`order` is the *arranged* sensor ids of the screen's list (what `arrange()` returns today) and the result is saved
back as the user's `dash_order` (via `clean_order`) so that Live and Scan both reflect it; groups still apply
(`arrange` sorts by group first, then the user order), so a "move" works within the sensor's group and the menu
says so ("Moves within TCM"). `move_to_page` is the exception: pages are cut after arrangement, so document and
test how it behaves (it moves to the first slot of that page's group-run; if the target page is in another group
the menu explains and does nothing). **The implementer must choose one consistent, tested behaviour and write it
in the docstring.**

After any move: save prefs, call `dashboard_layout.configure(...)`, and re-render Live and Scan
(`main.py` has `views_changed` / `sensors_changed`; add a method for order changes). Keep scroll position as
`views_changed` already tries to.

**Tests (core):** each function: ids preserved, no duplicates, edges, unknown id, page maths for sizes 4/5/6,
interplay with `arrange` (the arranged result puts the sensor where the menu said). Android: py_compile, headless
smoke of the menu opening and a move changing `dashboard_layout.ORDER`.

### Task 3: Full-page template layouts

**Files:** new core `scanner/page_layout.py` (+ tests), `prefs.py`; Android `live_ui.py`, `scan_ui.py`,
`pid_card.py` (the Page layout entry), a small `layout_chooser` widget in `ui_kit.py` or a new
`layout_ui.py`.

In full-screen mode Live and Scan show pages of 4, 5 or 6 sensors (see `dashboard_layout.pages`, `set_full`). Add
named **templates** describing how the sensors of one page are placed. Core `page_layout.py`:

- `TEMPLATES` ordered mapping `id -> {'name', 'min', 'max'}`; at least: `grid` (even grid, the current look),
  `columns2` (two columns), `hero` (one large sensor on the left, the rest stacked on the right), `hero_top` (one
  wide sensor on top, the rest in a row/grid below), `rows` (one full-width row each), `dials` (big square cells,
  best for analogue gauges). Each declares which sensor counts it supports.
- `slots(template_id, count)` -> list of `(x, y, w, h)` as fractions of the page, `(0,0)` top-left, covering the
  page without overlap and without gaps larger than a rounding error, in sensor order. Unknown id or unsupported
  count falls back to `grid`.
- `clean_choice(raw)` and `clean_per_page(raw)` for saved data: `dash_template` (the default, `grid`) and
  `dash_page_templates` (a dict page-index-as-string -> template id). Add both to `prefs.DEFAULTS`.
- `template_for_page(default_id, per_page, page_index)`.

Android: a **Page layout** chooser (opened from the long press menu entry "Page layout..." and from a "Page layout"
button near the existing full-screen controls) shows each template as a small drawn preview (rectangles from
`slots`) and applies to *this page* or *all pages*. Full-screen Live/Scan pages place the cards by `slots` instead
of the fixed grid. Non-full-screen lists are unchanged. HUD mirror still works.

**Tests (core):** every template at every supported count tiles the unit square (area sum = 1, no overlap),
fallbacks, saved-data cleaning, per-page lookup. Android: py_compile + headless smoke of the chooser and of laying
out a page.

### Task 4: Shift light on top of every screen

**Files:** core `scanner/shift_light.py` / `prefs.py` as needed; Android `main.py`, `shift_light_ui.py`,
`live_ui.py`, possibly new `shift_overlay.py`.

Today the shift light is a card on the Live screen (`ShiftLight` in `shift_light_ui.py`, driven by
`LiveScreen.tick_light`), and it only runs while Live is open (`StreamRunner.paused = name != 'live'` in
`main.show`). Make it an **app-wide overlay**: a slim bar of the ten LEDs (same style, theme, start, shift and
warning settings, same chime) that sits above every screen of the app: Shift, Dyno, Live, Scan, Link, Sniff, Agent,
Settings and the menus' home navigation, in normal and full-screen mode, and mirrored along with the picture in HUD
mode. System-wide drawing over *other* apps (the Torque plugin's SYSTEM_ALERT_WINDOW approach) is out of scope: it
needs a native Android service; note it as a follow-up in the README, nothing more.

Requirements:
- One owner of shift light state and the chime for the whole app (no double chime when Live is showing). The Live
  card keeps its settings controls but its strip may be hidden in favour of the overlay; both must read the same
  saved settings and never disagree.
- RPM source: `stream.latest['010C']` of the Live `StreamRunner`. The runner must keep reading RPM whenever the
  shift light is on and the app has a data source, **on every screen except while another component owns the
  adapter** (the Sniff screen while it listens: `sniff.holds_adapter()`; and Scan, which polls the adapter itself:
  on Scan take RPM from the Scan screen's own latest readings if it reads `010C`, otherwise show the bar dimmed
  with "RPM not read on this screen"). **Two threads must never talk to the adapter at once.** Read how
  `main.show` pauses the runner and how `Elm327` locks (`elm._lock`) before deciding; write the rule as a pure
  function in core or a small Kivy-free module with tests (for example `shift_light.rpm_source(screen, holds_adapter,
  light_on)` returning `'live'|'scan'|'none'`), and test it for every screen name.
- The overlay shows even with the Live stream stopped (all LEDs off) so its place is stable; it hides only when the
  shift light switch is off.
- Position: top (below the status bar / over the header) or bottom, chosen with a saved `light_position`
  (`'top'|'bottom'`, default `top`) and a height choice small/medium/large (`light_size`); both added to
  `shift_light.DEFAULTS`/`clean` and `prefs.DEFAULTS`. Tapping the bar opens the shift light settings (Live screen
  card); a long press on the bar toggles its position top/bottom.
- It must not swallow touches meant for the screen below except on the bar itself; it must not cover the Record /
  Exit full-screen buttons (leave their space free: they are top right; place the bar so the three buttons stay
  usable, for example inset on the right in full screen).
- The 0.10 s flash and 0.15 s blink timing is unchanged (`LIGHT_TICK`).

**Tests (core, first):** `rpm_source` table; `clean` for the new keys and old prefs files; bar height lookup.
Android: py_compile + headless smoke that builds the overlay, feeds frames, and confirms the chime timer fires once
per due frame even when the Live screen is not current.

### Task 5: OBD adapter settings and communication updates

**Files:** core `link/obd.py` (+ tests incl. the fake ELM327 in `link/testing.py`), `prefs.py`; Android `link_ui.py`,
`menu_pages.py` if the settings live there.

First read what exists: `send_timing`, `PROTOCOLS`, the Link screen's speed settings, `live_ui.ROUND_SECONDS`,
and the Torque Pro references in `/home/nathan/torque-pro-main`: `src/main/res/xml/preferences.xml` (protocol list,
update period, init/reader config, units, GPS, full logging) and `ObdGatewayService`. Add, **read-only and
allow-listed**:

1. **Adapter information** button on the Link screen (visible when connected): shows firmware (`ATI`), adapter
   voltage (`ATRV`), the protocol the adapter picked (`ATDP`) and the car's battery volts if `0142` is in the
   catalogue. `ATI`, `ATRV`, `ATDP` (and `AT@1` if the fake supports it) are the only new commands; add them to the
   allow-list with tests proving a near-miss (`ATRV1`, `ATDP1`, `ATI 1`) is still refused and everything refused
   before is still refused.
2. **Protocol** choice already exists in part; make sure all of `PROTOCOLS` including Automatic can be chosen and
   saved from the Link screen and are re-sent after a reconnect, and add `ATSP`-style *try this one then fall back to
   automatic* via a pure function `protocol_plan(saved)` returning the commands to send (tested).
3. **Reconnect:** when a connected adapter stops answering (`check_connection` in `main.py` drops it today), offer an
   "Reconnect automatically" saved choice (default off): retry with backoff 1, 2, 4, 8, 16 s (pure function
   `backoff_schedule()` in core, tested), stop after the last, tell the user on the Link tab each step.
4. **Update rate cap:** a saved "Read at most N rounds per second" (1 to 10, default 4, matching `ROUND_SECONDS`)
   replacing the constant used by `StreamRunner`; pure `round_delay(rate)` in core (tested, clamps).
5. **Imperial/metric** is already per sensor in `units`; do not duplicate it.

All new saved keys go in `prefs.DEFAULTS` with cleaning. The fake adapter tests must cover the three info commands
and show no command outside the allow-list is ever sent in a full connect + info + 3 live rounds session
(there is an existing pattern in `test_obd.py` / `test_session.py` that records written bytes; follow it).

**Expected:** core tests prove default refusal of everything else; Android py_compile + headless smoke of the Link
screen building with the new card.

### Task 6: PID data for other car models

**Files:** core `scanner/predefined.py`, `scanner/profiles.py`, `link/obd.py` (header opt-in), `scanner/catalog` as
found, `data/`, `prefs.py`; Android `menu_pages.py` (the "GM and Holden PID lists" page), `link_ui.py`.

Sources you may use (and **nothing else**; do not invent manufacturer-specific Mode 21/22 PIDs from memory):
- the owner's Torque PID CSV at
  `/run/user/1000/gvfs/google-drive:host=gmail.com,user=nbrookes80/0AD1l7LopF80nUk9PVA/1han2DNMB8v2YgGr-qVkD1lxyIPGqrt7_/18xRhJAHh-9PrfvJ0Jo5Xg0Sw0RcIDlfF/1QusKfgqR7fClW6J2Rvo_wtANz4yRTtvI`
  (186 rows: rows tagged `[GM]` already exist as `tunertoolpro/data/torque_gm_predefined.csv`; the rest are generic
  Mode 01 rows and Toyota-style Mode 21 rows on headers `7B0` (ABS/skid), `7C0` (meter), `7C4` (A/C) and `7E1`).
  Copy it into core `tunertoolpro/data/` under a clear name (if the GVFS path is unreadable, fall back to the CSV
  content quoted in `docs/` if you can find it, else report BLOCKED);
- the SAE J1979 standard Mode 01 PIDs `0x00`-`0x5F` (public, formulas known) for a **Generic OBD-II** pack that adds
  the standard sensors the current catalogue lacks;
- `/home/nathan/torque-pro-main/src/main/java/com/github/pires/obd/**` (the standard Mode 01 command classes show
  which PIDs and formulas that reader uses).

Do:
1. Extend the predefined-list mechanism so there are packs: **Generic OBD-II (any car)**, **Toyota-style modules
   (from your Torque CSV)** and keep the GM pack. Rows are parsed with the existing safe `torque_csv.parse`
   (equations go through `compile_equation`; refused rows are reported, not guessed). Every non-GM, non-J1979 row is
   `verified = False` (shown as "unconfirmed" by the cards already).
2. Built-in **profiles** (`profiles.built_in`) for Generic OBD-II and Toyota-style, with make/model/year left
   generic; selecting one shows only that pack's sensors on the dashboard like the GM profile does. The imported-CAN
   and user profile machinery must keep working.
3. **Wire safety:** Toyota-style rows use Mode 21 and headers `7B0`, `7C0`, `7C4`, `7E1` that `is_allowed` does not
   accept today. Add an **opt-in**: `Elm327(transport, allow_clear=False, extra_modules=False)`; with it False
   (default) nothing changes and the pack's Mode 21 / extra-header reads are skipped with a clear "module access is
   off" message on the card. With it True: `ATSH` for exactly `7B0`, `7C0`, `7C4`, `7E1` and Mode 21 requests for
   *catalogued* PIDs only are allowed (still read-only: no Mode 2E/2F/31/10/27/14/04 or anything else). A saved
   Link-screen switch "Allow reads of other modules (ABS, meter, A/C) for the Toyota-style pack" (default off) sets
   it; the only construction site is `link_ui.py` (`Elm327(...)` there already passes `allow_clear`); extend
   `tests/test_clear_codes_wiring.py` style checking so every `Elm327(` call passes `extra_modules=` too.
4. Core tests: pack counts and a few exact decoded values per pack (hand-computed from the equations); refused rows;
   profiles listed; `is_allowed` default refuses `ATSH7B0` and `217101` style requests; opt-in allows exactly the
   catalogued ones and still refuses `2E`, `2F`, `04`, `10`, `27`, `31`, `14` services and an uncatalogued `21XX`.
   README note lists what each pack came from and that nothing is confirmed on a real car.

### Task 7: Zone alerts and other dashboard tools

**Files:** new core `scanner/alerts.py` (+ tests), `prefs.py`; Android `pid_card.py`, `live_ui.py`, `scan_ui.py`,
`main.py`, `menu_pages.py`, `README.md`.

Use the zones from Task 1 for visible and audible danger support:
1. **Red alert:** when a sensor's zone becomes `red`, its card flashes (border/background pulse at about 2 Hz) while
   it stays red, and a beep (reuse the chime WAV generator in `shift_light.write_chime` or a second tone) plays at
   most once every 2 seconds across all sensors, only if "Zone alerts" is on. `alerts.py`: a pure
   `AlertTracker` with `update(pid_id, zone, now)` returning `{'flash': bool, 'beep': bool}`, rate limit and
   hysteresis (stay red until the value has left the red zone for 1 s) all tested with a fake clock.
2. Saved choices `alert_on` (default True) and `alert_sound` (default True) in `prefs.DEFAULTS` and two toggles on
   the Settings page (find where dashboard options such as `dash_stats` are toggled in `menu_pages.py`).
3. **Peak hold marks** already exist as min/max stats; do not redo them. Instead add a long-press menu entry
   "Copy these zones to similar sensors..." only if trivial; otherwise skip and say so in the report.
4. README: describe the sensor menu, zones, page layouts, the app-wide shift light, adapter settings, PID packs and
   their limits; update the PID count claims that are now wrong (the README says 111, check the real number).

**Tests (core):** `AlertTracker` table. Android: py_compile + headless smoke that a card in red toggles its flash
state.
