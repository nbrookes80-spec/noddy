# TunerToolPro design template

The app uses one palette, defined in `app/tunertoolpro/gui/theme.py` as `PALETTE`. Change a
colour there and every tab updates. Nothing else in the code should hard-code a colour.

## Colour tokens

| Token | Value | Used for |
|---|---|---|
| `window` | `#0d0f24` | Window and tab background (midnight indigo) |
| `base` | `#171a38` | Text boxes, tables, inputs |
| `alt` | `#222650` | Tab bars, table headers, secondary surfaces |
| `text` | `#f5f7ff` | Main text |
| `muted` | `#aab1e0` | Hints, notes, secondary labels |
| `accent` | `#ff2e7e` | Primary buttons (start of gradient), selected tab |
| `accent2` | `#ff9f1c` | Primary buttons (end of gradient) |
| `accent_hover` | `#ff5c9a` | Primary button on hover |
| `highlight` | `#00e5ff` | Group titles, secondary buttons, focus and selection |
| `good` | `#2bff9a` | Success, saved, consistent |
| `warn` | `#ffc247` | Check this, possible problem |
| `bad` | `#ff4d6d` | Error, contradictory inputs |
| `border` | `#3d4386` | Borders and gridlines |

## Components

- **Primary button:** the default `QPushButton`. Pink-to-orange gradient, bold white text.
  Use it for the one main action on a tab (Calculate, Ask, Save vehicle).
- **Secondary button:** set the property `role` to `secondary`. Dark fill, cyan border and text.
  Use it for supporting actions (Check consistency, Import, Reject).
- **Labels with meaning:** set the property `role` to `good`, `warn`, `bad` or `muted` on a
  `QLabel`. The stylesheet colours it.
- **Icons:** `gui/theme.py` maps a short name (`calculate`, `save`, `apply`, `reject`, `ask`, ...)
  to a standard Qt icon. Use `icon(widget, 'name')` so the set stays in one place.
- **Tabs:** the selected tab is filled with `accent`. Tab order is listed in
  `gui/main_window.py`.

## Accessibility

- Text on `window`, `base` and `alt` is at least 4.5:1 for normal text (the light `text` colour on
  the dark backgrounds). Check any new colour with a contrast checker before adding it.
- Status is never shown by colour alone. Findings have a text level ("Error", "Check", "Note")
  next to the colour.

## Changing the palette

1. Edit the value in `PALETTE` in `app/tunertoolpro/gui/theme.py`.
2. If you add a token, use it in `apply()` and list it in the table above.
3. Run the GUI tests (`QT_QPA_PLATFORM=offscreen python3 -m unittest tests.test_gui`) and look at
   the Vehicle and AI Assistant tabs, which show most of the components.
