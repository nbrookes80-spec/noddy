"""Draw the app icon and the four screen icons into android/icons/. Run: python3 make_icons.py

Pillow is needed (pip install pillow). The icons are plain shapes in one colour family so they read
the same on a dark screen.
"""

from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OUT = HERE / 'icons'
BG = (17, 22, 28, 255)
ACCENT = (245, 166, 35, 255)
LINE = (120, 200, 255, 255)
SIZE = 512


def canvas(size=SIZE):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img), size / 512.0


def shift_icon(size=SIZE):
    """Four gear-step bars rising to the right, like a shift-point chart."""
    img, d, k = canvas(size)
    d.rounded_rectangle([40 * k, 40 * k, 472 * k, 472 * k], radius=72 * k, fill=BG)
    for i, height in enumerate((120, 200, 280, 360)):
        x = (110 + i * 92) * k
        d.rounded_rectangle([x, (430 - height) * k, x + 60 * k, 430 * k], radius=10 * k, fill=ACCENT)
    return img


def dyno_icon(size=SIZE):
    """A torque-curve line on axes."""
    img, d, k = canvas(size)
    d.rounded_rectangle([40 * k, 40 * k, 472 * k, 472 * k], radius=72 * k, fill=BG)
    d.line([(100 * k, 400 * k), (100 * k, 120 * k)], fill=LINE, width=int(12 * k))
    d.line([(100 * k, 400 * k), (420 * k, 400 * k)], fill=LINE, width=int(12 * k))
    curve = [(130, 360), (190, 250), (260, 170), (330, 160), (390, 230), (420, 290)]
    d.line([(x * k, y * k) for x, y in curve], fill=ACCENT, width=int(26 * k), joint='curve')
    return img


def link_icon(size=SIZE):
    """A plug with waves: a scan adapter link."""
    img, d, k = canvas(size)
    d.rounded_rectangle([40 * k, 40 * k, 472 * k, 472 * k], radius=72 * k, fill=BG)
    d.rounded_rectangle([190 * k, 230 * k, 322 * k, 370 * k], radius=24 * k, fill=ACCENT)
    d.rectangle([215 * k, 170 * k, 235 * k, 230 * k], fill=ACCENT)
    d.rectangle([277 * k, 170 * k, 297 * k, 230 * k], fill=ACCENT)
    d.rectangle([246 * k, 370 * k, 266 * k, 420 * k], fill=ACCENT)
    for r in (70, 110):
        d.arc([256 * k - r * k, 300 * k - r * k, 256 * k + r * k, 300 * k + r * k],
              start=-40, end=40, fill=LINE, width=int(12 * k))
    return img


def upload_icon(size=SIZE):
    """An arrow going up into a tray: load a CSV file."""
    img, d, k = canvas(size)
    d.rounded_rectangle([40 * k, 40 * k, 472 * k, 472 * k], radius=72 * k, fill=BG)
    d.line([(256 * k, 360 * k), (256 * k, 130 * k)], fill=ACCENT, width=int(30 * k))
    d.polygon([(256 * k, 90 * k), (180 * k, 175 * k), (332 * k, 175 * k)], fill=ACCENT)
    d.line([(130 * k, 330 * k), (130 * k, 400 * k), (382 * k, 400 * k), (382 * k, 330 * k)],
           fill=LINE, width=int(26 * k), joint='curve')
    return img


def save_all():
    OUT.mkdir(exist_ok=True)
    shift_icon().save(OUT / 'app_icon.png')
    for name, make in (('shift', shift_icon), ('dyno', dyno_icon), ('link', link_icon),
                       ('upload', upload_icon)):
        make(size=128).save(OUT / f'{name}.png')
    return sorted(p.name for p in OUT.glob('*.png'))


if __name__ == '__main__':
    print('Wrote', ', '.join(save_all()), 'to', OUT)
