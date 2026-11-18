#!/usr/bin/env python3
"""Cut Carlos's concept film into the web loops for the promo site (DESIGN-GUIDE §6.15).

Source: images/minihouse_walkthrough_v11.mp4 (the master; never changed). The version of
2026-11-18 07:12 is 17.02 s, 1920 x 1080, 24 fps, with five shots cut at 4.02, 7.02, 10.52 and
14.52 s: hillside exterior, living room, bed, bathroom, wide bathroom.

Writes (all git-ignored, like every other media file):
  web/promo/public/film/house-film.mp4    the whole film, 1280 x 720
  web/promo/public/film/living-loop.mp4   shot 2, cropped 3:2, 960 x 640
  web/promo/public/film/bath-loop.mp4     shot 4, cropped 4:5, 720 x 900
  web/promo/src/assets/film/<name>.jpg    the first frame of each, used as the poster

Every file is silent H.264 with its index at the front (+faststart). The whole film ends with a
short crossfade into its own first frames, so the restart has no jump. The two section loops
are slow camera moves, so they play forward and then backward (ping-pong): no cut at all, and
twice the length of the shot.

Run from anywhere:  python scripts/cut_film.py
Needs ffmpeg and ffprobe on PATH. Standard library only.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, 'images', 'minihouse_walkthrough_v11.mp4')
VIDEO_DIR = os.path.join(ROOT, 'web', 'promo', 'public', 'film')
POSTER_DIR = os.path.join(ROOT, 'web', 'promo', 'src', 'assets', 'film')

# The shot times below belong to this version of the master. If the master changes,
# check the shots again (ffmpeg scene detection) before cutting.
EXPECTED_DURATION = 17.02

# name: (start s, end s or None for the whole film, crop (aspect, centre x) or None,
#        output size, loop: crossfade seconds or 'pingpong', CRF)
CUTS = {
    'house-film': (0.0, None, None, (1280, 720), 0.5, 31),
    'living-loop': (4.10, 6.95, (3 / 2, 0.50), (960, 640), 'pingpong', 30),
    'bath-loop': (10.60, 14.10, (4 / 5, 0.45), (720, 900), 'pingpong', 30),
}
SOURCE_SIZE = (1920, 1080)


def probe_duration(path: str) -> float:
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', path],
        check=True, capture_output=True, text=True,
    ).stdout
    return float(json.loads(out)['format']['duration'])


def frame_filter(crop: tuple[float, float] | None, size: tuple[int, int]) -> str:
    steps = []
    if crop:
        aspect, centre = crop
        width, height = SOURCE_SIZE
        crop_width = round(height * aspect)
        x = max(0, min(width - crop_width, round(centre * width - crop_width / 2)))
        steps.append(f'crop={crop_width}:{height}:{x}:0')
    steps.append(f'scale={size[0]}:{size[1]}:flags=lanczos')
    steps.append('setsar=1')
    return ','.join(steps)


def cut(name: str, start: float, end: float, crop, size, loop, crf: int) -> str:
    frames = frame_filter(crop, size)
    if loop == 'pingpong':
        graph = (
            f'[0:v]trim=start={start:.3f}:end={end:.3f},setpts=PTS-STARTPTS,{frames},split[fwd][back];'
            '[back]reverse[rev];[fwd][rev]concat=n=2:v=1:a=0,format=yuv420p[v]'
        )
    else:
        fade = float(loop)
        body = end - start - fade
        graph = (
            f'[0:v]trim=start={start + fade:.3f}:end={end:.3f},setpts=PTS-STARTPTS,{frames}[body];'
            f'[0:v]trim=start={start:.3f}:end={start + fade:.3f},setpts=PTS-STARTPTS,{frames}[head];'
            f'[body][head]xfade=transition=fade:duration={fade}:offset={body - fade:.3f},format=yuv420p[v]'
        )
    out = os.path.join(VIDEO_DIR, f'{name}.mp4')
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-i', SOURCE, '-filter_complex', graph, '-map', '[v]', '-an',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-profile:v', 'high',
        '-g', '48', '-movflags', '+faststart', out,
    ], check=True)
    poster = os.path.join(POSTER_DIR, f'{name}.jpg')
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-i', out, '-frames:v', '1', '-q:v', '3', poster,
    ], check=True)
    return out


def main() -> int:
    if not os.path.exists(SOURCE):
        print(f'missing master: {SOURCE}', file=sys.stderr)
        return 1
    duration = probe_duration(SOURCE)
    if abs(duration - EXPECTED_DURATION) > 0.05:
        print(f'the master is {duration:.2f} s, not {EXPECTED_DURATION} s: re-check the shot '
              'times before cutting', file=sys.stderr)
        return 1
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(POSTER_DIR, exist_ok=True)
    for name, (start, end, crop, size, loop, crf) in CUTS.items():
        out = cut(name, start, duration if end is None else end, crop, size, loop, crf)
        length = probe_duration(out)
        poster = os.path.join(POSTER_DIR, f'{name}.jpg')
        print(f'{name}: {length:.2f} s, {os.path.getsize(out) / 1e6:.2f} MB video, '
              f'{os.path.getsize(poster) / 1e3:.0f} KB poster')
    return 0


if __name__ == '__main__':
    sys.exit(main())
