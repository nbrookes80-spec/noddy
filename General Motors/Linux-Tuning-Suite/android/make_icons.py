"""Draw the app icon and the screen icons into android/icons/. Run: python3 make_icons.py

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


def _tile(d, k):
    d.rounded_rectangle([40 * k, 40 * k, 472 * k, 472 * k], radius=72 * k, fill=BG)


def scan_icon(size=SIZE):
    """A round gauge with a needle: live scanner data."""
    img, d, k = canvas(size)
    _tile(d, k)
    d.arc([96 * k, 120 * k, 416 * k, 440 * k], start=150, end=390, fill=LINE, width=int(26 * k))
    d.arc([96 * k, 120 * k, 416 * k, 440 * k], start=330, end=390, fill=ACCENT, width=int(26 * k))
    d.line([(256 * k, 300 * k), (340 * k, 215 * k)], fill=ACCENT, width=int(24 * k))
    d.ellipse([228 * k, 272 * k, 284 * k, 328 * k], fill=ACCENT)
    return img


def app_icon(size=SIZE):
    """The app icon: a tachometer arc over three rising shift bars."""
    img, d, k = canvas(size)
    _tile(d, k)
    d.arc([86 * k, 86 * k, 426 * k, 426 * k], start=160, end=380, fill=LINE, width=int(24 * k))
    d.arc([86 * k, 86 * k, 426 * k, 426 * k], start=320, end=380, fill=ACCENT, width=int(24 * k))
    d.line([(256 * k, 270 * k), (336 * k, 190 * k)], fill=ACCENT, width=int(22 * k))
    for i, height in enumerate((70, 110, 150)):
        x = (160 + i * 70) * k
        d.rounded_rectangle([x, (430 - height) * k, x + 46 * k, 430 * k], radius=8 * k, fill=ACCENT)
    return img


def demo_icon(size=SIZE):
    """A play triangle in a ring: run the demo."""
    img, d, k = canvas(size)
    _tile(d, k)
    d.ellipse([110 * k, 110 * k, 402 * k, 402 * k], outline=LINE, width=int(22 * k))
    d.polygon([(220 * k, 180 * k), (220 * k, 332 * k), (346 * k, 256 * k)], fill=ACCENT)
    return img


def codes_icon(size=SIZE):
    """A warning triangle: stored trouble codes."""
    img, d, k = canvas(size)
    _tile(d, k)
    d.polygon([(256 * k, 110 * k), (410 * k, 390 * k), (102 * k, 390 * k)], outline=ACCENT,
              width=int(24 * k))
    d.line([(256 * k, 200 * k), (256 * k, 290 * k)], fill=ACCENT, width=int(26 * k))
    d.ellipse([240 * k, 318 * k, 272 * k, 350 * k], fill=ACCENT)
    return img


def log_icon(size=SIZE):
    """Three text lines: the traffic log."""
    img, d, k = canvas(size)
    _tile(d, k)
    for i, length in enumerate((250, 180, 220)):
        y = (170 + i * 80) * k
        d.rounded_rectangle([130 * k, y, (130 + length) * k, y + 30 * k], radius=14 * k,
                            fill=ACCENT if i == 0 else LINE)
    return img


def live_icon(size=SIZE):
    """A pulse trace with a live dot: data streaming from the car."""
    img, d, k = canvas(size)
    _tile(d, k)
    trace = [(90, 270), (170, 270), (205, 190), (255, 370), (300, 150), (340, 270), (410, 270)]
    d.line([(x * k, y * k) for x, y in trace], fill=LINE, width=int(22 * k), joint='curve')
    d.ellipse([384 * k, 120 * k, 432 * k, 168 * k], fill=ACCENT)
    return img


def agent_icon(size=SIZE):
    """A speech bubble with three dots: your AI agent talking to the app."""
    img, d, k = canvas(size)
    _tile(d, k)
    d.rounded_rectangle([96 * k, 120 * k, 416 * k, 340 * k], radius=56 * k, outline=LINE, width=int(22 * k))
    d.polygon([(170 * k, 336 * k), (170 * k, 410 * k), (250 * k, 336 * k)], fill=LINE)
    for i in range(3):
        cx = (186 + i * 70) * k
        d.ellipse([cx - 20 * k, 210 * k, cx + 20 * k, 250 * k], fill=ACCENT)
    return img


def save_all():
    OUT.mkdir(exist_ok=True)
    app_icon().save(OUT / 'app_icon.png')
    for name, make in (('shift', shift_icon), ('dyno', dyno_icon), ('link', link_icon),
                       ('upload', upload_icon), ('scan', scan_icon),
                       ('demo', demo_icon), ('codes', codes_icon), ('log', log_icon),
                       ('live', live_icon), ('agent', agent_icon)):
        make(size=128).save(OUT / f'{name}.png')
    return sorted(p.name for p in OUT.glob('*.png'))


if __name__ == '__main__':
    print('Wrote', ', '.join(save_all()), 'to', OUT)
