"""Render the Fit 2 preview from its fourteen assembled, millimetre binary STLs."""

from pathlib import Path
import struct
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "fase1/prototipo/marco-fit2"
STL_RECORD = np.dtype([("normal", "<f4", (3,)), ("vertices", "<f4", (3, 3)), ("attr", "<u2")])
EXPECTED = {1: "rail_left", 9: "wall_front", 10: "wall_back", 11: "gable_left",
            12: "gable_right", 13: "roof_front", 14: "roof_back"}
PALETTE = np.array([[110, 134, 151], [124, 171, 164], [210, 160, 112]], dtype=float)
INK, MUTED, LINE = "#203538", "#526a6c", "#c8d2cf"
PAPER, PANEL = "#f5f5ef", "#fcfcf8"


def read_parts(directory):
    paths = {}
    for path in directory.glob("*.stl"):
        prefix, _, name = path.stem.partition("_")
        if prefix not in {f"{k:02}" for k in range(1, 15)}:
            raise ValueError(f"Unexpected assembled STL: {path.name}")
        index = int(prefix)
        if index in paths or not name or (index in EXPECTED and name != EXPECTED[index]):
            raise ValueError(f"Duplicate or unexpected part name: {path.name}")
        paths[index] = path
    missing = sorted(set(range(1, 15)) - paths.keys())
    if missing:
        raise ValueError(f"Missing assembled STL part(s) in {directory}: " + ", ".join(f"{i:02}" for i in missing))

    parts = []
    for index in range(1, 15):
        path = paths[index]
        with path.open("rb") as source:
            header = source.read(84)
            count = struct.unpack_from("<I", header, 80)[0] if len(header) == 84 else 0
            if not count or path.stat().st_size != 84 + count * STL_RECORD.itemsize:
                raise ValueError(f"Not a complete binary STL: {path.name}")
            triangles = np.fromfile(source, dtype=STL_RECORD, count=count)["vertices"].astype(np.float64)
        if not np.isfinite(triangles).all():
            raise ValueError(f"Nonfinite vertices: {path.name}")
        parts.append(triangles)
    return parts


def unit(v):
    return v / np.linalg.norm(v)


def camera():
    # Model X runs along the ridge, Z is vertical. Keep this camera in both panels.
    eye = unit(np.array([0.90, -1.55, 0.94]))
    right = unit(np.cross([0, 0, 1], eye))
    return np.stack((right, -np.cross(eye, right), eye), axis=1)


def explosion(centers, middle):
    offsets = np.zeros((14, 3))
    for i in range(8, 14):
        axis = 0 if i in (10, 11) else 1
        offsets[i, axis] = np.sign(centers[i, axis] - middle[axis]) * (17 if i < 12 else 25)
        offsets[i, 2] = 16 if i < 12 else 43
    return offsets


def render(parts, offsets, size, basis):
    aa = 2
    w, h = size[0] * aa, size[1] * aa
    projected = [(triangles + shift) @ basis for triangles, shift in zip(parts, offsets)]
    pmin = np.min([p.min(axis=(0, 1)) for p in projected], axis=0)
    pmax = np.max([p.max(axis=(0, 1)) for p in projected], axis=0)
    span = pmax[:2] - pmin[:2]
    if np.any(span <= 0):
        raise ValueError("Assembly has no projected area")
    scale = min((w - 14 * aa) / span[0], (h - 14 * aa) / span[1])
    origin = (np.array([w, h]) - scale * (pmax[:2] + pmin[:2])) / 2
    rgb = np.empty((h, w, 3), dtype=np.uint8)
    rgb[:] = (252, 252, 248)
    depth = np.full((h, w), -np.inf, dtype=np.float32)
    owners = np.zeros((h, w), dtype=np.uint8)
    light = unit(np.array([-0.45, -0.55, 1.0]))
    for part_id, (triangles, p) in enumerate(zip(parts, projected), 1):
        family = 0 if part_id <= 8 else (1 if part_id <= 12 else 2)
        normals = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
        normals /= np.maximum(np.linalg.norm(normals, axis=1, keepdims=True), 1e-30)
        normals[normals @ basis[:, 2] < 0] *= -1
        intensity = 0.76 + 0.26 * np.maximum(0.0, normals @ light) + 0.06 * normals[:, 2].clip(0, 1)
        colors = np.rint(intensity[:, None] * PALETTE[family]).clip(0, 255).astype(np.uint8)
        p[:, :, :2] = p[:, :, :2] * scale + origin
        lo = np.ceil(p[:, :, :2].min(axis=1)).astype(int).clip(min=[0, 0])
        hi = np.floor(p[:, :, :2].max(axis=1)).astype(int).clip(max=[w - 1, h - 1])
        for tri, color, (x0, y0), (x1, y1) in zip(p, colors, lo, hi):
            if x1 < x0 or y1 < y0:
                continue
            (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
            det = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
            if abs(det) < 1e-9:
                continue
            ys, xs = np.ogrid[y0:y1 + 1, x0:x1 + 1]
            u = ((xs - ax) * (cy - ay) - (ys - ay) * (cx - ax)) / det
            v = ((ys - ay) * (bx - ax) - (xs - ax) * (by - ay)) / det
            z = az + u * (bz - az) + v * (cz - az)
            box = np.s_[y0:y1 + 1, x0:x1 + 1]
            visible = (u >= -1e-8) & (v >= -1e-8) & (u + v <= 1 + 1e-8) & (z > depth[box])
            depth[box][visible] = z[visible]
            owners[box][visible] = part_id
            rgb[box][visible] = color
    # Ink only visible part boundaries; no triangle-edge strokes or invented hidden lines.
    edge = np.zeros((h, w), dtype=bool)
    edge[:, 1:] |= owners[:, 1:] != owners[:, :-1]
    edge[1:, :] |= owners[1:, :] != owners[:-1, :]
    edge &= owners != 0
    rgb[edge] = (rgb[edge] * 0.75).astype(np.uint8)
    return Image.fromarray(rgb).resize(size, Image.Resampling.LANCZOS)


def font(size, bold=False):
    for name in (("segoeuib.ttf", "DejaVuSans-Bold.ttf") if bold else ("segoeui.ttf", "DejaVuSans.ttf")):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def sheet(parts):
    minima = np.array([p.min(axis=(0, 1)) for p in parts])
    maxima = np.array([p.max(axis=(0, 1)) for p in parts])
    lo, hi = minima.min(axis=0), maxima.max(axis=0)
    basis = camera()
    offsets = explosion((maxima + minima) / 2, (hi + lo) / 2)
    image = Image.new("RGB", (1920, 1120), PAPER)
    draw = ImageDraw.Draw(image)

    def label(x, y, text, size, bold=False, color=INK, anchor="lt"):
        draw.text((x, y), text, fill=color, font=font(size, bold), anchor=anchor)

    label(66, 48, "MINIHOUSE   /   PROTOTYPE ENGINEERING", 21, True, MUTED)
    label(62, 85, "Fit 2 frame assembly", 72, True)
    label(1850, 71, "ASSEMBLED ENVELOPE   /   X × Y × Z", 20, True, MUTED, "rt")
    dims = " × ".join(f"{value:.1f}".removesuffix(".0") for value in hi - lo)
    label(1850, 110, dims + " mm", 37, True, anchor="rt")

    panels = [(64, 1164, "01", "Assembled", np.zeros_like(offsets)),
              (1188, 1856, "02", "Exploded", offsets)]
    for left, right, number, title, displacement in panels:
        draw.rounded_rectangle((left, 207, right, 883), radius=15, fill=PANEL, outline=LINE, width=2)
        label(left + 32, 242, number, 25, True, MUTED)
        label(left + 87, 235, title, 38, True)
        tile = render(parts, displacement, (right - left - 64, 545), basis)
        image.paste(tile, (left + 32, 303))

    label(66, 940, "14 PARTS", 27, True)
    for x, name, count, color in zip((365, 855, 1385), ("Base", "Walls / gables", "Split roof halves"),
                                     (8, 4, 2), PALETTE.astype(int)):
        draw.rounded_rectangle((x, 940, x + 29, 969), radius=5, fill=tuple(color.tolist()))
        label(x + 48, 938, f"{name}  ({count})", 30, True)
    draw.line((64, 1010, 1856, 1010), fill=LINE, width=2)
    label(65, 1044, "Conceptual printable mock-up", 23, False, MUTED)
    label(1854, 1044, "Orthographic views from assembled STL geometry", 23, False, MUTED, "rt")
    return image


if __name__ == "__main__":
    target = ROOT / "Frames_Fit2_preview.png"
    try:
        sheet(read_parts(ROOT / "assembled_meshes")).save(target)
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))
    print(target)
