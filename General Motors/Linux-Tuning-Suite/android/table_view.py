"""The four shift tables as text for the screen: coloured by grade, with the car's place marked.

Each cell is seven characters. A marker character after the number says the same thing as the
colour, for anyone who cannot tell green from red: space is good, ~ is yellow, ! is red. A * marks
the cell the car is in right now while live data is streaming. No Kivy here, so it can be tested.
"""

from tunertoolpro import core

HEX = {'good': '66cc8c', 'ok': 'ffd940', 'bad': 'ff6661', 'off': '6b7684'}
MARKER = {'good': ' ', 'ok': '~', 'bad': '!', 'off': ' '}
DISABLED_MPH = 255.0
LABEL_WIDTH = 8


def _cursor_cells(cursor, counts):
    """{table: (row, col)} for the cell the car is in, from {'gear': 1-based, 'tps': percent}."""
    if not cursor:
        return {}
    axis = core.tps_axis()
    step = axis[1] - axis[0]
    col = min(max(int(round(cursor['tps'] / step)), 0), len(axis) - 1)
    gear = cursor['gear']
    wanted = {'upshift': gear - 1, 'downshift': gear - 2, 'tcc_unlock': gear - 1, 'tcc_lock': gear - 1}
    return {name: (row, col) for name, row in wanted.items() if 0 <= row < counts[name]}


def table_blocks(tables, levels=None, cursor=None):
    """The four shift tables as (title, text) pairs. With levels the text carries colour markup."""
    blocks = []
    tps = [f'{v:g}%' for v in core.tps_axis()]
    gear_labels = [f'Gear {g + 1}' for g in range(tables['n_gears'])]
    shift_labels = [f'{g + 1}-{g + 2}' for g in range(len(tables['upshift']))]
    sections = [('upshift', 'Upshift MPH', shift_labels), ('downshift', 'Downshift MPH', shift_labels),
                ('tcc_unlock', 'TCC unlock MPH', gear_labels), ('tcc_lock', 'TCC lock MPH', gear_labels)]
    here = _cursor_cells(cursor, {name: len(tables[name]) for name, _t, _l in sections})
    for name, title, labels in sections:
        lines = [' ' * LABEL_WIDTH + ' '.join(f'{t:>7}' for t in tps)]
        for r, (label, row) in enumerate(zip(labels, tables[name])):
            cells = []
            for c, mph in enumerate(row):
                level = levels[name][r][c] if levels else 'good'
                number = '    --' if mph >= DISABLED_MPH else f'{mph:6.1f}'
                marker = '*' if here.get(name) == (r, c) else MARKER[level]
                cell = number + marker
                cells.append(f'[color=#{HEX[level]}]{cell}[/color]' if levels else cell)
            lines.append(f'{label:>{LABEL_WIDTH}}' + ' '.join(cells))
        blocks.append((title, '\n'.join(lines)))
    return blocks
