"""Enter a PID by hand and save it to a car profile. Opened from the menu.

The user types the id, name, unit, a formula and the module. Each entry is checked as it is added, and nothing
is saved until every entry checks out (manual_pids.save). The formula can use the reply bytes A, B, C and D.
"""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput

from scanner import manual_pids, torque_csv
from settings_ui import spinner
from ui_kit import (GAP, MUTED, RAISED, STATUS, TEXT, Card, make_button, panel_label, section_title, stack)

MODULES = ('Auto', '7E0', '7E2', '7E3')


def _field(hint):
    return TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=dp(44),
                     background_color=RAISED, foreground_color=TEXT, hint_text_color=MUTED)


class PidEditor(ModalView):
    def __init__(self, profiles, folder, on_saved, **kwargs):
        super().__init__(size_hint=(0.94, 0.92), background_color=(0, 0, 0, 0.6), **kwargs)
        self.profiles = {p.name: p for p in profiles}
        self.folder, self.on_saved = folder, on_saved
        self.entries = []

        form = Card()
        form.add_widget(section_title('Manual PID'))
        form.add_widget(panel_label('Mode 01 (4 digits, e.g. 010C) or Mode 22 (6 digits, e.g. 22194F). The formula '
                                    'uses A, B, C or D for the reply bytes, e.g. (A*256+B)/4.', color=MUTED,
                                    font_size=dp(12)))
        self.profile_box = spinner(list(self.profiles), next(iter(self.profiles), ''))
        self.pid_box, self.name_box = _field('PID, e.g. 2219AA'), _field('Name')
        self.unit_box, self.equation_box = _field('Unit, e.g. kPa'), _field('Formula, e.g. A*2')
        self.low_box, self.high_box = _field('Min value'), _field('Max value')
        self.header_box = spinner(list(MODULES), 'Auto')
        for widget in (panel_label('Profile to save to', color=MUTED), self.profile_box, self.pid_box,
                       self.name_box, self.unit_box, self.equation_box, self.low_box, self.high_box,
                       panel_label('Module', color=MUTED), self.header_box):
            form.add_widget(widget)
        self.form_status = panel_label('', color=STATUS['bad'], font_size=dp(13))
        form.add_widget(self.form_status)
        form.add_widget(make_button('Add to the list', self.add_entry, primary=True))

        self.list_card = Card()
        self.list_card.add_widget(section_title('Entered for this profile'))
        self.list_rows = BoxLayout(orientation='vertical', spacing=GAP, size_hint_y=None)
        self.list_rows.bind(minimum_height=self.list_rows.setter('height'))
        self.list_card.add_widget(self.list_rows)

        save = Card()
        save.add_widget(make_button('Save to profile', self.save_to_profile, primary=True))
        self.save_status = panel_label('', color=STATUS['bad'], font_size=dp(13))
        save.add_widget(self.save_status)
        save.add_widget(make_button('Close', self.dismiss))

        self.profile_box.bind(text=lambda _box, name: self._select_profile(name))
        self.add_widget(stack(form, self.list_card, save))
        self._select_profile(self.profile_box.text)

    # --- the list -------------------------------------------------------------------------------

    def _select_profile(self, name):
        """Load what is already saved for the chosen profile, so new entries are added to it."""
        profile = self.profiles.get(name)
        if profile is None:
            return
        self.entries = [dict(row) for row in manual_pids.load(self.folder).get(profile.key, [])]
        self._redraw()

    def _redraw(self):
        self.list_rows.clear_widgets()
        if not self.entries:
            self.list_rows.add_widget(panel_label('Nothing entered for this profile yet.', color=MUTED))
            return
        for index, row in enumerate(self.entries):
            line = BoxLayout(size_hint_y=None, height=dp(60), spacing=GAP)
            label = Label(text=f'{row["pid"]}  {row["name"]}', color=TEXT, font_size=dp(14),
                          halign='left', valign='middle')   # wraps inside its column, so the name stays readable
            label.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))   # the text stays in its own column
            line.add_widget(label)
            remove = make_button('Remove', lambda i=index: self.remove_entry(i))
            remove.size_hint_x, remove.width = None, dp(110)
            line.add_widget(remove)
            self.list_rows.add_widget(line)

    def remove_entry(self, index):
        del self.entries[index]
        self._redraw()

    def add_entry(self):
        entry = {'pid': self.pid_box.text.strip().upper(), 'name': self.name_box.text.strip(),
                 'unit': self.unit_box.text.strip(), 'equation': self.equation_box.text.strip(),
                 'low': self.low_box.text.strip() or '0', 'high': self.high_box.text.strip() or '100',
                 'header': self.header_box.text}
        try:
            manual_pids.build(entry)     # check it now, so a bad row is caught before it is listed
        except torque_csv.Refused as exc:
            self.form_status.text = str(exc)
            self.form_status.color = STATUS['bad']
            return
        self.entries = [row for row in self.entries if row['pid'] != entry['pid']] + [entry]
        self.form_status.text = f'Added {entry["pid"]}. Add more, or save to the profile.'
        self.form_status.color = STATUS['good']
        self._redraw()

    def save_to_profile(self):
        profile = self.profiles.get(self.profile_box.text)
        if profile is None:
            self.save_status.text = 'Choose a profile first.'
            return
        try:
            saved = manual_pids.save(self.folder, profile.key, self.entries)
        except torque_csv.Refused as exc:
            self.save_status.text = f'Not saved: {exc}'
            self.save_status.color = STATUS['bad']
            return
        self.save_status.text = f'Saved {len(saved)} PID(s) to {profile.name}.'
        self.save_status.color = STATUS['good']
        self.on_saved(profile, saved)
