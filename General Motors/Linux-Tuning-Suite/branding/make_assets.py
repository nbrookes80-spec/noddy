"""Rebuilds the cut-out car pictures the apps show on the splash screen and in the header.

Run once when the source photos change; the finished PNGs are what ship. Needs a throwaway virtual
environment:  pip install "rembg[cpu]" onnxruntime pillow numpy opencv-python-headless
The first run downloads the isnet-general-use model (about 170 MB) to ~/.u2net.

    python branding/make_assets.py app/tunertoolpro/gui/assets android/assets

Licence plates are blurred before the cut-out. Every picture gets the same auto-adjust.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source'

# name -> (source file, plate box to blur or None, longest side to ship)
JOBS = {
    'logo_car.png': ('car_logo_gold.png', None, 640),    # plate is already hidden in this photo
    'intro_side.png': ('car_side.jpg', (160, 545, 255, 640), 1280),
    'intro_bay.png': ('car_bay.jpg', None, 1280),
}


def blur_box(img, box, radius=14):
    img = img.copy()
    img.paste(img.crop(box).filter(ImageFilter.GaussianBlur(radius)), box)
    return img


def clean_mask(alpha):
    """Hard threshold, drop specks and holes, then feather the edge slightly."""
    import cv2
    mask = (np.asarray(alpha) > 140).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    keep = np.zeros_like(mask)
    for i in range(1, count):
        if stats[i, cv2.CC_STAT_AREA] >= 0.02 * mask.sum():
            keep[labels == i] = 1
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    out = Image.fromarray(keep * 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.5))
    return out


def auto_adjust(rgb):
    rgb = ImageOps.autocontrast(rgb, cutoff=0.5)
    rgb = ImageEnhance.Color(rgb).enhance(1.12)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.06)
    return rgb.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=3))


def build(name, session):
    from rembg import remove
    source, plate, longest = JOBS[name]
    photo = Image.open(SOURCE / source).convert('RGB')
    if plate:
        photo = blur_box(photo, plate)
    cut = remove(photo, session=session)
    alpha = clean_mask(cut.getchannel('A'))
    car = auto_adjust(photo).convert('RGBA')
    car.putalpha(alpha)
    car = car.crop(alpha.getbbox())
    scale = longest / max(car.size)
    if scale < 1:
        car = car.resize((round(car.width * scale), round(car.height * scale)), Image.LANCZOS)
    return car


def main(out_dirs):
    from rembg import new_session
    session = new_session('isnet-general-use')
    for name in JOBS:
        car = build(name, session)
        for folder in out_dirs:
            Path(folder).mkdir(parents=True, exist_ok=True)
            car.save(Path(folder) / name, optimize=True)
        print(name, car.size)


if __name__ == '__main__':
    main(sys.argv[1:] or [HERE.parent / 'app' / 'tunertoolpro' / 'gui' / 'assets'])
