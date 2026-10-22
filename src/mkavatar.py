# -*- coding: utf-8 -*-
import math
from PIL import Image, ImageDraw

S = 4
W = 460
CREAM = (246, 241, 231)
img = Image.new("RGB", (W*S, W*S), CREAM)
d = ImageDraw.Draw(img)

def bez(p0, p1, p2, p3, n=500):
    pts = []
    for i in range(n+1):
        t = i/n; mt = 1-t
        x = mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0]
        y = mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts

# one continuous vine from bottom-left to the light at top-right
segs = [
    ((118, 408), (108, 336), (176, 330), (206, 300)),
    ((206, 300), (236, 270), (222, 214), (262, 196)),
    ((262, 196), (302, 178), (300, 126), (338, 98)),
    ((338, 98), (362, 80), (380, 74), (396, 70)),
]
path = []
for s in segs:
    path += bez(*s, n=160)

DEEP = (44, 84, 48)
GREEN = (62, 116, 66)
LIGHT = (86, 142, 84)

# tapered stem
left, right = [], []
N = len(path)
for i, (x, y) in enumerate(path):
    t = i/(N-1)
    w = (12.5 - 7.5*t) / 2
    if i == 0: dx, dy = path[1][0]-x, path[1][1]-y
    elif i == N-1: dx, dy = x-path[-2][0], y-path[-2][1]
    else: dx, dy = path[i+1][0]-path[i-1][0], path[i+1][1]-path[i-1][1]
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy/ln, dx/ln
    left.append((x+nx*w, y+ny*w))
    right.append((x-nx*w, y-ny*w))
d.polygon([(x*S, y*S) for x, y in left + right[::-1]], fill=DEEP)

def leaf(cx, cy, ang, L, Wd, color, rib=None):
    n = 80
    upper, lower = [], []
    for i in range(n+1):
        t = i/n
        x = L*t
        y = Wd*0.5*(math.sin(math.pi*t)**0.85)
        upper.append((x, -y)); lower.append((x, y))
    poly = upper + lower[::-1]
    ca, sa = math.cos(ang), math.sin(ang)
    out = [(cx + p[0]*ca - p[1]*sa, cy + p[0]*sa + p[1]*ca) for p in poly]
    d.polygon([(x*S, y*S) for x, y in out], fill=color)
    if rib:
        tip = (cx + L*ca*0.93, cy + L*sa*0.93)
        d.line([(cx*S, cy*S), (tip[0]*S, tip[1]*S)], fill=rib, width=max(1, int(1.1*S)))

# leaves alternate along the stem, angled away from it
leaves = [
    (0.17, -125, 74, 40, GREEN, (60, 106, 62)),
    (0.33,   58, 84, 46, LIGHT, (70, 122, 70)),
    (0.50, -118, 76, 42, GREEN, (60, 106, 62)),
    (0.65,   62, 68, 38, LIGHT, (70, 122, 70)),
    (0.80, -105, 56, 30, GREEN, (60, 106, 62)),
]
for frac, deg, L, Wd, col, rib in leaves:
    idx = int(frac*(N-1))
    x, y = path[idx]
    leaf(x, y, math.radians(deg), L, Wd, col, rib)

# the light
cx, cy = 400, 66
for rr, wd, col in [(56, 1.5, (236, 205, 152)), (78, 1.2, (242, 219, 178))]:
    d.ellipse([(cx-rr)*S, (cy-rr)*S, (cx+rr)*S, (cy+rr)*S], outline=col, width=int(wd*S))
d.ellipse([(cx-27)*S, (cy-27)*S, (cx+27)*S, (cy+27)*S], fill=(230, 166, 70))

img = img.resize((W, W), Image.LANCZOS)
img.save("avatar.png", optimize=True)
import os
print("avatar.png", os.path.getsize("avatar.png"), img.size)
