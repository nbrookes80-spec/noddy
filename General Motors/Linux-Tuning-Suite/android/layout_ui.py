"""Full-page layouts on the Live and Scan screens.

  PageBoard     places the sensor cards of one full-screen page where scanner/page_layout.slots says
  FullPage      a page: a title strip, the board, and a Previous / Next / Page layout bar
  LayoutChooser lists the templates as small drawn previews and applies one to this page or to all pages

Which cell each sensor gets, and what the saved choices are, is decided in the shared core (page_layout.py); this
file only draws and places. Nothing here touches the car.
"""

from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from tunertoolpro.scanner import page_layout
from ui_kit import ACCENT, BG, BORDER, GAP, MUTED, RAISED, TEXT, Card, make_button, panel_label, section_title, style_button

CELL_GAP = dp(8)          # space between the cards of a page
TITLE_HEIGHT = dp(36)     # the strip above the board; the Record, HUD and Exit buttons float over its right end
BAR_HEIGHT = dp(44)


class PageBoard(Widget):
    """The cards of one page, each in its cell. The cells follow the board's size, so turning the phone re-lays
    the page out."""

    def __init__(self, cards, template, **kwargs):
        super().__init__(**kwargs)
        self.cards = list(cards)
        self.template = template
        for card in self.cards:
            card.fit_cell()
            self.add_widget(card)
        self.bind(pos=self.place, size=self.place)

    def place(self, *_):
        if self.width <= 0 or self.height <= 0:
            return
        cells = page_layout.slots(self.template, len(self.cards), aspect=self.width / self.height)
        pixels = page_layout.to_pixels(cells, self.x, self.y, self.width, self.height, CELL_GAP)
        for card, (x, y, w, h) in zip(self.cards, pixels):
            card.pos, card.size = (x, y), (w, h)


class FullPage(BoxLayout):
    """One full-screen page. `on_turn(step)` and `on_layout()` are the screen's own actions."""

    def __init__(self, cards, page, total, template, on_turn, on_layout, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        title = Label(text=f'Page {page + 1} of {total}', color=MUTED, font_size=dp(12), halign='left',
                      valign='middle', size_hint_y=None, height=TITLE_HEIGHT, padding=(GAP, 0))
        title.bind(size=lambda w, _: setattr(w, 'text_size', (w.width - dp(24), w.height)))
        self.board = PageBoard(cards, template)
        bar = BoxLayout(size_hint_y=None, height=BAR_HEIGHT, spacing=dp(8), padding=(GAP, 0, GAP, dp(4)))
        for text, action in (('Previous', lambda: on_turn(-1)), ('Next', lambda: on_turn(1)),
                             ('Page layout', on_layout)):
            button = make_button(text, action)
            button.height = BAR_HEIGHT - dp(4)
            button.disabled = total < 2 and text != 'Page layout'
            bar.add_widget(button)
        for widget in (title, self.board, bar):
            self.add_widget(widget)


class LayoutPreview(Widget):
    """A template drawn as the rectangles of `page_layout.slots`: the first sensor's cell is lit."""

    def __init__(self, template, count, aspect, **kwargs):
        super().__init__(**kwargs)
        self.template, self.count, self.aspect = template, count, aspect
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        self.canvas.clear()
        if self.width <= 0 or self.height <= 0:
            return
        cells = page_layout.slots(self.template, self.count, aspect=self.aspect)
        with self.canvas:
            for i, (x, y, w, h) in enumerate(page_layout.to_pixels(cells, self.x, self.y, self.width, self.height,
                                                                   dp(4))):
                Color(*(ACCENT if i == 0 else BORDER))
                RoundedRectangle(pos=(x, y), size=(w, h), radius=[dp(3)])


class TemplateTile(ButtonBehavior, Card):
    """One template in the chooser: its picture and name. The chosen one has an accent border."""

    def __init__(self, template, count, aspect, chosen, on_pick, **kwargs):
        super().__init__(size_hint_y=None, height=dp(128), padding=dp(8), spacing=dp(4), **kwargs)
        self.template = template
        self._on_pick = on_pick
        name = page_layout.TEMPLATES[template]['name']
        if not page_layout.supports(template, count):
            name += f' (grid for {count})'
        label = Label(text=name, color=TEXT, font_size=dp(12), size_hint_y=None, height=dp(20), shorten=True,
                      shorten_from='right')
        label.bind(size=lambda w, _: setattr(w, 'text_size', (w.width, w.height)))
        self.add_widget(LayoutPreview(template, count, aspect))
        self.add_widget(label)
        self.set_border(ACCENT if chosen else BORDER)

    def _fit_height(self, *_):
        pass

    def on_release(self):
        self._on_pick(self.template)


class LayoutChooser(ModalView):
    """Pick a template for the page being looked at, or for all pages.

    `count` is the number of sensors on the page, `page` its index from 0, `current` the template it has now.
    `on_pick(template_id, all_pages)` does the saving; the chooser closes after it is called."""

    def __init__(self, count, page, current, on_pick, all_pages=False, aspect=None, **kwargs):
        super().__init__(size_hint=(0.92, 0.9), background_color=(0, 0, 0, 0.6), **kwargs)
        self.count, self.page, self.on_pick = count, page, on_pick
        aspect = aspect or Window.width / max(Window.height, 1)
        box = Card()
        box.add_widget(section_title('Page layout'))
        box.add_widget(panel_label('Choose how the sensors of a full-screen page are placed. The lit rectangle is the '
                                   'first sensor of the page.', color=MUTED, font_size=dp(12)))
        self.this_page = ToggleButton(text=f'This page (page {page + 1})', group=f'layout_scope_{id(self)}',
                                      state='normal' if all_pages else 'down', allow_no_selection=False)
        self.every_page = ToggleButton(text='All pages', group=f'layout_scope_{id(self)}',
                                       state='down' if all_pages else 'normal', allow_no_selection=False)
        scope = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        for button in (self.this_page, self.every_page):
            style_button(button, primary=button.state == 'down')
            button.bind(state=self._scope_changed)
            scope.add_widget(button)
        box.add_widget(scope)
        grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        self.tiles = []
        for template in page_layout.TEMPLATES:
            tile = TemplateTile(template, count, aspect, template == current, self.pick)
            self.tiles.append(tile)
            grid.add_widget(tile)
        box.add_widget(grid)
        box.add_widget(make_button('Close', self.dismiss, primary=True))
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        scroll.add_widget(box)
        self.add_widget(scroll)

    @property
    def all_pages(self):
        return self.every_page.state == 'down'

    @staticmethod
    def _scope_changed(button, _state):
        button.background_color = ACCENT if button.state == 'down' else RAISED
        button.color = BG if button.state == 'down' else TEXT

    def pick(self, template):
        self.dismiss()
        self.on_pick(template, self.all_pages)
