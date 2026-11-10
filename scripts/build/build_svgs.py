#!/usr/bin/env python3
"""SYMBIOTEX asset generator — part 1: shared design system + all SVG assets."""
import os, re, math, random, hashlib

ROOT = os.environ.get('SYMBIOTEX_ROOT') or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def W(rel, txt):
    p = f'{ROOT}/{rel}'
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(txt)


# ---------- design tokens ----------
RED = '#E10600'; HOT = '#FF2A1A'; BLOOD = '#8E0000'
SIL = '#C9CDD2'; WHT = '#F2F4F6'; DIM = '#6B7078'; CH = '#141414'
MONO = "'SFMono-Regular','Consolas','Liberation Mono','Menlo','DejaVu Sans Mono',monospace"
CW = 0.6  # monospace advance in em


def head(w, h, title, desc, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="tt dd">'
            f'<title id="tt">{title}</title><desc id="dd">{desc}</desc><defs>{defs}</defs>')


def T(x, y, s, size=14, fill=SIL, anchor='start', weight='normal', ls=0, op=1, extra=''):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" letter-spacing="{ls}" opacity="{op}" {extra}>{s}</text>')


def brackets(w, h, m=14, l=24, color=SIL, op=.55, sw=1.5):
    p = (f'M{m} {m+l} V{m} H{m+l} M{w-m-l} {m} H{w-m} V{m+l} '
         f'M{w-m} {h-m-l} V{h-m} H{w-m-l} M{m+l} {h-m} H{m} V{h-m-l}')
    return f'<path d="{p}" fill="none" stroke="{color}" stroke-width="{sw}" opacity="{op}"/>'


# ---------- custom SYMBIOTEX letterforms (original geometry, no font dependency) ----------
LET = {
    'S': "M52 12 H12 V44 H48 V76 H8",
    'Y': "M8 10 L30 44 L52 10 M30 44 V80",
    'M': "M8 80 V10 L30 44 L52 10 V80",
    'B': "M10 10 V80 H36 L50 66 V56 L38 45 H10 M10 10 H36 L50 24 V34 L38 45",
    'I': "M18 10 H42 M18 80 H42 M30 10 V80",
    'O': "M20 10 H40 L52 22 V68 L40 80 H20 L8 68 V22 Z",
    'T': "M4 10 H56 M30 10 V80",
    'E': "M52 10 H10 V80 H52 M10 45 H44",
    'X': "M8 10 L52 80 M52 10 L8 80",
}
PITCH = 66
WORD = 'SYMBIOTEX'


def wordmark_group(gid='wm'):
    paths = ''.join(f'<path d="{LET[c]}" transform="translate({i*PITCH} 0)"/>' for i, c in enumerate(WORD))
    return f'<g id="{gid}" fill="none" stroke-linejoin="miter" stroke-linecap="butt">{paths}</g>'


WM_L, WM_R = 3, (len(WORD) - 1) * PITCH + 57  # local ink extents incl. stroke


# ---------- tendril generator (shared by SVG + GIF) ----------
def make_tendril(rng, x0, y0, dy, length, amp):
    pts = [(x0, y0)]
    cx, cy = x0, y0
    seg = length / 3
    for _ in range(3):
        ex = cx + rng.uniform(-amp, amp) * .8
        ey = cy + dy * seg
        c1 = (cx + rng.uniform(-amp, amp), cy + dy * seg * .33)
        c2 = (ex + rng.uniform(-amp, amp), ey - dy * seg * .33)
        pts += [c1, c2, (ex, ey)]
        cx, cy = ex, ey
    B = [pts[0]] + [(x + rng.uniform(-amp * .7, amp * .7), y + rng.uniform(-amp * .3, amp * .3)) for x, y in pts[1:]]
    return dict(A=pts, B=B, len=length, ph=rng.random())


def pstr(pts):
    f = lambda v: f'{v:.1f}'
    s = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(1, len(pts), 3):
        a, b, c = pts[i:i + 3]
        s += f' C{f(a[0])} {f(a[1])} {f(b[0])} {f(b[1])} {f(c[0])} {f(c[1])}'
    return s


def tendril_svg(t, rng, wbase=18):
    dA, dB = pstr(t['A']), pstr(t['B'])
    dur = rng.uniform(5, 9)
    beg = -rng.uniform(0, dur)
    L = t['len'] * 1.25
    pd = rng.uniform(2.6, 4.2)
    pb = -rng.uniform(0, pd)

    def a():
        return (f'<animate attributeName="d" values="{dA};{dB};{dA}" keyTimes="0;.5;1" calcMode="spline" '
                f'keySplines=".4 0 .6 1;.4 0 .6 1" dur="{dur:.2f}s" begin="{beg:.2f}s" repeatCount="indefinite"/>')
    cap = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
    s = f'<path d="{dA}" {cap} stroke="#222" stroke-width="{wbase}">{a()}</path>'
    s += f'<path d="{dA}" {cap} stroke="#070707" stroke-width="{wbase-5}">{a()}</path>'
    s += (f'<path d="{dA}" {cap} stroke="{HOT}" stroke-width="2.2" stroke-dasharray="22 {L+30:.0f}" opacity=".9">{a()}'
          f'<animate attributeName="stroke-dashoffset" from="{L+52:.0f}" to="0" dur="{pd:.2f}s" begin="{pb:.2f}s" repeatCount="indefinite"/></path>')
    return s


# ---------- venom eyes ----------
EYE_PTS = ((2, 2), (76, -8), (134, 62), (46, 72))
EYE = "M2 2 Q76 -8 134 62 Q46 72 2 2 Z"
EYE_CTR = (67, 32)
EYE_INNER = 67  # inner tip offset from eye centre (x)


def eyes_defs():
    return ('<linearGradient id="eyeFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/>'
            '<stop offset="1" stop-color="#cfd3d8"/></linearGradient>'
            '<filter id="eg" x="-40%" y="-80%" width="180%" height="260%"><feGaussianBlur stdDeviation="7"/></filter>')


def eyes_body(cx, cy, s=1.0, gap=26):
    out = ''
    for m in (1, -1):
        ex = cx - m * (gap / 2 + EYE_INNER * s)
        out += (f'<g transform="translate({ex:.1f} {cy}) scale({m*s} {s})"><g>'
                '<animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 .06;1 1;1 1" '
                'keyTimes="0;.88;.91;.94;1" dur="7s" repeatCount="indefinite"/>'
                f'<g transform="translate({-EYE_CTR[0]} {-EYE_CTR[1]})">'
                f'<path d="{EYE}" fill="#fff" filter="url(#eg)" opacity=".7">'
                '<animate attributeName="opacity" values=".4;.95;.4" dur="3.5s" repeatCount="indefinite"/></path>'
                f'<path d="{EYE}" fill="url(#eyeFill)"/></g></g></g>')
    return out


def banner_tendrils():
    rng = random.Random(11)
    L = []
    for x in [18, 64, 112, 164, 222]:
        L.append(make_tendril(rng, x, -10, 1, rng.uniform(80, 170), 24))
    for x in [1182, 1136, 1088, 1036, 978]:
        L.append(make_tendril(rng, x, -10, 1, rng.uniform(80, 170), 24))
    for x in [40, 100, 170, 1160, 1100, 1030]:
        L.append(make_tendril(rng, x, 410, -1, rng.uniform(60, 120), 22))
    return L


WM_SCALE = 1.7
WM_TX = 600 - WM_SCALE * (WM_L + WM_R) / 2
WM_TY = 118 - 5 * WM_SCALE


def build_banner():
    defs = (eyes_defs() + wordmark_group() +
            '<radialGradient id="bgGlow" cx=".5" cy="1" r=".75"><stop offset="0" stop-color="#3a0000" stop-opacity=".7"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="metal" gradientUnits="userSpaceOnUse" x1="0" y1="5" x2="0" y2="85">'
            '<stop offset="0" stop-color="#fff"/><stop offset=".38" stop-color="#d7dbe0"/>'
            '<stop offset=".5" stop-color="#8a9097"/><stop offset=".53" stop-color="#eceff2"/>'
            '<stop offset="1" stop-color="#7c828a"/></linearGradient>'
            '<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E10600" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#E10600" stop-opacity=".16"/><stop offset="1" stop-color="#E10600" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E10600" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#E10600"/></linearGradient>'
            '<linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E10600"/>'
            '<stop offset="1" stop-color="#E10600" stop-opacity="0"/></linearGradient>'
            '<filter id="glowRed" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>'
            f'<mask id="wmMask" maskUnits="userSpaceOnUse" x="-20" y="-10" width="640" height="110">'
            '<use href="#wm" xlink:href="#wm" stroke="#fff" stroke-width="10"/></mask>')
    s = head(1200, 400, 'SYMBIOTEX — WE ARE VENOM.',
             'Animated banner: glowing white eyes above the metallic SYMBIOTEX wordmark, with symbiote tendrils pulsing red energy.', defs)
    s += '<rect width="1200" height="400" fill="#000"/><rect width="1200" height="400" fill="url(#bgGlow)"/>'
    grid = ''.join(f'<path d="M{x} 0V400" />' for x in range(0, 1201, 50)) + ''.join(f'<path d="M0 {y}H1200"/>' for y in range(0, 401, 50))
    s += f'<g stroke="#fff" stroke-width=".6" opacity=".045">{grid}</g>'
    rng = random.Random(5)
    for t in banner_tendrils():
        s += tendril_svg(t, rng)
    s += ('<rect x="0" y="-60" width="1200" height="60" fill="url(#scan)"><animate attributeName="y" from="-60" to="400" '
          'dur="7s" repeatCount="indefinite"/></rect>')
    # wordmark
    s += f'<g transform="translate({WM_TX:.2f} {WM_TY:.2f}) scale({WM_SCALE})">'
    s += ('<use href="#wm" xlink:href="#wm" stroke="#E10600" stroke-width="16" filter="url(#glowRed)" opacity=".5">'
          '<animate attributeName="opacity" values=".3;.8;.3" dur="3.5s" repeatCount="indefinite"/></use>')
    s += '<use href="#wm" xlink:href="#wm" stroke="#33363b" stroke-width="12.5"/>'
    s += '<use href="#wm" xlink:href="#wm" stroke="url(#metal)" stroke-width="10"/>'
    s += ('<g mask="url(#wmMask)"><g transform="skewX(-20)"><rect x="-70" y="-10" width="46" height="110" fill="url(#sweep)">'
          '<animateTransform attributeName="transform" type="translate" values="0 0;760 0;760 0" keyTimes="0;.55;1" dur="6s" repeatCount="indefinite"/>'
          '</rect></g></g></g>')
    s += eyes_body(600, 60, .85, 28)
    # tagline
    s += f'<rect x="150" y="298" width="250" height="2" fill="url(#fadeL)" opacity=".8"/><rect x="800" y="298" width="250" height="2" fill="url(#fadeR)" opacity=".8"/>'
    s += T(600, 306, 'WE ARE VENOM.', 24, RED, 'middle', 'bold', 14)
    s += ('<circle cx="400" cy="299" r="3" fill="#fff"><animate attributeName="cx" values="150;400;150" dur="4s" repeatCount="indefinite"/>'
          '<animate attributeName="opacity" values="0;1;0" dur="4s" repeatCount="indefinite"/></circle>'
          '<circle cx="800" cy="299" r="3" fill="#fff"><animate attributeName="cx" values="1050;800;1050" dur="4s" repeatCount="indefinite"/>'
          '<animate attributeName="opacity" values="0;1;0" dur="4s" repeatCount="indefinite"/></circle>')
    s += T(600, 342, 'S Y M B I O T E X   //   A Y U S H   A M O L   N A V A L E', 12.5, SIL, 'middle', 'normal', 2, .75)
    # HUD
    s += T(34, 40, 'SYMBIOTE RESEARCH INTERFACE', 11, SIL, 'start', 'normal', 2, .6)
    s += T(1166, 40, 'ACCESS: CLASSIFIED', 11, RED, 'end', 'normal', 2, .9)
    s += T(34, 372, 'HOST // SYMBIOTEX01', 11, SIL, 'start', 'normal', 2, .6)
    s += T(1166, 372, 'STATUS // EVOLVING', 11, SIL, 'end', 'normal', 2, .6)
    s += ('<circle cx="996" cy="368" r="3.5" fill="#E10600"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    s += brackets(1200, 400, 14, 26)
    s += '</svg>'
    W('assets/banner.svg', s)


def build_eyes():
    s = head(600, 150, 'Venom-inspired eyes', 'Two glowing white slanted eyes in the dark, pulsing and blinking.', eyes_defs() +
             '<radialGradient id="v" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#3a0000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>')
    s += '<rect width="600" height="150" fill="#000"/><rect width="600" height="150" fill="url(#v)"/>'
    s += eyes_body(300, 75, 1.0, 34)
    s += '</svg>'
    W('assets/venom-eyes.svg', s)


def build_divider():
    defs = ('<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a3a3a" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#5a5d62"/><stop offset="1" stop-color="#3a3a3a" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="pl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E10600" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#FF2A1A"/></linearGradient>'
            '<linearGradient id="pr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF2A1A"/>'
            '<stop offset="1" stop-color="#E10600" stop-opacity="0"/></linearGradient>')
    s = head(1200, 44, 'Section divider', 'A thin line with red energy pulses travelling out from a central diamond, and small dripping tendrils.', defs)
    s += '<rect width="1200" height="44" fill="#000"/>'
    s += '<rect x="20" y="17" width="1160" height="1.5" fill="url(#ln)"/>'
    s += ('<rect x="600" y="16.5" width="140" height="2.5" fill="url(#pl)"><animate attributeName="x" from="600" to="-140" dur="3.6s" repeatCount="indefinite"/></rect>'
          '<rect x="460" y="16.5" width="140" height="2.5" fill="url(#pr)"><animate attributeName="x" from="460" to="1200" dur="3.6s" repeatCount="indefinite"/></rect>')
    for i, x in enumerate([180, 330, 520, 680, 870, 1020]):
        h = [12, 18, 10, 10, 18, 12][i]
        s += (f'<path d="M{x} 18 C{x-2} {18+h*.4} {x+2} {18+h*.7} {x} {18+h}" fill="none" stroke="#2c2c2c" stroke-width="3" stroke-linecap="round">'
              f'<animate attributeName="d" values="M{x} 18 C{x-2} {18+h*.4} {x+2} {18+h*.7} {x} {18+h};M{x} 18 C{x+2} {18+h*.4} {x-2} {18+h*.8} {x} {18+h*1.35};M{x} 18 C{x-2} {18+h*.4} {x+2} {18+h*.7} {x} {18+h}" '
              f'dur="{4+i*.7:.1f}s" repeatCount="indefinite"/></path>')
    s += ('<g transform="translate(600 18)"><path d="M0 -9 L9 0 L0 9 L-9 0 Z" fill="#000" stroke="#E10600" stroke-width="1.6"/>'
          '<path d="M0 -4 L4 0 L0 4 L-4 0 Z" fill="#E10600"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></path></g>')
    s += '</svg>'
    W('assets/section-divider.svg', s)


# ---------- typing terminal ----------
def build_terminal():
    FS, CWPX = 20, 20 * CW  # 12 px per column
    LH, X0, Y0 = 36, 40, 112
    lines = [('cmd', '$ ./boot symbiotex01'), ('sys', 'SYSTEM INITIALIZED...'),
             ('kv', 'HOST', 'SYMBIOTEX01', WHT), ('kv', 'IDENTITY', 'AYUSH NAVALE', WHT),
             ('kv', 'STATUS', 'EVOLVING', HOT), ('kv', 'MISSION', 'BUILDING INTELLIGENT SYSTEMS', WHT),
             ('kv', 'CREED', 'EXPLORE. EXPERIMENT. BUILD. EVOLVE.', WHT), ('last', '$ ')]
    CYCLE = 18.0
    DT = .05
    t = .6
    body = ''
    clips = ''
    for i, ln in enumerate(lines):
        y = Y0 + i * LH
        cols = 12 + len(ln[2]) if ln[0] == 'kv' else (2 if ln[0] == 'last' else len(ln[1]))
        s_t = t
        e_t = s_t + cols * DT
        t = e_t + .35
        times, vals, cx = [0.0], [0], [X0]
        for k in range(1, cols + 1):
            times.append((s_t + (k - 1) * DT) / CYCLE)
            vals.append(round(k * CWPX, 1))
        hide = (CYCLE - 1.4) / CYCLE
        times += [hide, 1.0]
        vals += [0, 0]
        kt = ';'.join(f'{x:.4f}' for x in times)
        vv = ';'.join(str(v) for v in vals)
        cid = f'c{i}'
        clips += (f'<clipPath id="{cid}"><rect x="{X0}" y="{y-FS}" width="{cols*CWPX:.1f}" height="{LH-4}">'
                  f'<animate attributeName="width" values="{vv}" keyTimes="{kt}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/></rect></clipPath>')
        g = f'<g clip-path="url(#{cid})">'
        if ln[0] == 'cmd':
            g += T(X0, y, '$', FS, RED, 'start', 'bold', 0, 1, f'textLength="{CWPX:.1f}"')
            g += T(X0 + 2 * CWPX, y, ln[1][2:], FS, SIL, 'start', 'normal', 0, 1, f'textLength="{(len(ln[1])-2)*CWPX:.1f}" lengthAdjust="spacing"')
        elif ln[0] == 'sys':
            g += T(X0, y, ln[1], FS, RED, 'start', 'bold', 0, 1, f'textLength="{len(ln[1])*CWPX:.1f}" lengthAdjust="spacing"')
        elif ln[0] == 'kv':
            g += T(X0, y, ln[1], FS, DIM, 'start', 'normal', 0, 1, f'textLength="{len(ln[1])*CWPX:.1f}" lengthAdjust="spacing"')
            g += T(X0 + 10 * CWPX, y, ':', FS, DIM)
            g += T(X0 + 12 * CWPX, y, ln[2], FS, ln[3], 'start', 'bold' if ln[3] == HOT else 'normal', 0, 1, f'textLength="{len(ln[2])*CWPX:.1f}" lengthAdjust="spacing"')
        else:
            g += T(X0, y, '$', FS, RED, 'start', 'bold')
        g += '</g>'
        body += g
        # cursor: follows typing for this line, last line blinks forever
        if ln[0] == 'last':
            vt = f'0;{s_t/CYCLE:.4f};{hide:.4f};1'
            body += (f'<g opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="{vt}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/>'
                     f'<rect x="{X0+2*CWPX:.1f}" y="{y-FS+3}" width="{CWPX*.8:.1f}" height="{FS}" fill="{RED}">'
                     f'<animate attributeName="opacity" values="1;0;1" dur=".9s" repeatCount="indefinite"/></rect></g>')
        else:
            cvals = ';'.join(str(round(X0 + v, 1)) for v in vals)
            vis = ['0'] + ['1'] * cols
            vis_t = times[:cols + 1]
            vis_t2 = vis_t + [(e_t + .3) / CYCLE, 1.0]
            vis += ['0', '0']
            body += (f'<rect y="{y-FS+3}" width="{CWPX*.8:.1f}" height="{FS}" fill="{RED}" x="{X0}">'
                     f'<animate attributeName="x" values="{cvals}" keyTimes="{kt}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="{";".join(vis)}" keyTimes="{";".join(f"{x:.4f}" for x in vis_t2)}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/></rect>')
    Wd, Hd = 860, 112 + 8 * LH - 10
    s = head(Wd, Hd, 'Terminal introduction',
             'Typing animation: SYSTEM INITIALIZED. HOST SYMBIOTEX01. IDENTITY AYUSH NAVALE. STATUS EVOLVING. MISSION BUILDING INTELLIGENT SYSTEMS. CREED EXPLORE, EXPERIMENT, BUILD, EVOLVE.',
             clips + '<linearGradient id="tb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E10600" stop-opacity=".9"/><stop offset="1" stop-color="#E10600" stop-opacity="0"/></linearGradient>')
    s += (f'<rect x=".5" y=".5" width="{Wd-1}" height="{Hd-1}" rx="10" fill="#050505" stroke="#2a2a2a"/>'
          f'<path d="M.5 40 V10.5 Q.5 .5 10.5 .5 H{Wd-10.5} Q{Wd-.5} .5 {Wd-.5} 10.5 V40 Z" fill="#101010"/>'
          f'<rect x="1" y="39" width="{Wd-2}" height="1.5" fill="url(#tb)"/>'
          '<circle cx="26" cy="21" r="6" fill="#E10600"/><circle cx="48" cy="21" r="6" fill="#333"/><circle cx="70" cy="21" r="6" fill="#333"/>')
    s += T(Wd / 2, 26, 'symbiote@symbiotex01: ~/profile', 13, DIM, 'middle')
    s += body
    s += '</svg>'
    W('assets/terminal.svg', s)


# ---------- identity card ----------
def build_identity():
    w, h = 1000, 500
    defs = (eyes_defs() +
            '<linearGradient id="scanV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E10600" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#E10600" stop-opacity=".2"/><stop offset="1" stop-color="#E10600" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="hl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E10600"/><stop offset="1" stop-color="#E10600" stop-opacity="0"/></linearGradient>'
            '<clipPath id="card"><rect x="0" y="0" width="1000" height="500"/></clipPath>')
    s = head(w, h, 'Symbiote dossier — Ayush Amol Navale',
             'Classified identity file. Name: Ayush Amol Navale. Handle: SymbioteX01. Education: B.Tech Information Technology, MIT Academy of Engineering, Pune, India. Interests: AI, software development, networks, data. Status: evolving.', defs)
    s += f'<rect width="{w}" height="{h}" fill="#050505"/>'
    s += f'<rect x="1" y="1" width="{w-2}" height="{h-2}" fill="none" stroke="#2a2a2a"/>'
    s += '<g stroke="#fff" stroke-width=".5" opacity=".035">' + ''.join(f'<path d="M0 {y}H1000"/>' for y in range(60, 500, 20)) + '</g>'
    s += T(40, 52, 'SYMBIOTE DOSSIER', 26, WHT, 'start', 'bold', 4)
    s += T(960, 40, 'FILE SX-01', 12, SIL, 'end', 'normal', 2, .7) + T(960, 58, 'CLASSIFICATION: PERSONAL // LEVEL RED', 12, RED, 'end', 'normal', 2)
    s += '<rect x="40" y="72" width="920" height="2" fill="url(#hl)"/>'
    # emblem panel
    s += '<rect x="40" y="100" width="230" height="300" fill="#0a0a0a" stroke="#2a2a2a"/>'
    s += '<g clip-path="url(#card)">' + '<g transform="translate(155 220) scale(.6)">' + eyes_body(0, 0, 1.0, 34) + '</g></g>'
    s += T(155, 306, 'HOST', 11, DIM, 'middle', 'normal', 3) + T(155, 330, 'SYMBIOTEX01', 18, WHT, 'middle', 'bold', 2)
    s += '<rect x="40" y="0" width="230" height="46" fill="url(#scanV)"><animate attributeName="y" values="100;354;100" dur="5s" repeatCount="indefinite"/></rect>'
    s += f'<g transform="translate(155 372) rotate(-6)"><rect x="-82" y="-16" width="164" height="26" fill="none" stroke="{RED}" stroke-width="2" opacity=".85"/>' + T(0, 2, 'ACCESS GRANTED', 14, RED, 'middle', 'bold', 2, .95) + '</g>'
    rows = [('NAME', 'Ayush Amol Navale'), ('HANDLE', 'SymbioteX01'), ('EDUCATION', 'B.Tech, Information Technology'),
            ('INSTITUTION', 'MIT Academy of Engineering'), ('LOCATION', 'Pune, India'),
            ('ROLE', 'AI Enthusiast / Developer / Problem Solver'), ('INTERESTS', 'AI, software, networks, data'),
            ('DIRECTION', 'Applied AI, data, usable software')]
    for i, (k, v) in enumerate(rows):
        y = 128 + i * 38
        s += T(310, y, k, 12, DIM, 'start', 'normal', 2.5)
        s += T(450, y, v, 18, WHT if i < 2 else SIL, 'start', 'bold' if i < 2 else 'normal')
        s += f'<path d="M310 {y+12} H960" stroke="#1f1f1f" stroke-width="1"/>'
    s += f'<rect x="0" y="430" width="{w}" height="70" fill="#0a0a0a"/><rect x="0" y="430" width="{w}" height="1" fill="#2a2a2a"/>'
    s += '<circle cx="52" cy="465" r="5" fill="#E10600"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>'
    s += T(68, 470, 'STATUS: EVOLVING', 15, HOT, 'start', 'bold', 2)
    s += T(960, 470, 'EXPLORE. EXPERIMENT. BUILD. EVOLVE.', 15, SIL, 'end', 'normal', 2)
    s += brackets(w, h, 8, 22, RED, .8)
    s += '</svg>'
    W('assets/identity-card.svg', s)


# ---------- project file banners ----------
PROJECTS = [
    ('01', 'CAMPUS CLUB HUB', 'WEB PLATFORM'),
    ('02', 'NETSAGE AI', 'AI // NETWORKS'),
    ('03', 'NETPULSE', 'DIAGNOSTICS CONCEPT'),
    ('04', 'HYPOGUARD / GLUCOGUARD AI', 'AI // HEALTH'),
    ('05', 'SAFEBITE', 'FOOD SAFETY APP'),
]


def build_projects():
    for num, title, typ in PROJECTS:
        w, h = 1000, 124
        defs = ('<linearGradient id="sc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E10600" stop-opacity="0"/>'
                '<stop offset=".5" stop-color="#E10600" stop-opacity=".22"/><stop offset="1" stop-color="#E10600" stop-opacity="0"/></linearGradient>'
                '<clipPath id="cp"><rect width="1000" height="124"/></clipPath>')
        s = head(w, h, f'Project file {num}: {title}', f'Classified project file {num}. {title}. Type: {typ}.', defs)
        s += f'<rect width="{w}" height="{h}" fill="#070707"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" fill="none" stroke="#262626"/>'
        s += f'<rect x="0" y="0" width="10" height="{h}" fill="{RED}"/>'
        s += T(36, 32, f'CLASSIFIED PROJECT FILE  //  FILE {num}', 12, RED, 'start', 'normal', 2.5)
        s += T(36, 78, title, 32, WHT, 'start', 'bold', 2)
        s += T(36, 106, f'TYPE: {typ}', 12, DIM, 'start', 'normal', 2)
        # barcode from title hash
        hd = hashlib.md5(title.encode()).digest()
        x = 770
        bars = ''
        for i in range(36):
            bw = 1 + hd[i % 16] % 4
            if i % 2 == 0:
                bars += f'<rect x="{x}" y="52" width="{bw}" height="38" fill="#C9CDD2" opacity=".55"/>'
            x += bw + 1
            if x > 950:
                break
        s += bars
        s += T(950, 106, f'SX-{num}', 11, DIM, 'end', 'normal', 2)
        s += '<circle cx="944" cy="28" r="4" fill="#E10600"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        s += T(930, 32, 'FILE OPEN', 11, SIL, 'end', 'normal', 2, .8)
        s += f'<g clip-path="url(#cp)"><rect x="-200" y="0" width="200" height="{h}" fill="url(#sc)"><animate attributeName="x" from="-200" to="1000" dur="6s" repeatCount="indefinite"/></rect></g>'
        s += brackets(w, h, 6, 14, SIL, .35, 1)
        s += '</svg>'
        W(f'assets/projects/file-{num}.svg', s)


# ---------- symbiote footer animation ----------
def build_footer():
    w, h = 1200, 280
    rng = random.Random(23)
    s = head(w, h, 'WE ARE VENOM. WE ARE SYMBIOTEX.', 'Footer animation: dark tendrils rise from the bottom with red energy pulses around the closing line.',
             '<radialGradient id="g" cx=".5" cy="1" r=".8"><stop offset="0" stop-color="#3a0000" stop-opacity=".6"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
             '<linearGradient id="fl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E10600" stop-opacity="0"/><stop offset="1" stop-color="#E10600"/></linearGradient>'
             '<linearGradient id="fr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E10600"/><stop offset="1" stop-color="#E10600" stop-opacity="0"/></linearGradient>')
    s += f'<rect width="{w}" height="{h}" fill="#000"/><rect width="{w}" height="{h}" fill="url(#g)"/>'
    xs = list(range(10, 1200, 44))
    for x in xs:
        d = abs(x - 600) / 600
        ln = 40 + 150 * d ** 1.2 + rng.uniform(-10, 20)
        t = make_tendril(rng, x + rng.uniform(-10, 10), h + 10, -1, ln, 20)
        s += tendril_svg(t, rng, 16)
    s += '<rect x="250" y="102" width="700" height="1" fill="#2a2a2a"/>'
    s += T(600, 150, 'WE ARE VENOM.', 40, WHT, 'middle', 'bold', 10)
    s += T(600, 196, 'WE ARE SYMBIOTEX.', 40, RED, 'middle', 'bold', 10)
    s += '<rect x="400" y="218" width="400" height="1" fill="#2a2a2a"/>'
    s += T(600, 242, 'EXPLORE.  EXPERIMENT.  BUILD.  EVOLVE.', 12, SIL, 'middle', 'normal', 4, .7)
    s += ('<rect x="250" y="101" width="120" height="3" fill="url(#fl)"><animate attributeName="x" values="250;830;250" dur="5s" repeatCount="indefinite"/></rect>')
    s += brackets(w, h, 14, 26, SIL, .35)
    s += '</svg>'
    W('assets/animations/symbiote-animation.svg', s)


# ---------- contribution snake (neutral preview; overwritten by workflow with real data) ----------
def build_snake():
    cols, rows, pitch, cell = 53, 7, 16, 12
    mx, my = 26, 44
    w, h = 900, 176
    s = head(w, h, 'Contribution snake (preview)', 'A symbiote crawler moves across an empty contribution grid. Replaced by a data-driven snake when the GitHub Action runs.',
             '<linearGradient id="hd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF2A1A"/><stop offset="1" stop-color="#8E0000"/></linearGradient>')
    s += f'<rect width="{w}" height="{h}" fill="#000"/>'
    s += T(mx, 26, 'SYMBIOTE CRAWLER // PREVIEW — LIVE DATA APPEARS AFTER THE FIRST WORKFLOW RUN', 11, DIM, 'start', 'normal', 1.5)
    cells = ''
    for c in range(cols):
        for r in range(rows):
            cells += f'<rect x="{mx+c*pitch}" y="{my+r*pitch}" width="{cell}" height="{cell}" rx="2"/>'
    s += f'<g fill="#101010" stroke="#262626" stroke-width=".8">{cells}</g>'
    # path
    cx = lambda c: mx + c * pitch + cell / 2
    cy = lambda r: my + r * pitch + cell / 2
    d = f'M{-60} {cy(0)} H{cx(0)}'
    for c in range(cols):
        end = rows - 1 if c % 2 == 0 else 0
        d += f' V{cy(end)}'
        d += f' H{cx(c+1)}' if c < cols - 1 else f' H{w+60}'
    N = 14
    dt = .11
    # more-negative begin = further along the path, so the head (i=0) leads and the tail trails
    for i in reversed(range(N)):
        size = 14 - i * .5
        fill = 'url(#hd)' if i == 0 else '#' + f'{max(60, 225 - i * 12):02X}' + '0500'
        beg = -(N - i) * dt
        s += (f'<rect x="{-size/2:.1f}" y="{-size/2:.1f}" width="{size:.1f}" height="{size:.1f}" rx="3" fill="{fill}">'
              f'<animateMotion dur="40s" begin="{beg:.2f}s" repeatCount="indefinite" path="{d}"/></rect>')
    s += '</svg>'
    W('assets/animations/contribution-snake.svg', s)


def run_all():
    build_banner(); build_eyes(); build_divider(); build_terminal(); build_identity()
    build_projects(); build_footer(); build_snake()


if __name__ == '__main__':
    run_all()
    print('svgs ok')
