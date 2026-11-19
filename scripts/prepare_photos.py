#!/usr/bin/env python3
"""Make the site copies of Carlos's demolition photos and the steel sample (task-landing-r3 G-11).

The originals in images/ are never changed. Every copy is converted to sRGB and saved with no
EXIF, IPTC, XMP or colour profile: the photographer's files carry his name and phone number,
and none of that may reach the site (DESIGN-GUIDE §7, D16). Needs Pillow (10.4 is installed).
"""
from __future__ import annotations

import io
import os
import sys

from PIL import Image, ImageCms, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'images')
OUT = os.path.join(ROOT, 'web', 'promo', 'src', 'assets', 'images')

# site copy: (original in images/, width, height, crop box (left, top, right, bottom) or None)
JOBS = {
    'midtun-gable.jpg': ('IMG_1343.jpg', 1800, 2400, None),
    'midtun-stove.jpg': ('6.jpg', 1800, 2400, None),
    'midtun-glass.jpg': ('0V0A2359.jpg', 2400, 1601, None),
    'midtun-1887.jpg': ('0V0A2394.jpg', 2400, 1601, None),
    'midtun-nail.jpg': ('0V0A2535.jpg', 2400, 1601, None),
    'midtun-stone.jpg': ('0V0A2667.jpg', 2400, 1601, None),
    # The steel sample: the front-right corner, the dark plinth across the bottom fifth.
    'texture-stal.jpg': ('Weathered timber cabin with a glowing interior.png', 280, 350, (1024, 480, 1304, 830)),
}
NEVER = {'3.jpg', '5.jpg'}  # workers and a readable number plate (D16: «Leave them out»)
SRGB = ImageCms.createProfile('sRGB')


def to_srgb(image: Image.Image, icc: bytes | None) -> Image.Image:
    if icc:
        source = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        return ImageCms.profileToProfile(image, source, SRGB, outputMode='RGB')
    return image.convert('RGB')


def private_segments(path: str) -> list[str]:
    """APP1 (EXIF or XMP) and APP13 (IPTC) segments left in a JPEG."""
    with open(path, 'rb') as handle:
        data = handle.read()
    found, i = [], 2
    while i + 4 <= len(data) and data[i] == 0xFF:
        marker = data[i + 1]
        if marker in (0xD9, 0xDA):
            break
        length = int.from_bytes(data[i + 2:i + 4], 'big')
        if marker == 0xE1:
            found.append('APP1')
        elif marker == 0xED:
            found.append('APP13')
        i += 2 + length
    return found


def main() -> int:
    for name, (original, width, height, box) in JOBS.items():
        if original in NEVER:
            print(f'refused: {original} is excluded (D16)')
            return 1
        path = os.path.join(SRC, original)
        if not os.path.isfile(path):
            print(f'missing: {path}')
            return 1
        with Image.open(path) as opened:
            icc = opened.info.get('icc_profile')
            image = to_srgb(ImageOps.exif_transpose(opened), icc)
        if box:
            image = image.crop(box)
        if image.size != (width, height):
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        target = os.path.join(OUT, name)
        # No exif=, icc_profile= or xmp= argument, on purpose.
        image.save(target, 'JPEG', quality=90 if box else 86, optimize=True, progressive=True)
        left = private_segments(target)
        if left:
            print(f'{name}: file data survived ({", ".join(left)})')
            return 1
        print(f'{name}: {width} x {height}, {os.path.getsize(target) / 1e6:.2f} MB, from {original}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
