import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image  # noqa: E402

ASSETS = Path(__file__).resolve().parents[1] / 'tunertoolpro' / 'gui' / 'assets'
NAMES = ['logo_car.png', 'intro_side.png', 'intro_bay.png']


class CarPictureTests(unittest.TestCase):
    def test_every_picture_has_a_see_through_background_and_a_solid_car(self):
        for name in NAMES:
            with self.subTest(name):
                alpha = Image.open(ASSETS / name).convert('RGBA').getchannel('A')
                width, height = alpha.size
                corners = [alpha.getpixel(p) for p in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1))]
                self.assertTrue(all(c == 0 for c in corners), corners)
                solid = sum(1 for v in alpha.getdata() if v > 200)
                self.assertGreater(solid / (width * height), 0.25)

    def test_pictures_are_small_enough_to_ship_in_a_phone_app(self):
        for name in NAMES:
            with self.subTest(name):
                self.assertLess((ASSETS / name).stat().st_size, 2_000_000)
                self.assertLessEqual(max(Image.open(ASSETS / name).size), 1280)


if __name__ == '__main__':
    unittest.main()
