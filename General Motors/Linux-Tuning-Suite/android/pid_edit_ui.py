"""The editor opened by a long press on a sensor: name, unit, range, red line, and for a PID you entered
yourself also its equation and module. Display choices are saved to the PidViews file; a PID you entered is
saved back to its car profile through `save_manual`, which checks it before anything is written."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput

from scanner import manual_pids, torque_csv
from settings_ui import spinner
from ui_kit import GAP, MUTED, RAISED, STATUS, TEXT, Card, button_row, make_button, panel_label, section_title, stack

MODULES = ('Auto', '7E0', '7E2', '7E3')


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
        form.add_widget(panel_label('Changes how this sensor is shown. Leave the red line empty for none.',
                                    color=MUTED, font_size=dp(12)))
        self.name_box, self.unit_box = _field('Name', shown['name']), _field('Unit', shown['unit'])
        self.low_box, self.high_box = _field('Minimum', _show(shown['low'])), _field('Maximum', _show(shown['high']))
        self.red_box = _field('Empty for no red line', _show(shown['redline']))
        widgets = []
        for label, box in (('Name', self.name_box), ('Unit', self.unit_box), ('Minimum (gauge starts here)', self.low_box),
                           ('Maximum (gauge ends here)', self.high_box),
                           ('Red line (the gauge turns red from this value)', self.red_box)):
            widgets += [panel_label(label, color=MUTED, font_size=dp(12)), box]
        if manual_entry is not None:
            self.equation_box = _field('Equation, e.g. (A*256+B)/4', str(manual_entry.get('equation', '')))
            self.module_box = spinner(list(MODULES), str(manual_entry.get('header') or 'Auto'))
            widgets += [panel_label('Equation (uses the reply bytes A, B, C, D)', color=MUTED), self.equation_box,
                        panel_label('Module the request is sent to', color=MUTED), self.module_box]
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
            low, high = self._number(self.low_box, 'The minimum'), self._number(self.high_box, 'The maximum')
            redline = self._number(self.red_box, 'The red line', allow_empty=True)
            if not low < high:
                raise ValueError('The minimum must be less than the maximum.')
            if self.manual is not None:
                entry = dict(self.manual, name=self.name_box.text.strip(), unit=self.unit_box.text.strip(),
                             equation=self.equation_box.text.strip(), header=self.module_box.text,
                             low=_show(low), high=_show(high))
                self.save_manual(entry)       # raises torque_csv.Refused when the equation or module is no good
        except (ValueError, torque_csv.Refused) as exc:
            self.status.text = str(exc)
            return
        self.views.update(self.pid.pid, name=self.name_box.text.strip() or None, unit=self.unit_box.text.strip() or None,
                          low=low, high=high, redline=redline)
        self.dismiss()
        self.done()

    def reset(self):
        self.views.reset(self.pid.pid)
        self.dismiss()
        self.done()
