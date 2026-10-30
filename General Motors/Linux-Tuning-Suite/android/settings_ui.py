"""The Settings screen: pick the car's make and automatic transmission, or start from a whole vehicle profile.

Choosing a transmission loads its gear ratios and keeps the converter-lock gears within the gears it has.
Choosing a profile loads every Shift setting for that vehicle. Both recalculate the shift tables at once,
and the choice is remembered for next time (vehicles.py).
"""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner

from tunertoolpro import trans_data
from tunertoolpro import vehicles
from tunertoolpro import core
from ui_kit import MUTED, STATUS, TEXT, Card, make_button, panel_label, section_title, stack, style_button


def spinner(values, text):
    # One line that ends in "..." when the choice is too long, instead of running past the box.
    box = Spinner(text=text, values=values, size_hint_y=None, height=dp(48), shorten=True, shorten_from='right')
    box.bind(size=lambda w, _: setattr(w, 'text_size', (w.width - dp(24), w.height)))
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
        self.car_status = panel_label('', color=STATUS['good'], font_size=dp(13))
        for widget in (panel_label('Make', color=MUTED), self.make_box,
                       panel_label('Automatic transmission', color=MUTED), self.trans_box,
                       self.apply_button, self.car_status, self.detail):
            car.add_widget(widget)

        profile = Card()
        profile.add_widget(section_title('Start from a vehicle'))
        profile.add_widget(panel_label('Loads every Shift setting for that vehicle: tyres, axle, RPM, '
                                       'converter lock and shift feel. It replaces what is on the Shift '
                                       'screen now.', color=MUTED, font_size=dp(13)))
        names = core.profile_names()
        self.profile_box = spinner(names, self.choice['profile'] or names[0])
        profile.add_widget(self.profile_box)
        self.load_button = make_button('Load this vehicle', self.apply_profile, primary=True)
        profile.add_widget(self.load_button)
        self.profile_status = panel_label('', color=STATUS['good'], font_size=dp(13))
        profile.add_widget(self.profile_status)

        about = Card()
        about.add_widget(section_title('About'))
        about.add_widget(panel_label(f'TunerToolPro {version}. Read-only: the app never writes to the car.',
                                     color=MUTED, font_size=dp(13)))
        self.add_widget(stack(car, profile, about))
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
        self.apply_button.text = 'Use this transmission' if found else 'Pick a transmission above first'
        if found is None:
            self.detail.text = ''
            return
        state = 'Ratios checked against the shared tuning data.' if found.verified else found.note
        self.detail.text = (f'{len(found.ratios)} gears, {found.drive}. Ratios {vehicles.ratios_text(found)}.\n'
                            f'{state}\n\n{trans_data.summary(trans_data.for_transmission(found))}')

    # --- applying --------------------------------------------------------------------------------

    def apply_transmission(self):
        found = vehicles.find(self.trans_box.text)
        if found is None:
            return
        data = self.shift.apply_transmission(found)
        self.choice.update(make=self.make_box.text, transmission=found.name)
        vehicles.save(self.choice_path, self.choice)
        self.on_changed()
        self.profile_status.text = ''
        self.car_status.text = (f'Loaded {found.name}: {len(found.ratios)} gears, shift delays, lead and converter-lock '
                                f'rules ({"derived" if data.derived else "Blue Cat"}). The shift tables have updated.')

    def apply_profile(self):
        name = self.profile_box.text
        self.shift.apply_profile(name)
        from tunertoolpro.engines import constants
        trans = constants.STARTER_PROFILES[name]['trans_name']
        self.choice.update(profile=name, transmission=trans, make='GM')
        vehicles.save(self.choice_path, self.choice)
        self.make_box.text = 'GM'
        self._refill_transmissions(trans)
        self.on_changed()
        self.car_status.text = ''
        self.profile_status.text = f'Loaded {name} with its {trans} data. The shift tables have updated.'

    def restore(self):
        """Re-apply what was chosen last time. Called once at start-up."""
        if self.choice['profile']:
            self.shift.apply_profile(self.choice['profile'])
        found = vehicles.find(self.choice['transmission'])
        if found and found.name != self._profile_transmission(self.choice['profile']):
            self.shift.apply_transmission(found)

    @staticmethod
    def _profile_transmission(name):
        from tunertoolpro.engines import constants
        return constants.STARTER_PROFILES[name]['trans_name'] if name in constants.STARTER_PROFILES else None

    def summary(self):
        found = vehicles.find(self.choice['transmission'])
        return found.name if found else (self.choice['profile'] or core.profile_names()[0])
