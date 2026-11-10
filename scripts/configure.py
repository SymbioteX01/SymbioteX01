#!/usr/bin/env python3
"""Fill the SYMBIOTEX README placeholders from profile.config.json.

Usage:   python scripts/configure.py            (apply)
         python scripts/configure.py --check    (report what is still pending, change nothing)
Only touches text between <!--@NAME--> ... <!--/@NAME--> markers. Safe to re-run.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / 'README.md'
CONFIG = ROOT / 'profile.config.json'
DEFAULTS = {
    "LINKEDIN": "<img src=\"https://img.shields.io/badge/LINKEDIN-NOT%20CONFIGURED-0d0d0d?style=for-the-badge&logo=linkedin&logoColor=555555\" alt=\"LinkedIn (not configured yet)\">",
    "EMAIL": "<img src=\"https://img.shields.io/badge/EMAIL-NOT%20CONFIGURED-0d0d0d?style=for-the-badge&logoColor=555555\" alt=\"Email (not configured yet)\">",
    "P1_REPO": "<code>REPOSITORY ▸ [ LINK PENDING ]</code>",
    "P1_STACK": "<code>STACK ▸ [ PENDING CONFIRMATION ]</code>",
    "P1_STATUS": "",
    "P2_REPO": "<code>REPOSITORY ▸ [ LINK PENDING ]</code>",
    "P2_STACK": "<code>STACK ▸ [ PENDING CONFIRMATION ]</code>",
    "P2_STATUS": "",
    "P3_REPO": "<code>REPOSITORY ▸ [ LINK PENDING ]</code>",
    "P3_STACK": "<code>STACK ▸ [ PENDING CONFIRMATION ]</code>",
    "P3_STATUS": "",
    "P4_REPO": "<code>REPOSITORY ▸ [ LINK PENDING ]</code>",
    "P4_STACK": "<code>STACK ▸ [ PENDING CONFIRMATION ]</code>",
    "P4_STATUS": "",
    "P5_REPO": "<code>REPOSITORY ▸ [ LINK PENDING ]</code>",
    "P5_STACK": "<code>STACK ▸ [ PENDING CONFIRMATION ]</code>",
    "P5_STATUS": "",
    "A_CERT": "<sub><code>[ AWAITING VERIFIED ENTRY ]</code></sub>",
    "A_INTERN": "<sub><code>[ AWAITING VERIFIED ENTRY ]</code></sub>",
    "A_MILE": "<sub><code>[ AWAITING VERIFIED ENTRY ]</code></sub>",
    "A_HACK": "<sub><code>[ AWAITING VERIFIED ENTRY ]</code></sub>",
    "A_LEARN": "B.Tech in Information Technology — MIT Academy of Engineering, Pune"
}
SLUGS = {
    "Python": "python",
    "C": "c",
    "C++": "cplusplus",
    "JavaScript": "javascript",
    "HTML5": "html5",
    "CSS3": "css3",
    "React": "react",
    "TensorFlow": "tensorflow",
    "NumPy": "numpy",
    "Pandas": "pandas",
    "Matplotlib": "matplotlib",
    "Oracle SQL": "oracle",
    "Firebase": "firebase",
    "Git": "git",
    "GitHub": "github",
    "VS Code": "visualstudiocode",
    "Tableau": "tableau",
    "Power BI": "powerbi",
    "Canva": "canva",
    "Node.js": "nodedotjs",
    "Flask": "flask",
    "Java": "openjdk",
    "SQL": "mysql",
    "Scikit-learn": "scikitlearn",
    "Android": "android",
    "Flutter": "flutter",
    "TypeScript": "typescript",
    "Wireshark": "wireshark"
}
PROJECT_KEYS = ['campus-club-hub', 'netsage-ai', 'netpulse', 'hypoguard-glucoguard-ai', 'safebite']
LOG_KEYS = {'A_CERT': 'certifications', 'A_LEARN': 'technical_learning', 'A_INTERN': 'internships',
            'A_MILE': 'project_milestones', 'A_HACK': 'hackathons'}


def enc(t):
    return t.replace('-', '--').replace('_', '__').replace(' ', '%20').replace('+', '%2B').replace('/', '%2F')


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build(cfg):
    out = dict(DEFAULTS)
    li = (cfg.get('linkedin_url') or '').strip()
    if li:
        out['LINKEDIN'] = (f'<a href="{li}"><img src="https://img.shields.io/badge/LINKEDIN-CONNECT-0d0d0d?style=for-the-badge&logo=linkedin&logoColor=E10600" alt="LinkedIn"></a>')
    em = (cfg.get('email') or '').strip()
    if em:
        out['EMAIL'] = (f'<a href="mailto:{em}"><img src="https://img.shields.io/badge/EMAIL-SEND%20SIGNAL-0d0d0d?style=for-the-badge" alt="Email"></a>')
    for n, key in enumerate(PROJECT_KEYS, 1):
        p = (cfg.get('projects') or {}).get(key) or {}
        if (p.get('repo') or '').strip():
            out[f'P{n}_REPO'] = (f'<a href="{p["repo"].strip()}"><img src="https://img.shields.io/badge/REPOSITORY-OPEN%20FILE-0d0d0d?style=flat-square&logo=github&logoColor=E10600" alt="Repository for {key}"></a>')
        stack = [s.strip() for s in (p.get('stack') or []) if s.strip()]
        if stack:
            imgs = []
            for s in stack:
                u = f'https://img.shields.io/badge/{enc(s)}-0d0d0d?style=flat-square'
                if s in SLUGS:
                    u += f'&logo={SLUGS[s]}&logoColor=E10600'
                imgs.append(f'<img src="{u}" alt="{esc(s)}">')
            out[f'P{n}_STACK'] = ' '.join(imgs)
        if (p.get('status') or '').strip():
            out[f'P{n}_STATUS'] = f'<code>STATUS ▸ {esc(p["status"].strip().upper())}</code>'
    log = cfg.get('log') or {}
    for region, key in LOG_KEYS.items():
        items = [esc(i.strip()) for i in (log.get(key) or []) if i.strip()]
        if items:
            joined = '<br>'.join(items)
            out[region] = (DEFAULTS[region] + '<br>' + joined) if region == 'A_LEARN' else joined
    return out


def main():
    check = '--check' in sys.argv
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    text = README.read_text(encoding='utf-8')
    new = build(cfg)
    pending = []
    for name, html in new.items():
        pat = re.compile(rf'<!--@{name}-->.*?<!--/@{name}-->', re.S)
        if not pat.search(text):
            print(f'warning: marker {name} not found in README.md')
            continue
        if html == DEFAULTS[name] and name != 'A_LEARN' and DEFAULTS[name]:
            pending.append(name)
        if not check:
            text = pat.sub(lambda m: f'<!--@{name}-->{html}<!--/@{name}-->', text)
    if check:
        print('Still pending (using placeholders):', ', '.join(pending) if pending else 'none')
    else:
        README.write_text(text, encoding='utf-8')
        print('README.md updated.')
        print('Still pending:', ', '.join(pending) if pending else 'none')


if __name__ == '__main__':
    main()
