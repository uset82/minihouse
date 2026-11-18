#!/usr/bin/env python3
"""Cut Carlos's concept film into the web loops for the promo site (DESIGN-GUIDE §6.15).

Source: images/minihouse_walkthrough_v18_4k.mp4 (the master; never changed). The version of
2026-11-18 is 17.04 s, 3840 x 2160, 24 fps, with five shots cut at 4.04, 7.04, 10.54 and
14.54 s: hillside exterior, living room, bed, bathroom, wide bathroom. The source size is
read from the master with ffprobe, never hard-coded, so a new master cannot silently put the
crops on the wrong part of the frame.

Writes (all git-ignored, like every other media file):
  web/promo/public/film/house-film-1920.mp4  the whole film, 1920 x 1080 (wide screens)
  web/promo/public/film/house-film.mp4       the whole film, 1280 x 720
  web/promo/public/film/living-loop.mp4      shot 2, cropped 3:2, 1440 x 960
  web/promo/public/film/bath-loop.mp4        shot 4, cropped 4:5, 1080 x 1350
  web/promo/src/assets/film/<name>.jpg       posters: first frame of each film's largest cut

Every file is silent H.264 with its index at the front (+faststart). The whole film ends with a
short crossfade into its own first frames, so the restart has no jump. The two section loops
are slow camera moves, so they play forward and then backward (ping-pong): no cut at all, and
twice the length of the shot. CRF starts at 31 for the hero and 30 for the loops and is raised
one step at a time only if a cut exceeds its size budget.

Run from anywhere:  python scripts/cut_film.py
Needs ffmpeg and ffprobe on PATH. Standard library only.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, 'images', 'minihouse_walkthrough_v18_4k.mp4')
VIDEO_DIR = os.path.join(ROOT, 'web', 'promo', 'public', 'film')
POSTER_DIR = os.path.join(ROOT, 'web', 'promo', 'src', 'assets', 'film')

# The shot times below belong to this version of the master. If the master changes,
# check the shots again (ffmpeg scene detection) before cutting.
EXPECTED_DURATION = 17.04

# name: (start s, end s or None for the whole film, crop (aspect, centre x) or None,
#        output size, loop: crossfade seconds or 'pingpong', starting CRF)
CUTS = {
    'house-film-1920': (0.0, None, None, (1920, 1080), 0.5, 31),
    'house-film': (0.0, None, None, (1280, 720), 0.5, 31),
    'living-loop': (4.10, 6.95, (3 / 2, 0.50), (1440, 960), 'pingpong', 30),
    'bath-loop': (10.60, 14.10, (4 / 5, 0.45), (1080, 1350), 'pingpong', 30),
}

# MB (decimal, as printed by ffprobe/os.path.getsize). Raise CRF only to meet these.
BUDGET_MB = {
    'house-film-1920': 4.5,
    'house-film': 2.5,
    'living-loop': 1.2,
    'bath-loop': 1.3,
}
MAX_CRF_RAISE = 12

# Poster -> the cut it comes from. Each film's first frame is taken from its largest cut;
# the two loops have only one cut each, so they are their own source.
POSTER_FROM = {
    'house-film': 'house-film-1920',
    'living-loop': 'living-loop',
    'bath-loop': 'bath-loop',
}


def probe_duration(path: str) -> float:
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', path],
        check=True, capture_output=True, text=True,
    ).stdout
    return float(json.loads(out)['format']['duration'])


def probe_size(path: str) -> tuple[int, int]:
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=width,height', '-of', 'json', path],
        check=True, capture_output=True, text=True,
    ).stdout
    stream = json.loads(out)['streams'][0]
    return int(stream['width']), int(stream['height'])


def frame_filter(crop: tuple[float, float] | None, size: tuple[int, int],
                 source_size: tuple[int, int]) -> str:
    steps = []
    if crop:
        aspect, centre = crop
        width, height = source_size
        crop_width = round(height * aspect)
        x = max(0, min(width - crop_width, round(centre * width - crop_width / 2)))
        steps.append(f'crop={crop_width}:{height}:{x}:0')
    steps.append(f'scale={size[0]}:{size[1]}:flags=lanczos')
    steps.append('setsar=1')
    return ','.join(steps)


def cut(name: str, start: float, end: float, crop, size, loop, crf: int,
        source_size: tuple[int, int]) -> str:
    frames = frame_filter(crop, size, source_size)
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
    return out


def make_poster(name: str, source_cut: str) -> str:
    video = os.path.join(VIDEO_DIR, f'{source_cut}.mp4')
    poster = os.path.join(POSTER_DIR, f'{name}.jpg')
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-i', video, '-frames:v', '1', '-q:v', '3', poster,
    ], check=True)
    return poster


def main() -> int:
    if not os.path.exists(SOURCE):
        print(f'missing master: {SOURCE}', file=sys.stderr)
        return 1
    duration = probe_duration(SOURCE)
    if abs(duration - EXPECTED_DURATION) > 0.05:
        print(f'the master is {duration:.2f} s, not {EXPECTED_DURATION} s: re-check the shot '
              'times before cutting', file=sys.stderr)
        return 1
    source_size = probe_size(SOURCE)
    print(f'master: {source_size[0]} x {source_size[1]}, {duration:.3f} s')
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(POSTER_DIR, exist_ok=True)
    for name, (start, end, crop, size, loop, base_crf) in CUTS.items():
        budget = BUDGET_MB[name]
        crf = base_crf
        while True:
            out = cut(name, start, duration if end is None else end, crop, size, loop, crf,
                      source_size)
            mb = os.path.getsize(out) / 1e6
            if mb <= budget or crf >= base_crf + MAX_CRF_RAISE:
                break
            crf += 1
        length = probe_duration(out)
        flag = 'within budget' if mb <= budget else f'WARNING: over {budget:.1f} MB budget'
        print(f'{name}: {length:.2f} s, {size[0]} x {size[1]}, {mb:.2f} MB '
              f'(budget {budget:.1f} MB, CRF {crf}) — {flag}')
    for name, source_cut in POSTER_FROM.items():
        poster = make_poster(name, source_cut)
        print(f'{name}.jpg: first frame of {source_cut}, {os.path.getsize(poster) / 1e3:.0f} KB')
    return 0


if __name__ == '__main__':
    sys.exit(main())
