"""The editor opened by a long press on a sensor: name, unit, range, zones (red, yellow, blue, green and where each
starts or ends), a colour, and for a PID you entered yourself also its equation and module. Display choices are
saved to the PidViews file; a PID you entered is saved back to its car profile through `save_manual`, which checks
it before anything is written.

The numbers are shown in the units the dashboard uses (C or F, kPa or psi...) and saved in the sensor's own unit.
Typing a unit of your own into the Unit box means the numbers are in that unit and nothing is converted."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput

from tunertoolpro.scanner import manual_pids, pid_view, torque_csv
from settings_ui import spinner
from ui_kit import (GAP, MUTED, RAISED, STATUS, TEXT, Card, button_row, make_button, panel_label,
                    section_title, stack)

MODULES = ('Auto', '7E0', '7E2', '7E3')
# The zone boxes, top to bottom: the key saved in PidViews and the hint shown in an empty box.
ZONE_BOXES = (('red_low', 'Empty for none'), ('warn_low', 'Empty for none'), ('cold', 'Empty for none'),
              ('good', 'Empty for none'), ('good_to', 'Empty for none'), ('warn', 'Empty for none'),
              ('redline', 'Empty for none'))
# The colour buttons: a name, and the colour saved (None keeps the theme's own colour).
SWATCHES = (('White', '#FFFFFF'), ('Cyan', '#00E5FF'), ('Green', '#66CC8C'), ('Orange', '#FF9800'),
            ('Magenta', '#FF4DD2'), ('None', None))


def _field(hint, text=''):
    return TextInput(text=text, hint_text=hint, multiline=False, size_hint_y=None, height=dp(40),
                     font_size=dp(15), padding=(dp(10), dp(10)),
                     background_color=RAISED, foreground_color=TEXT, hint_text_color=MUTED)


def _show(number):
    return '' if number is None else f'{number:g}'


class PidEditPopup(ModalView):
    def __init__(self, pid, views, manual_entry, save_manual, done, **kwargs):
        super().__init__(size_hint=(0.94, 0.92), background_color=(0, 0, 0, 0.6), **kwargs)
        self.pid, self.views, self.manual, self.save_manual, self.done = pid, views, manual_entry, save_manual, done
        shown = views.apply(pid)

        form = Card()
        form.add_widget(section_title(f'Edit {pid.pid}'))
        form.add_widget(panel_label('Changes how this sensor is shown. Leave a zone empty for none.',
                                    color=MUTED, font_size=dp(12)))
        self.shown_unit, self.back = shown['unit'], shown['back']
        self.name_box, self.unit_box = _field('Name', shown['name']), _field('Unit', shown['unit'])
        self.low_box, self.high_box = _field('Minimum', _show(shown['low'])), _field('Maximum', _show(shown['high']))
        widgets = []
        for label, box in (('Name', self.name_box), ('Unit', self.unit_box), ('Minimum (gauge starts here)', self.low_box),
                           ('Maximum (gauge ends here)', self.high_box)):
            widgets += [panel_label(label, color=MUTED, font_size=dp(12)), box]
        widgets.append(section_title('Zones'))
        unit_note = f'Numbers are in {shown["unit"]}.' if shown['unit'] else 'Numbers are in the sensor\'s own unit.'
        widgets.append(panel_label(f'Red is for danger, yellow for take care, green for good, blue for cold. {unit_note}',
                                   color=MUTED, font_size=dp(12)))
        self.zone_boxes = {}
        for key, hint in ZONE_BOXES:
            self.zone_boxes[key] = _field(hint, _show(shown[key]))
            widgets += [panel_label(pid_view.ZONE_LABELS[key], color=MUTED, font_size=dp(12)), self.zone_boxes[key]]
        self.color = shown.get('color')
        self.swatches = {}
        widgets += [panel_label('Colour of the number and gauge', color=MUTED, font_size=dp(12)), self._swatch_row()]
        if manual_entry is not None:
            self.equation_box = _field('Equation, e.g. (A*256+B)/4', str(manual_entry.get('equation', '')))
            self.module_box = spinner(list(MODULES), str(manual_entry.get('header') or 'Auto'))
            widgets += [panel_label('Equation (uses the reply bytes A, B, C, D)', color=MUTED), self.equation_box,
                        panel_label('Module the request is sent to', color=MUTED), self.module_box]
        elif pid.source == 'CAN import':
            widgets.append(panel_label(f'{pid.pid} is imported from a CAN log. Nothing is sent to the car for it; '
                                       'only its name, range and display can be changed.',
                                       color=MUTED, font_size=dp(12)))
        else:
            widgets.append(panel_label(f'{pid.pid} is a built-in sensor: its equation and module are fixed. '
                                       'Long press a PID you entered yourself to change those.',
                                       color=MUTED, font_size=dp(12)))
        for widget in widgets:
            form.add_widget(widget)
        self.status = panel_label('', color=STATUS['bad'], font_size=dp(13))
        form.add_widget(self.status)
        form.add_widget(make_button('Back to the original name and range', self.reset))
        body = BoxLayout(orientation='vertical', spacing=GAP, padding=GAP)
        body.add_widget(stack(form))
        body.add_widget(button_row(make_button('Close', self.dismiss), make_button('Save', self.save, primary=True)))
        self.add_widget(body)

    def _swatch_row(self):
        row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(4))
        for name, colour in SWATCHES:
            button = make_button(name, lambda c=colour: self.pick_colour(c))
            button.height, button.font_size = dp(44), dp(11)
            if colour is not None:
                button.background_color = pid_view.rgba(colour)
                button.color = (0, 0, 0, 1)
            self.swatches[colour] = button
            row.add_widget(button)
        self.pick_colour(self.color)
        return row

    def pick_colour(self, colour):
        """Choose a colour for the number and gauge (None for the theme's own). The chosen button is bold and bracketed."""
        self.color = colour
        for key, button in self.swatches.items():
            name = next(n for n, c in SWATCHES if c == key)
            chosen = key == colour
            button.text, button.bold = (f'[{name}]' if chosen else name), chosen

    def _number(self, box, label, allow_empty=False):
        text = box.text.strip()
        if not text and allow_empty:
            return None
        try:
            return float(text)
        except ValueError:
            raise ValueError(f'{label} must be a number.') from None

    def save(self):
        try:
            unit = self.unit_box.text.strip()
            own_unit = bool(unit) and unit != self.shown_unit      # a unit typed in: the numbers are in it, unconverted
            back = (lambda value: value) if own_unit else self.back
            low, high = self._number(self.low_box, 'The minimum'), self._number(self.high_box, 'The maximum')
            zones = {key: self._number(self.zone_boxes[key], pid_view.ZONE_LABELS[key], allow_empty=True)
                     for key, _hint in ZONE_BOXES}
            if not low < high:
                raise ValueError('The minimum must be less than the maximum.')
            problems = pid_view.zone_problems(zones)
            if problems:
                raise ValueError(' '.join(problems))
            low, high = round(back(low), 6), round(back(high), 6)
            zones = {key: None if x is None else round(back(x), 6) for key, x in zones.items()}
            if self.manual is not None:
                entry = dict(self.manual, name=self.name_box.text.strip(), unit=unit if own_unit else self.pid.unit,
                             equation=self.equation_box.text.strip(), header=self.module_box.text,
                             low=_show(low), high=_show(high))
                self.save_manual(entry)       # raises torque_csv.Refused when the equation or module is no good
        except (ValueError, torque_csv.Refused) as exc:
            self.status.text = str(exc)
            return
        self.views.update(self.pid.pid, name=self.name_box.text.strip() or None,
                          unit=unit if own_unit and unit != self.pid.unit else None,
                          low=low, high=high, color=self.color, **zones)
        self.dismiss()
        self.done()

    def reset(self):
        self.views.reset(self.pid.pid)
        self.dismiss()
        self.done()
