"""The pages behind the Settings menu: dashboard layout, themes, units, HUD, PID manager, log data parameters, and the
pre-defined GM and Holden PID lists. Each function returns the cards for one page.

`menu` is the AppMenu that shows them. A page reads and saves its choices through menu.saved and menu._save, so
they land in prefs.json like every other setting, and tells the rest of the app through pid_card.hooks and the
menu's callbacks. Nothing here sends anything to the car.
"""

import os

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

import pid_card
from scanner import car_scan, manual_pids, pid_view, pids, predefined, profiles, themes, units
from settings_ui import spinner
from tunertoolpro import vehicles
from ui_kit import MUTED, RAISED, STATUS, TEXT, Card, make_button, panel_label, section_title, style_button, toggle

COLUMN_LABELS = {0: 'Automatic (as many as fit)', 2: '2 across', 3: '3 across', 4: '4 across'}
SCOPE_LABELS = {'all': 'Everything: Live stream and dashboard', 'live': 'Live stream sensors only',
                'dashboard': 'Dashboard sensors only'}
RATE_LABELS = {0: 'Every round of readings', 1: '1 row per second', 2: '2 rows per second',
               5: '5 rows per second', 10: '10 rows per second'}


def _field(hint, text=''):
    return TextInput(hint_text=hint, text=text, multiline=False, size_hint_y=None, height=dp(44),
                     background_color=RAISED, foreground_color=TEXT, hint_text_color=MUTED)


def _key_for(labels, text):
    return next(key for key, label in labels.items() if label == text)


def _redraw():
    """Ask the dashboards to redraw their cards, if the app has wired that up."""
    if pid_card.hooks.on_changed is not None:
        pid_card.hooks.on_changed()


# --- Dashboard layout and themes -------------------------------------------------------------------

def dashboard_cards(menu):
    saved = menu.saved
    layout = Card()
    layout.add_widget(section_title('Layout'))
    layout.add_widget(panel_label('How many sensor cards sit side by side on Live and Scan. A phone turned on its '
                                  'side fits more.', color=MUTED, font_size=dp(12)))
    columns = spinner(list(COLUMN_LABELS.values()), COLUMN_LABELS[saved['dash_columns']])

    def set_columns(_box, text):
        count = _key_for(COLUMN_LABELS, text)
        menu._save(dash_columns=count)
        pid_card.set_columns(count)
    columns.bind(text=set_columns)
    layout.add_widget(columns)

    style = Card()
    style.add_widget(section_title('Sensor display'))
    style.add_widget(panel_label('How a sensor is drawn until you change its own card (tap a card to choose '
                                 'text, digital, graph, histogram or analogue).', color=MUTED, font_size=dp(12)))
    modes = [pid_view.MODE_NAMES[m] for m in pid_view.MODES]
    chooser = spinner(modes, pid_view.MODE_NAMES[saved['dash_default_mode']])

    def set_mode(_box, text):
        mode = next(m for m in pid_view.MODES if pid_view.MODE_NAMES[m] == text)
        menu._save(dash_default_mode=mode)
        if pid_card.hooks.views is not None:
            pid_card.hooks.views.set_default(mode)
        _redraw()
    chooser.bind(text=set_mode)
    style.add_widget(chooser)
    status = panel_label('', color=MUTED, font_size=dp(12))

    def clear():
        if pid_card.hooks.views is not None:
            pid_card.hooks.views.clear_modes()
        _redraw()
        status.text = 'Every sensor now uses the display above. Names, units, ranges and red lines were kept.'
    style.add_widget(make_button('Use this display for every sensor', clear))
    style.add_widget(status)

    colours = Card()
    colours.add_widget(section_title('Gauge colours'))
    colours.add_widget(panel_label('The colour of the gauge bars, graph lines and needles. The red, blue and green bands '
                                   'keep their colours in every theme.', color=MUTED, font_size=dp(12)))
    chosen = spinner([t.label for t in themes.THEMES.values()], themes.THEMES[saved['dash_theme']].label)

    def set_theme(_box, text):
        key = themes.key_for(text)
        menu._save(dash_theme=key)
        themes.use(key)
        _redraw()
    chosen.bind(text=set_theme)
    colours.add_widget(chosen)

    readings = Card()
    readings.add_widget(section_title('Units'))
    readings.add_widget(panel_label('How temperatures, pressures and speeds are shown on the dashboard. A recording '
                                    'keeps each sensor\'s own unit.', color=MUTED, font_size=dp(12)))
    for group, label in (('temperature', 'Temperature'), ('pressure', 'Pressure'), ('speed', 'Speed and distance')):
        readings.add_widget(panel_label(label, color=MUTED))
        box = spinner(list(units.CHOICES[group]), saved[f'unit_{group}'])

        def set_unit(_box, text, group=group):
            menu._save(**{f'unit_{group}': text})
            if pid_card.hooks.views is not None:
                pid_card.hooks.views.set_units({g: menu.saved[f'unit_{g}'] for g in units.CHOICES})
            _redraw()
        box.bind(text=set_unit)
        readings.add_widget(box)

    extras = Card()
    extras.add_widget(section_title('Range and average'))
    extras.add_widget(panel_label('Shows the range (lowest to highest) and the average reading under each '
                                  'sensor, and marks the lowest and highest on the bar and dial. Tap a sensor '
                                  'and choose "Reset" to start it again.', color=MUTED, font_size=dp(12)))

    def set_stats(on):
        menu._save(dash_stats=on)
        pid_card.set_stats(on)
        _redraw()
    extras.add_widget(toggle('Show range and average under each sensor', saved['dash_stats'], set_stats))
    extras.add_widget(make_button('Reset every sensor now', pid_card.reset_stats))

    hud = Card()
    hud.add_widget(section_title('HUD mode'))
    hud.add_widget(panel_label('Draws full screen mirrored, so a phone lying flat on the dashboard reads correctly '
                               'as a reflection in the windscreen. The HUD button in full screen turns it on and '
                               'off. A mirrored picture ignores touches: use the Exit button.',
                               color=MUTED, font_size=dp(12)))
    hud.add_widget(toggle('Mirror the full screen (HUD)', saved['hud_mirror'],
                          lambda on: menu.on_hud(on) if menu.on_hud is not None else menu._save(hud_mirror=on)))
    hud.add_widget(make_button('Full screen live data', menu._fullscreen))
    return [layout, style, colours, readings, extras, hud]


# --- PID manager -----------------------------------------------------------------------------------

def pid_manager_cards(menu):
    profile = menu.active_profile()
    cards = []
    head = Card()
    head.add_widget(section_title('PID manager'))
    if profile is None:
        head.add_widget(panel_label('The standard list is on the dashboard. Pick a car under "GM and Holden PID '
                                    'lists" to get a list you can switch sensors on and off in.', color=MUTED,
                                    font_size=dp(13)))
        head.add_widget(make_button('GM and Holden PID lists', lambda: menu.open_page('lists'), primary=True))
        head.add_widget(make_button('Enter a PID by hand', menu._open_pid_editor))
        return [head]

    manual = manual_pids.pids_for(menu.cars_folder, profile.key)
    ids = profiles.candidates(profile, manual)
    scan = car_scan.load_scan(os.path.join(os.path.dirname(menu.cars_folder), 'car_scans'), profile.key)
    _shown, no_reply = car_scan.enforce(ids, scan)
    hidden = set(menu.saved['hidden_pids'].get(profile.key, []))
    summary = panel_label('', color=MUTED, font_size=dp(13))

    def show_summary():
        on = len([i for i in ids if i not in hidden and i not in no_reply])
        summary.text = (f'{profile.name}: {on} of {len(ids)} sensors on the dashboard'
                        + (f', {len(no_reply)} not answered by the car' if no_reply else '') + '.')
    show_summary()
    head.add_widget(summary)
    head.add_widget(panel_label('Switch a sensor off to take it off Live and Scan. It stays in the list and can be '
                                'switched back on. Nothing here changes what the car is asked.', color=MUTED,
                                font_size=dp(12)))
    head.add_widget(make_button('Enter a PID by hand', menu._open_pid_editor, primary=True))
    pending = []

    def apply_soon():
        """Several switches in a row make one refresh of the dashboards, not one each."""
        menu._save(hidden_pids=dict(menu.saved['hidden_pids'], **{profile.key: sorted(hidden)}))
        if pending:
            pending[0].cancel()
        pending[:] = [Clock.schedule_once(lambda _dt: menu.on_pids_saved(profile, []), 0.5)]

    def switch_all(on):
        hidden.clear()
        if not on:
            hidden.update(ids)
        for row in rows:
            row.state = 'down' if on else 'normal'
        show_summary()
        apply_soon()
    head.add_widget(make_button('Switch every sensor on', lambda: switch_all(True)))
    head.add_widget(make_button('Switch every sensor off', lambda: switch_all(False)))
    cards.append(head)

    listing = Card()
    listing.add_widget(section_title('Sensors'))
    rows = []
    for pid_id in ids:
        info = pids.get(pid_id)
        label = f'{info.name} ({info.unit})' if info is not None and info.unit else (info.name if info else pid_id)
        row = ToggleButton(text=f'{label}\n[size={int(dp(11))}]{pid_id}' + ('  -  no reply from this car' if pid_id in no_reply
                                                                  else '') + '[/size]',
                           markup=True, size_hint_y=None, height=dp(56),
                           state='normal' if pid_id in hidden else 'down')
        style_button(row, primary=row.state == 'down')
        row.height = dp(56)

        def changed(button, state, pid_id=pid_id):
            style_button(button, primary=state == 'down')
            button.height = dp(56)
            (hidden.discard if state == 'down' else hidden.add)(pid_id)
            show_summary()
            apply_soon()
        row.bind(state=changed)
        rows.append(row)
        listing.add_widget(row)
    cards.append(listing)
    return cards


# --- Log data parameters ---------------------------------------------------------------------------

def log_cards(menu):
    saved = menu.saved
    what = Card()
    what.add_widget(section_title('What is recorded'))
    what.add_widget(panel_label('Choose the sensors a recording has columns for, and how often a row is written. '
                                'Changes apply from the next recording.', color=MUTED, font_size=dp(12)))
    scope = spinner(list(SCOPE_LABELS.values()), SCOPE_LABELS[saved['log_scope']])
    scope.bind(text=lambda _b, text: menu._save(log_scope=_key_for(SCOPE_LABELS, text)))
    what.add_widget(panel_label('Sensors', color=MUTED))
    what.add_widget(scope)
    rate = spinner(list(RATE_LABELS.values()), RATE_LABELS[saved['log_rate']])
    rate.bind(text=lambda _b, text: menu._save(log_rate=_key_for(RATE_LABELS, text)))
    what.add_widget(panel_label('Rows', color=MUTED))
    what.add_widget(rate)
    what.add_widget(panel_label('A slower rate makes a smaller file. Every reading is still kept: a sensor read '
                                'between two rows shows up in the next one.', color=MUTED, font_size=dp(12)))

    run = Card()
    run.add_widget(section_title('Recording'))
    run.add_widget(panel_label('Records the sensors to a spreadsheet (CSV) you can open on a computer. The REC '
                               'button at the top of every screen does the same. Files are named by date and time '
                               'and saved in Tuner Tool Info / Data logs.', color=MUTED, font_size=dp(12)))
    menu.record_button = make_button('', menu._toggle_recording, primary=True)
    run.add_widget(menu.record_button)
    menu.record_status = panel_label('', color=MUTED, font_size=dp(12))
    run.add_widget(menu.record_status)
    return [what, run]


# --- Pre-defined GM and Holden PID lists -----------------------------------------------------------

def lists_cards(menu):
    use = Card()
    use.add_widget(section_title('Use a car\'s list'))
    use.add_widget(panel_label('Switch Live and Scan to the PID list of a car: the built-in Holden, Pontiac and GM '
                               'lists, or one you saved below.', color=MUTED, font_size=dp(12)))
    names = {p.name: p for p in menu.profiles}
    active = menu.active_profile()
    current = active.name if active is not None and active.name in names else next(iter(names), '')
    chooser = spinner(list(names), current)
    use.add_widget(chooser)
    use_status = panel_label('', color=MUTED, font_size=dp(12))

    def activate():
        menu.on_pids_saved(names[chooser.text], [])
        use_status.text = f'{chooser.text} is now the car on Live and Scan.'
        use_status.color = STATUS['good']
    use.add_widget(make_button('Use this car now', activate, primary=True))
    use.add_widget(use_status)

    save = Card()
    save.add_widget(section_title('Save a list to my profile'))
    save.add_widget(panel_label('Pick a Holden or GM list, say which car it is for, and it is saved as your '
                                'profile for that vehicle. It is made the active car straight away.',
                                color=MUTED, font_size=dp(12)))
    titles = {item.title: item for item in predefined.LISTS}
    picker = spinner(list(titles), predefined.LISTS[0].title)
    summary = panel_label('', color=MUTED, font_size=dp(12))

    def describe(*_):
        item = titles[picker.text]
        summary.text = f'{item.summary} ({predefined.count(item)} sensors)'
    picker.bind(text=describe)
    describe()
    saved_car = active if active is not None and not active.builtin else None
    make = spinner(list(vehicles.MAKES), saved_car.make if saved_car and saved_car.make in vehicles.MAKES else 'Holden')
    transmission = spinner([''] + [t.name for t in vehicles.transmissions(make.text)], '')
    make.bind(text=lambda _b, text: setattr(transmission, 'values', [''] + [t.name for t in vehicles.transmissions(text)]))
    model, year = _field('Model, e.g. VE Commodore SS'), _field('Year, e.g. 2011')
    name = _field('Name for this car (optional), e.g. My SS')
    for widget in (picker, summary, panel_label('Make', color=MUTED), make, model, year,
                   panel_label('Transmission (optional)', color=MUTED), transmission, name):
        save.add_widget(widget)
    status = panel_label('', color=STATUS['bad'], font_size=dp(13))

    def save_list():
        item = titles[picker.text]
        profile, rejected = predefined.save_to_profile(menu.cars_folder, item, name.text, make.text, model.text,
                                                       year.text, transmission.text)
        if profile is None:
            status.text = rejected[0]['reason'] if rejected else 'Nothing was saved.'
            status.color = STATUS['bad']
            return
        menu.profiles = profiles.everything(menu.cars_folder)
        menu.on_pids_saved(profile, [])
        status.text = f'Saved {predefined.count(item)} sensors to "{profile.name}" and made it the active car.'
        status.color = STATUS['good']
    save.add_widget(make_button('Save to my profile', save_list, primary=True))
    save.add_widget(status)
    return [use, save]
