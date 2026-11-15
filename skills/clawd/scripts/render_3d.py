"""Render transparent poses for the rounded OPUSCAR 98-style Clawd."""

import argparse
import json
import math
import re
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
from numba import njit, prange
from PIL import Image


RENDER_SIZE = (1320, 1000)
PNG_SIZE = (990, 750)
ANCHOR = (495, 609)


@dataclass(frozen=True)
class Pose:
    yaw: float
    pitch: float
    left: float
    right: float
    look: float
    blink: bool
    eye_y: float = 0.0


POSES = {
    "hero": Pose(.24, .09, -.21, .14, .015, False),
    "listen": Pose(-.12, .055, -.11, -.04, -.033, False),
    "listen-blink": Pose(-.12, .055, -.11, -.04, -.033, True),
    "question": Pose(-.07, .073, -.29, .21, .015, False),
    "point": Pose(.09, .08, -.21, .59, .125, False),
    "close": Pose(.045, .043, -.17, .19, 0., False),
    "blink": Pose(.045, .043, -.17, .19, 0., True),
}
GAZES = {
    "forward": (0., 0., False),
    "left": (-.13, 0., False),
    "right": (.13, 0., False),
    "up": (0., .14, False),
    "down": (0., -.14, False),
    "blink": (0., 0., True),
}


@njit(cache=True, inline="always")
def box(x, y, z, w, h, d, r):
    x = abs(x) - w + r
    y = abs(y) - h + r
    z = abs(z) - d + r
    return math.sqrt(max(0, x)**2 + max(0, y)**2 + max(0, z)**2) + min(0, max(x, y, z)) - r


@njit(cache=True, inline="always")
def arm(x, y, z, cx, cy, angle):
    x, y, z = x - cx, y - cy, z - .015
    c, s = math.cos(angle), math.sin(angle)
    return box(x*c + y*s, -x*s + y*c, z, .43, .167, .235, .088)


@njit(cache=True, inline="always")
def model(x, y, z, left, right, look, blink, eye_y):
    d = box(x, y - 1.59, z, 1.50, .943, .433, .163)
    d = min(d, arm(x, y, z, -1.70, 1.38, left), arm(x, y, z, 1.70, 1.38, right))
    for i in range(4):
        cx = (-1.055, -.425, .425, 1.055)[i]
        d = min(d, box(x-cx, y-.484, z-.04, .106, .201, .153, .068))
    shape = 0
    height = .071 if blink else .212
    elevation = 1.856 - (.14 if blink else 0.) + eye_y
    for i in range(2):
        cx = (-.675 if i == 0 else .675) + look
        eye = box(x-cx, y-elevation, z-.438, .085, height, .018, .016)
        if eye < d:
            shape = 1
            d = eye
    return d, shape


@njit(cache=True)
def normalize(x, y, z):
    length = math.sqrt(x*x + y*y + z*z)
    return x/length, y/length, z/length


@njit(cache=True, inline="always")
def dot(x, y, z, a, b, c):
    return x*a + y*b + z*c


@njit(cache=True)
def shade(x, y, z, vx, vy, vz, mat, left, right, look, blink, eye_y):
    e = .0011
    a = model(x+e, y, z, left, right, look, blink, eye_y)[0] - model(x-e, y, z, left, right, look, blink, eye_y)[0]
    b = model(x, y+e, z, left, right, look, blink, eye_y)[0] - model(x, y-e, z, left, right, look, blink, eye_y)[0]
    c = model(x, y, z+e, left, right, look, blink, eye_y)[0] - model(x, y, z-e, left, right, look, blink, eye_y)[0]
    nx, ny, nz = normalize(a, b, c)
    key = normalize(-.7, .93, .9)
    fill = normalize(.76, .24, .26)
    rim = normalize(.67, .74, -.82)
    l1 = max(0, dot(nx, ny, nz, key[0], key[1], key[2]))
    l2 = max(0, dot(nx, ny, nz, fill[0], fill[1], fill[2]))
    l3 = max(0, dot(nx, ny, nz, rim[0], rim[1], rim[2]))
    half = normalize(key[0]+vx, key[1]+vy, key[2]+vz)
    spec = max(0, dot(nx, ny, nz, half[0], half[1], half[2])) ** (24 if mat else 15)
    rim_gloss = (1-max(0, dot(nx, ny, nz, vx, vy, vz)))**2
    n = .5 * math.sin(x*32.1 + y*49.3 + z*67.1) * math.cos(x*67.3 - y*35.7)
    if mat:
        return 17 + 46*spec, 18 + 37*spec, 19 + 31*spec
    front = max(0, nz)
    light = .56 + .46*l1 + .135*l2 + .24*l3 + front*.052
    bronze = .15 + .85*min(1., y/1.5)
    r = (216 * light + 29*spec + 19*l3*rim_gloss + n*2.0) * (.92 + .08*bronze)
    g = (115 * light + 25*spec + 28*l3*rim_gloss + n*1.6) * (.86 + .14*bronze)
    b = (77 * light + 21*spec + 16*l2 + 21*l3*rim_gloss + n*1.4) * (.86 + .14*bronze)
    return min(255, r), min(255, g), min(255, b)


@njit(parallel=True, cache=True)
def render(w, h, yaw, pitch, left, right, look, blink, eye_y):
    image = np.zeros((h, w, 4), np.uint8)
    dist = 7.25
    cx = dist * math.sin(yaw)
    cy = 1.26 + dist * math.sin(pitch)
    cz = dist * math.cos(yaw)
    fx, fy, fz = normalize(-cx, 1.26-cy, -cz)
    rx, ry, rz = normalize(-fz, 0, fx)
    ux, uy, uz = -fy*rz, fz*rx-fx*rz, fy*rx
    ux, uy, uz = -ux, -uy, -uz
    size = 4.83
    for j in prange(h):
        v = size * (h/2 - j - .5) / w
        for i in range(w):
            u = size * (i + .5 - w/2) / w
            vx, vy, vz = normalize(fx+rx*u/dist+ux*v/dist, fy+ry*u/dist+uy*v/dist, fz+rz*u/dist+uz*v/dist)
            t = 0.
            for k in range(64):
                x, y, z = cx+t*vx, cy+t*vy, cz+t*vz
                d, mat = model(x, y, z, left, right, look, blink, eye_y)
                if d < .00085:
                    r, g, b = shade(x, y, z, -vx, -vy, -vz, mat, left, right, look, blink, eye_y)
                    image[j, i, 0] = int(r)
                    image[j, i, 1] = int(g)
                    image[j, i, 2] = int(b)
                    image[j, i, 3] = 255
                    break
                t += d
                if t > 11.:
                    break
    return image


def bounded_degrees(limit):
    def parse(value):
        number = float(value)
        if not -limit <= number <= limit:
            raise argparse.ArgumentTypeError(f"expected degrees between {-limit} and {limit}")
        return math.radians(number)
    return parse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--pose", nargs="+", choices=tuple(POSES), help="named poses (default: hero)")
    selection.add_argument("--all", action="store_true", help="render all seven poses")
    parser.add_argument("--name", help="output filename stem for a single pose")
    parser.add_argument("--yaw", type=bounded_degrees(40), help="camera azimuth in degrees")
    parser.add_argument("--pitch", type=bounded_degrees(16), help="camera elevation in degrees")
    parser.add_argument("--arm-left", type=bounded_degrees(65), help="left arm angle in degrees (positive lifts)")
    parser.add_argument("--arm-right", type=bounded_degrees(65), help="right arm angle in degrees (positive lifts)")
    parser.add_argument("--gaze", choices=tuple(GAZES))
    args = parser.parse_args()

    selected = tuple(POSES) if args.all else tuple(dict.fromkeys(args.pose or ["hero"]))
    changes = {field: getattr(args, field) for field in ("yaw", "pitch") if getattr(args, field) is not None}
    if args.arm_left is not None:
        changes["left"] = -args.arm_left
    if args.arm_right is not None:
        changes["right"] = args.arm_right
    if args.gaze is not None:
        look, eye_y, blink = GAZES[args.gaze]
        changes.update(look=look, eye_y=eye_y, blink=blink)
    if (args.name or changes) and len(selected) != 1:
        parser.error("use one pose when naming or customizing a render")
    if args.name is not None and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.name):
        parser.error("--name must contain lowercase letters, digits and single hyphens")

    output = args.output_dir.resolve()
    targets = [(base, output / f"{args.name or base}.png") for base in selected]
    for _, target in targets:
        if target.exists() or target.is_symlink():
            parser.error(f"output already exists: {target}")
    output.mkdir(parents=True, exist_ok=True)

    assets = []
    for base, target in targets:
        pose = replace(POSES[base], **changes)
        pixels = render(*RENDER_SIZE, pose.yaw, pose.pitch, pose.left, pose.right, pose.look, pose.blink, pose.eye_y)
        image = Image.fromarray(pixels).resize(PNG_SIZE, Image.Resampling.LANCZOS)
        bounds = image.getchannel("A").getbbox()
        if bounds is None or not (0 < bounds[0] < bounds[2] < PNG_SIZE[0]
                                  and 0 < bounds[1] < bounds[3] < PNG_SIZE[1]):
            raise RuntimeError(f"pose is empty or clipped: {target.stem}")
        with target.open("xb") as file:
            image.save(file, format="PNG")
        assets.append({"name": target.stem, "base_pose": base, "path": str(target), "alpha_bounds": bounds})
    print(json.dumps({"size": PNG_SIZE, "anchor": ANCHOR, "assets": assets}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
