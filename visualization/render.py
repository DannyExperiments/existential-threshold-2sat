#!/usr/bin/env python3
"""Render the uniform y-assignment cube for the worked example."""
from itertools import product
from math import cos, pi, sin
from pathlib import Path
import argparse

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 660, 598
BACKGROUND = "#0d1824"
PANEL = "#132638"
INK = "#f1f6fb"
MUTED = "#adc3d4"
WIRE = "#435d72"
ON = "#66dfc3"
OFF = "#5b7184"
ACCENT = "#ffd480"
POINTS = list(product((0, 1), repeat=3))
EDGES = [(a, b) for i, a in enumerate(POINTS) for b in POINTS[i + 1:]
         if sum(u != v for u, v in zip(a, b)) == 1]
STEPS = [
    ("Root · S is empty", "B alone keeps six assignments.", "Force x1 and x2. Their assumptions conflict.", None),
    ("Allow y1 · S = {y1}", "B with y1 keeps four assignments.", "x = (0, 1) is a witness. Count reaches threshold.", 0),
    ("Allow y2 · S = {y2}", "B with y2 keeps three assignments.", "The count test prunes this branch.", 1),
]


def survives(p, axis):
    return bool((p[0] or p[2]) and (axis is None or p[axis]))


def project(p, angle, centre=(330, 301)):
    x, y, z = ((v - .5) * 2 for v in p)
    a, b = cos(angle), sin(angle)
    x, y = a * x - b * y, b * x + a * y
    elevation = .41
    y, z = cos(elevation) * y - sin(elevation) * z, sin(elevation) * y + cos(elevation) * z
    scale = 83 * 8 / (8 + y)
    return centre[0] + scale * x, centre[1] - scale * z, y


def font_factory(font_directory):
    alternatives = [font_directory] if font_directory else [
        Path("/System/Library/Fonts/Supplemental"), Path("/usr/share/fonts/truetype/dejavu")]
    for directory in alternatives:
        for names in [("Arial.ttf", "Arial Bold.ttf"), ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")]:
            if all((directory / name).is_file() for name in names):
                return lambda size, bold=False: ImageFont.truetype(str(directory / names[bold]), size)
    raise SystemExit("Pass --font-dir containing Arial or DejaVu Sans")


def draw_frame(frame, total, fonts):
    stage = min(frame * 3 // total, 2)
    title, caption, action, axis = STEPS[stage]
    picture = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(picture)
    draw.text((26, 24), "Existential threshold 2-SAT", font=fonts(32, True), fill=INK)
    draw.text((28, 72), "Worked example  •  8 uniform y-assignments  •  p = 1/2", font=fonts(22), fill=MUTED)
    draw.rounded_rectangle((24, 116, 636, 482), radius=22, fill=PANEL)
    draw.text((44, 137), title, font=fonts(24, True), fill=INK)
    angle = 0.56 + 2 * pi * frame / total
    coords = {p: project(p, angle) for p in POINTS}
    for a, b in EDGES:
        passing = survives(a, axis) and survives(b, axis)
        draw.line((coords[a][:2], coords[b][:2]), fill=ON if passing else WIRE, width=3 if passing else 2)
    for p in sorted(POINTS, key=lambda p: coords[p][2], reverse=True):
        x, y, _ = coords[p]
        passing = survives(p, axis)
        radius = 9 if passing else 7
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=ON if passing else OFF,
                     outline=PANEL, width=2)
    count = sum(survives(p, axis) for p in POINTS)
    draw.text((612, 145), f"{count} / 8", anchor="ra", font=fonts(29, True), fill=ON if count >= 4 else ACCENT)
    draw.text((45, 449), "●  passes B and S", font=fonts(21), fill=ON)
    draw.text((294, 449), "●  filtered out", font=fonts(21), fill=MUTED)
    draw.text((28, 500), caption, font=fonts(25, True), fill=INK)
    draw.text((28, 543), action, font=fonts(21), fill=MUTED)
    return picture


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", type=Path)
    parser.add_argument("--frames", type=int, default=36)
    parser.add_argument("--out", type=Path, default=ROOT / "threshold-search.gif")
    args = parser.parse_args()
    if args.frames < 3 or args.frames % 3:
        parser.error("--frames must be a positive multiple of 3")
    fonts = font_factory(args.font_dir)
    frames = [draw_frame(i, args.frames, fonts).quantize(colors=64) for i in range(args.frames)]
    durations = [100] * args.frames
    for index in range(args.frames // 3 - 1, args.frames, args.frames // 3):
        durations[index] = 600
    frames[0].save(args.out, save_all=True, append_images=frames[1:], optimize=True,
                   duration=durations, loop=0, disposal=1)


if __name__ == "__main__":
    main()
