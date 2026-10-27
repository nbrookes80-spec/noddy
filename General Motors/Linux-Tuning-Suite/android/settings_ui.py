"""The Settings screen: pick the car's make and automatic transmission, or start from a whole vehicle profile.

Choosing a transmission loads its gear ratios and keeps the converter-lock gears within the gears it has.
Choosing a profile loads every Shift setting for that vehicle. Both recalculate the shift tables at once,
and the choice is remembered for next time (vehicles.py).
"""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner

import vehicles
from tunertoolpro import core
from ui_kit import MUTED, STATUS, TEXT, Card, make_button, panel_label, section_title, stack, style_button


def spinner(values, text):
    box = Spinner(text=text, values=values, size_hint_y=None, height=dp(48))
    style_button(box)
    return box


class SettingsScreen(BoxLayout):
    def __init__(self, shift, choice_path, version, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.shift, self.choice_path, self.version = shift, choice_path, version
        self.choice = vehicles.load(choice_path)
        self.on_changed = lambda: None

        car = Card()
        car.add_widget(section_title('Car and transmission'))
        car.add_widget(panel_label('Pick the make, then the automatic. The shift tables use its gear ratios.',
                                   color=MUTED, font_size=dp(13)))
        self.make_box = spinner(vehicles.MAKES, self.choice['make'])
        self.make_box.bind(text=self._make_changed)
        self.trans_box = spinner([], 'Choose a transmission')
        self.trans_box.bind(text=self._trans_changed)
        self.detail = panel_label('', color=MUTED, font_size=dp(13))
        self.apply_button = make_button('Use this transmission', self.apply_transmission, primary=True)
        for widget in (panel_label('Make', color=MUTED), self.make_box,
                       panel_label('Automatic transmission', color=MUTED), self.trans_box,
                       self.detail, self.apply_button):
            car.add_widget(widget)

        profile = Card()
        profile.add_widget(section_title('Start from a vehicle'))
        profile.add_widget(panel_label('Loads every Shift setting for that vehicle: tyres, axle, RPM, '
                                       'converter lock and shift feel. It replaces what is on the Shift '
                                       'screen now.', color=MUTED, font_size=dp(13)))
        names = core.profile_names()
        self.profile_box = spinner(names, self.choice['profile'] or names[0])
        profile.add_widget(self.profile_box)
        profile.add_widget(make_button('Load this vehicle', self.apply_profile))

        self.status = panel_label('', color=STATUS['good'], font_size=dp(13))
        about = Card()
        about.add_widget(section_title('About'))
        about.add_widget(panel_label(f'TunerToolPro {version}. Read-only: the app never writes to the car.',
                                     color=MUTED, font_size=dp(13)))
        self.add_widget(stack(car, profile, self.status, about))
        self._refill_transmissions(self.choice['transmission'])

    # --- the transmission list -------------------------------------------------------------------

    def _refill_transmissions(self, selected=''):
        listed = vehicles.transmissions(self.make_box.text)
        self.trans_box.values = [t.name for t in listed]
        self.trans_box.text = selected if selected in self.trans_box.values else 'Choose a transmission'
        self._show_detail()

    def _make_changed(self, _box, _text):
        self._refill_transmissions()

    def _trans_changed(self, _box, _text):
        self._show_detail()

    def _show_detail(self):
        found = vehicles.find(self.trans_box.text)
        self.apply_button.disabled = found is None
        if found is None:
            self.detail.text = ''
            return
        state = 'Ratios checked against the shared tuning data.' if found.verified else found.note
        self.detail.text = (f'{len(found.ratios)} gears, {found.drive}. Ratios {vehicles.ratios_text(found)}.\n'
                            f'{state}')

    # --- applying --------------------------------------------------------------------------------

    def apply_transmission(self):
        found = vehicles.find(self.trans_box.text)
        if found is None:
            return
        self.shift.apply_transmission(found)
        self.choice.update(make=self.make_box.text, transmission=found.name)
        vehicles.save(self.choice_path, self.choice)
        self.on_changed()
        self.status.text = f'Using {found.name} ({len(found.ratios)} gears). The shift tables have updated.'

    def apply_profile(self):
        name = self.profile_box.text
        self.shift.apply_profile(name)
        self.choice.update(profile=name, transmission='')
        vehicles.save(self.choice_path, self.choice)
        self._refill_transmissions()
        self.on_changed()
        self.status.text = f'Loaded {name}. The shift tables have updated.'

    def restore(self):
        """Re-apply what was chosen last time. Called once at start-up."""
        if self.choice['profile']:
            self.shift.apply_profile(self.choice['profile'])
        found = vehicles.find(self.choice['transmission'])
        if found:
            self.shift.apply_transmission(found)

    def summary(self):
        found = vehicles.find(self.choice['transmission'])
        return found.name if found else (self.choice['profile'] or core.profile_names()[0])
