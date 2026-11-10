#!/usr/bin/env python3
"""Render assets/banner.gif from the same geometry as banner.svg (Pillow only)."""
import math, re, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import build_svgs as B

FW, FH = 960, 320          # final size
S = 2                      # supersample
BW, BH = FW * S, FH * S
F = BW / 1200              # design -> big px
N = 36                     # frames
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'   # edit for macOS/Windows
FONTR = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'


def P(p):
    return (p[0] * F, p[1] * F)


def parse(d):
    subs, cur = [], []
    x = y = sx = sy = 0.0
    for cmd, args in re.findall(r'([MHVLZ])([^MHVLZ]*)', d):
        n = [float(v) for v in args.replace(',', ' ').split()]
        if cmd == 'M':
            if cur:
                subs.append(cur)
            x, y = n[0], n[1]; sx, sy = x, y; cur = [(x, y)]
        elif cmd == 'H':
            x = n[0]; cur.append((x, y))
        elif cmd == 'V':
            y = n[0]; cur.append((x, y))
        elif cmd == 'L':
            x, y = n[0], n[1]; cur.append((x, y))
        elif cmd == 'Z':
            cur.append((sx, sy))
    if cur:
        subs.append(cur)
    return subs


def wordmark_polys():
    polys = []
    for i, c in enumerate(B.WORD):
        for sub in parse(B.LET[c]):
            polys.append([P((B.WM_TX + B.WM_SCALE * (x + i * B.PITCH), B.WM_TY + B.WM_SCALE * y)) for x, y in sub])
    return polys


def bez(p0, p1, p2, p3, n=18):
    out = []
    for k in range(n + 1):
        t = k / n; u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


def tendril_poly(t, w):
    pts = [(a[0] + (b[0] - a[0]) * w, a[1] + (b[1] - a[1]) * w) for a, b in zip(t['A'], t['B'])]
    poly = []
    for i in range(0, 3):
        seg = bez(pts[i * 3], pts[i * 3 + 1], pts[i * 3 + 2], pts[i * 3 + 3])
        poly += seg if i == 0 else seg[1:]
    return poly


def quad(p0, c, p2, n=20):
    return [((1 - t)**2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p2[0],
             (1 - t)**2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p2[1]) for t in [k / n for k in range(n + 1)]]


_p0, _c1, _p2, _c2 = B.EYE_PTS
EYE_POLY = quad(_p0, _c1, _p2) + quad(_p2, _c2, _p0)[1:]


def eye_polys(cx, cy, s, gap, blink):
    out = []
    for m in (1, -1):
        ex = cx - m * (gap / 2 + B.EYE_INNER * s)
        out.append([P((ex + m * s * (x - 67), cy + s * blink * (y - 32))) for x, y in EYE_POLY])
    return out


def main():
    f_bold = lambda sz: ImageFont.truetype(FONT, int(sz * F))
    f_reg = lambda sz: ImageFont.truetype(FONTR, int(sz * F))

    # ---------- static layers ----------
    yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32)
    d = np.sqrt(((xx - BW / 2) / (BW * .75)) ** 2 + ((yy - BH) / (BH * .75)) ** 2)
    a = np.clip(1 - d, 0, 1) ** 2 * .22
    bg = np.zeros((BH, BW, 3), np.uint8)
    bg[..., 0] = (a * 255 * .9).astype(np.uint8)
    bgim = Image.fromarray(bg)
    gd = ImageDraw.Draw(bgim)
    for x in range(0, 1201, 50):
        gd.line([P((x, 0)), P((x, 400))], fill=(14, 14, 14), width=1)
    for y in range(0, 401, 50):
        gd.line([P((0, y)), P((1200, y))], fill=(14, 14, 14), width=1)

    wpolys = wordmark_polys()
    stroke = int(10 * B.WM_SCALE * F)
    wmask = Image.new('L', (BW, BH), 0)
    wd = ImageDraw.Draw(wmask)
    for pl in wpolys:
        wd.line(pl, fill=255, width=stroke, joint='curve')
    edge = Image.new('L', (BW, BH), 0)
    ed = ImageDraw.Draw(edge)
    for pl in wpolys:
        ed.line(pl, fill=255, width=int(12.5 * B.WM_SCALE * F), joint='curve')
    glowmask = Image.new('L', (BW, BH), 0)
    gm = ImageDraw.Draw(glowmask)
    for pl in wpolys:
        gm.line(pl, fill=255, width=int(16 * B.WM_SCALE * F), joint='curve')
    glowblur = glowmask.filter(ImageFilter.GaussianBlur(9 * B.WM_SCALE * F))

    # metallic vertical gradient in wordmark space
    top = B.WM_TY + 5 * B.WM_SCALE; bot = B.WM_TY + 85 * B.WM_SCALE
    tt = np.clip((yy / F - top) / (bot - top), 0, 1)
    stops = [(0, (255, 255, 255)), (.38, (215, 219, 224)), (.5, (138, 144, 151)), (.53, (236, 239, 242)), (1, (124, 130, 138))]
    grad = np.zeros((BH, BW, 3), np.float32)
    for c in range(3):
        grad[..., c] = np.interp(tt, [s[0] for s in stops], [s[1][c] for s in stops])
    gradim = Image.fromarray(grad.astype(np.uint8))

    tendrils = B.banner_tendrils()
    red = Image.new('RGB', (BW, BH), (225, 6, 0))
    white = Image.new('RGB', (BW, BH), (255, 255, 255))

    # tagline positions
    tag = 'WE ARE VENOM.'
    tf = f_bold(24)
    adv = 24 * B.CW * F + 14 * F
    total = adv * len(tag) - 14 * F
    tx0 = 600 * F - total / 2

    frames = []
    for i in range(N):
        ph = i / N
        pulse = .55 + .45 * math.sin(2 * math.pi * ph)
        wig = (1 - math.cos(2 * math.pi * ph)) / 2
        im = bgim.copy()
        dr = ImageDraw.Draw(im)
        # tendrils
        for t in tendrils:
            pl = [P(p) for p in tendril_poly(t, wig)]
            dr.line(pl, fill=(34, 34, 34), width=int(18 * F), joint='curve')
            dr.line(pl, fill=(7, 7, 7), width=int(13 * F), joint='curve')
            n = len(pl)
            pos = (ph + t['ph']) % 1.0
            a0 = int(pos * (n + 10)) - 10
            seg = pl[max(0, a0):max(0, min(n, a0 + 9))]
            if len(seg) > 1:
                dr.line(seg, fill=(255, 42, 26), width=int(2.4 * F), joint='curve')
        # scan band
        sy = -60 + (ph * 460)
        band = Image.new('L', (BW, BH), 0)
        ImageDraw.Draw(band).rectangle([0, int(sy * F), BW, int((sy + 60) * F)], fill=int(34))
        im.paste(red, mask=band)
        # wordmark glow, edge, metal
        im.paste(red, mask=glowblur.point(lambda v, k=pulse: int(v * (.3 + .5 * k) * .7)))
        im.paste((51, 54, 59), mask=edge)
        im.paste(gradim, mask=wmask)
        # specular sweep
        sw_x = -70 + 830 * min(1, ph / .55)
        if ph < .55:
            sm = Image.new('L', (BW, BH), 0)
            sd = ImageDraw.Draw(sm)
            bx = B.WM_TX + B.WM_SCALE * sw_x
            wdt = 46 * B.WM_SCALE
            sk = math.tan(math.radians(20)) * 110 * B.WM_SCALE
            y0 = B.WM_TY - 10 * B.WM_SCALE; y1 = B.WM_TY + 100 * B.WM_SCALE
            sd.polygon([P((bx, y0)), P((bx + wdt, y0)), P((bx + wdt - sk, y1)), P((bx - sk, y1))], fill=210)
            sm = sm.filter(ImageFilter.GaussianBlur(8))
            im.paste(white, mask=ImageChops.multiply(sm, wmask))
        # eyes
        k = i
        blink = [1, 1, 1, .5, .08, .5][k - 30] if 30 <= k < 36 else 1
        ep = eye_polys(600, 60, .85, 28, blink)
        gl = Image.new('L', (BW, BH), 0)
        gd2 = ImageDraw.Draw(gl)
        for pg in ep:
            gd2.polygon(pg, fill=255)
        glb = gl.filter(ImageFilter.GaussianBlur(7 * .85 * F))
        im.paste(white, mask=glb.point(lambda v, k2=pulse: int(v * (.45 + .45 * k2))))
        dr = ImageDraw.Draw(im)
        for pg in ep:
            dr.polygon(pg, fill=(245, 247, 249))
        # tagline
        for j, ch in enumerate(tag):
            dr.text((tx0 + j * adv, 306 * F), ch, font=tf, fill=(225, 6, 0), anchor='ls')
        dr.rectangle([P((150, 298)), P((400, 300))], fill=(110, 5, 0))
        dr.rectangle([P((800, 298)), P((1050, 300))], fill=(110, 5, 0))
        dr.text((600 * F, 342 * F), 'S Y M B I O T E X   //   A Y U S H   A M O L   N A V A L E', font=f_reg(12.5), fill=(150, 154, 160), anchor='ms')
        dr.text((34 * F, 40 * F), 'SYMBIOTE RESEARCH INTERFACE', font=f_reg(11), fill=(110, 113, 118), anchor='ls')
        dr.text((1166 * F, 40 * F), 'ACCESS: CLASSIFIED', font=f_reg(11), fill=(200, 12, 4), anchor='rs')
        dr.text((34 * F, 372 * F), 'HOST // SYMBIOTEX01', font=f_reg(11), fill=(110, 113, 118), anchor='ls')
        dr.text((1166 * F, 372 * F), 'STATUS // EVOLVING', font=f_reg(11), fill=(110, 113, 118), anchor='rs')
        # corner brackets
        m, l = 14, 26
        for (ax, ay, sx_, sy_) in [(m, m, 1, 1), (1200 - m, m, -1, 1), (1200 - m, 400 - m, -1, -1), (m, 400 - m, 1, -1)]:
            dr.line([P((ax, ay + sy_ * l)), P((ax, ay)), P((ax + sx_ * l, ay))], fill=(90, 92, 96), width=int(1.5 * F))
        frames.append(im.convert('RGB').resize((FW, FH), Image.LANCZOS))

    # shared palette for stable colours + small size
    strip = Image.new('RGB', (FW, FH * 4))
    for j, idx in enumerate([0, 9, 18, 27]):
        strip.paste(frames[idx], (0, j * FH))
    # reserve exact brand colours so quantization cannot dull them
    keys = [(225, 6, 0), (255, 42, 26), (245, 247, 249), (255, 255, 255), (200, 12, 4), (110, 5, 0), (150, 154, 160), (110, 113, 118), (90, 92, 96), (51, 54, 59), (34, 34, 34)]
    sw = Image.new('RGB', (FW, 40))
    sd2 = ImageDraw.Draw(sw)
    for j, c in enumerate(keys):
        sd2.rectangle([j * FW // len(keys), 0, (j + 1) * FW // len(keys), 40], fill=c)
    strip.paste(sw.resize((FW, FH * 4 // 4 // 2)), (0, 0))
    pal = strip.quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [fr.quantize(palette=pal, dither=Image.Dither.NONE) for fr in frames]
    out = f'{B.ROOT}/assets/banner.gif'
    q[0].save(out, save_all=True, append_images=q[1:], duration=70, loop=0, optimize=True, disposal=1)
    import os
    print('gif', os.path.getsize(out) // 1024, 'KB', FW, 'x', FH, N, 'frames')


if __name__ == '__main__':
    main()
