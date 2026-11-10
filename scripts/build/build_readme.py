#!/usr/bin/env python3
"""SYMBIOTEX build — part 2: README.md, scripts/configure.py, profile.config.json, workflow."""
import json
from build_svgs import W

USER = 'SymbioteX01'
PORTFOLIO = 'https://ayushnavalemit.github.io/portfolio/'

SLUGS = {'Python': 'python', 'C': 'c', 'C++': 'cplusplus', 'JavaScript': 'javascript', 'HTML5': 'html5', 'CSS3': 'css3',
         'React': 'react', 'TensorFlow': 'tensorflow', 'NumPy': 'numpy', 'Pandas': 'pandas', 'Matplotlib': 'matplotlib',
         'Oracle SQL': 'oracle', 'Firebase': 'firebase', 'Git': 'git', 'GitHub': 'github', 'VS Code': 'visualstudiocode',
         'Tableau': 'tableau', 'Power BI': 'powerbi', 'Canva': 'canva', 'Node.js': 'nodedotjs', 'Flask': 'flask',
         'Java': 'openjdk', 'SQL': 'mysql', 'Scikit-learn': 'scikitlearn', 'Android': 'android', 'Flutter': 'flutter',
         'TypeScript': 'typescript', 'Wireshark': 'wireshark'}


def enc(t):
    return (t.replace('-', '--').replace('_', '__').replace(' ', '%20').replace('+', '%2B').replace('/', '%2F'))


def badge(name, style='for-the-badge', logo=True, color='0d0d0d', logo_color='E10600'):
    u = f'https://img.shields.io/badge/{enc(name)}-{color}?style={style}'
    if logo and name in SLUGS:
        u += f'&logo={SLUGS[name]}&logoColor={logo_color}'
    return f'<img src="{u}" alt="{name}">'


def cat_row(label, items):
    return (f'<tr><td align="right" width="150"><sub><code>{label}</code></sub></td><td>'
            + ' '.join(badge(i) for i in items) + '</td></tr>')


# ---------- placeholder regions: (name -> default html). configure.py swaps these ----------
PENDING = '<sub><code>[ AWAITING VERIFIED ENTRY ]</code></sub>'
LI_OFF = f'<img src="https://img.shields.io/badge/LINKEDIN-NOT%20CONFIGURED-0d0d0d?style=for-the-badge&logo=linkedin&logoColor=555555" alt="LinkedIn (not configured yet)">'
EM_OFF = f'<img src="https://img.shields.io/badge/EMAIL-NOT%20CONFIGURED-0d0d0d?style=for-the-badge&logoColor=555555" alt="Email (not configured yet)">'
REPO_OFF = '<code>REPOSITORY ▸ [ LINK PENDING ]</code>'
STACK_OFF = '<code>STACK ▸ [ PENDING CONFIRMATION ]</code>'
LEARN_BASE = 'B.Tech in Information Technology — MIT Academy of Engineering, Pune'

DEFAULTS = {'LINKEDIN': LI_OFF, 'EMAIL': EM_OFF}
for n in range(1, 6):
    DEFAULTS[f'P{n}_REPO'] = REPO_OFF
    DEFAULTS[f'P{n}_STACK'] = STACK_OFF
    DEFAULTS[f'P{n}_STATUS'] = ''
for k in ['A_CERT', 'A_INTERN', 'A_MILE', 'A_HACK']:
    DEFAULTS[k] = PENDING
DEFAULTS['A_LEARN'] = LEARN_BASE


def region(name):
    return f'<!--@{name}-->{DEFAULTS[name]}<!--/@{name}-->'


# ---------- external services ----------
STAT_COLORS = 'bg_color=000000&title_color=E10600&text_color=C9CDD2&icon_color=E10600&border_color=2A2A2A&hide_border=false'
STATS = f'https://github-readme-stats.vercel.app/api?username={USER}&show_icons=true&{STAT_COLORS}&custom_title=SYMBIOTE%20TELEMETRY&rank_icon=github'
LANGS = f'https://github-readme-stats.vercel.app/api/top-langs/?username={USER}&layout=compact&langs_count=6&{STAT_COLORS}&custom_title=DOMINANT%20LANGUAGES'
STREAK = (f'https://streak-stats.demolab.com?user={USER}&theme=dark&background=000000&border=2A2A2A&stroke=2A2A2A&ring=E10600&fire=E10600'
          '&currStreakNum=F2F4F6&currStreakLabel=E10600&sideNums=F2F4F6&sideLabels=C9CDD2&dates=8A9097&hide_border=false')
ACT = (f'https://github-readme-activity-graph.vercel.app/graph?username={USER}&bg_color=000000&color=C9CDD2&line=E10600&point=F2F4F6'
       '&area=true&area_color=E10600&hide_border=true&custom_title=ACTIVITY%20SIGNAL')

PROJ = [
    ('01', 'Campus Club Hub', 'A centralized campus platform for club discovery, event management, and student memberships. '
     'Initially designed for MITAOE, with an architecture intended to support multiple colleges.'),
    ('02', 'NetSage AI', 'An AI-assisted network analysis project focused on network traffic analysis, anomaly detection, and network troubleshooting.'),
    ('03', 'NetPulse', 'An intelligent network diagnostics concept designed to identify Wi-Fi problems, explain root causes, and suggest fixes.'),
    ('04', 'HypoGuard / GlucoGuard AI', 'An AI-assisted hypoglycemia prediction and Indian food carbohydrate-counting project. '
     '<sub>A learning and research project, not medical advice.</sub>'),
    ('05', 'SafeBite', 'A canteen hygiene and food safety management application.'),
]

DIV = '<img src="assets/section-divider.svg" width="100%" alt="">'


def readme():
    r = []
    a = r.append
    a(f'''<!--
  SYMBIOTEX — GitHub profile README for {USER}
  This repository MUST be named exactly: {USER}   (public, with this README.md at the root)
  Pending items (LinkedIn, email, repo links, stacks, log entries) are filled by:
      1) editing profile.config.json   2) running: python scripts/configure.py
  See docs/CUSTOMIZATION.md and docs/DEPLOYMENT.md
-->

<div align="center">

<img src="assets/banner.svg" alt="SYMBIOTEX — WE ARE VENOM." width="100%">

<p>
<a href="#symbiote-dossier"><code>DOSSIER</code></a>&nbsp;&nbsp;
<a href="#technical-arsenal"><code>ARSENAL</code></a>&nbsp;&nbsp;
<a href="#classified-project-files"><code>PROJECT FILES</code></a>&nbsp;&nbsp;
<a href="#symbiote-telemetry"><code>TELEMETRY</code></a>&nbsp;&nbsp;
<a href="#clearance-log"><code>CLEARANCE LOG</code></a>&nbsp;&nbsp;
<a href="#establish-connection"><code>CONNECT</code></a>
</p>

<img src="assets/terminal.svg" alt="Terminal: SYSTEM INITIALIZED. HOST SYMBIOTEX01. IDENTITY AYUSH NAVALE. STATUS EVOLVING. MISSION BUILDING INTELLIGENT SYSTEMS." width="78%">

<br><br>

<img src="assets/venom-eyes.svg" alt="" width="42%">

</div>

<p align="center">
I'm <b>Ayush Amol Navale</b>, an Information Technology student at MIT Academy of Engineering, Pune.<br>
I'm interested in how AI can make everyday systems — campuses, networks, canteens, health tools — a little smarter,<br>
and I build projects to find out what works. <b>Explore. Experiment. Build. Evolve.</b>
</p>

{DIV}

<h2 align="center">SYMBIOTE DOSSIER</h2>

<div align="center">
<img src="assets/identity-card.svg" alt="Dossier: Ayush Amol Navale, GitHub SymbioteX01. B.Tech Information Technology at MIT Academy of Engineering, Pune, India. Interests: AI, software development, networks, data. Status: evolving." width="100%">
</div>

<br>

**AI and software journey.** My toolkit covers core programming (Python, C, C++, JavaScript), web front-end (HTML, CSS, React),
data and AI libraries (TensorFlow, NumPy, Pandas, Matplotlib), databases, and analytics tools. My projects point that toolkit at problems
I actually run into: finding clubs on campus, diagnosing slow Wi-Fi, keeping canteens hygienic, and making glucose management easier to reason about.

**Current learning direction**

- Applied AI and machine learning
- Intelligent tools for networks and health technology
- Turning project ideas into complete, usable software

{DIV}

<h2 align="center">TECHNICAL ARSENAL</h2>

<div align="center">
<sub>What I work with. I don't rate myself on a scale — I'm a student, and the whole point is to keep evolving.</sub>
<br><br>
<table>
''')
    a(cat_row('PROGRAMMING', ['Python', 'C', 'C++', 'JavaScript']))
    a(cat_row('FRONTEND', ['HTML5', 'CSS3', 'React']))
    a(cat_row('AI &amp; DATA', ['TensorFlow', 'NumPy', 'Pandas', 'Matplotlib']))
    a(cat_row('DATABASES', ['Oracle SQL', 'Firebase']))
    a(cat_row('TOOLS', ['Git', 'GitHub', 'VS Code', 'Tableau', 'Power BI', 'Canva']))
    a(f'''</table>
</div>

{DIV}

<h2 align="center">CLASSIFIED PROJECT FILES</h2>

<p align="center"><sub>Repository links and stacks are shown only once I've confirmed them. Nothing here is padded.</sub></p>
''')
    for n, (num, title, desc) in enumerate(PROJ, 1):
        a(f'''
<img src="assets/projects/file-{num}.svg" width="100%" alt="Project file {num}: {title}">

{desc}<br>
{region(f'P{n}_STACK')}<br>
{region(f'P{n}_REPO')} {region(f'P{n}_STATUS')}
''')
    a(f'''
{DIV}

<h2 align="center">SYMBIOTE TELEMETRY</h2>

<div align="center">

<table>
<tr>
<td><img src="{STATS}" alt="GitHub stats card for {USER}" width="420"></td>
<td><img src="{LANGS}" alt="Most-used languages card for {USER}" width="320"></td>
</tr>
</table>

<img src="{STREAK}" alt="Contribution streak card for {USER}" width="640">

<br>

<img src="{ACT}" alt="Contribution activity graph for {USER}" width="100%">

<br>

<img src="assets/animations/contribution-snake.svg" alt="Symbiote crawling across the contribution calendar" width="100%">

<sub>Live cards come from third-party services (github-readme-stats, streak-stats, github-readme-activity-graph) and can be slow or rate-limited;
if one is blank, open <a href="https://github.com/{USER}">the profile</a> for the source data. The crawler is generated by a GitHub Action in this repository.</sub>

</div>

{DIV}

<h2 align="center">CLEARANCE LOG</h2>

<p align="center"><sub>Verified entries only. Anything unconfirmed stays marked as pending.</sub></p>

<div align="center">
<table>
<tr><td align="right"><sub><code>CERTIFICATIONS</code></sub></td><td>{region('A_CERT')}</td></tr>
<tr><td align="right"><sub><code>TECHNICAL LEARNING</code></sub></td><td>{region('A_LEARN')}</td></tr>
<tr><td align="right"><sub><code>INTERNSHIP</code></sub></td><td>{region('A_INTERN')}</td></tr>
<tr><td align="right"><sub><code>PROJECT MILESTONES</code></sub></td><td>{region('A_MILE')}</td></tr>
<tr><td align="right"><sub><code>HACKATHONS</code></sub></td><td>{region('A_HACK')}</td></tr>
</table>
</div>

{DIV}

<h2 align="center">ESTABLISH CONNECTION</h2>

<p align="center">
<a href="https://github.com/{USER}"><img src="https://img.shields.io/badge/GITHUB-{USER}-0d0d0d?style=for-the-badge&logo=github&logoColor=E10600" alt="GitHub: {USER}"></a>
<a href="{PORTFOLIO}"><img src="https://img.shields.io/badge/PORTFOLIO-ENTER-0d0d0d?style=for-the-badge&logo=githubpages&logoColor=E10600" alt="Portfolio"></a>
{region('LINKEDIN')}
{region('EMAIL')}
</p>

<div align="center">
<img src="assets/animations/symbiote-animation.svg" alt="WE ARE VENOM. WE ARE SYMBIOTEX." width="100%">
</div>
''')
    return '\n'.join(r)


# ---------- configure script ----------
CONFIGURE = r'''#!/usr/bin/env python3
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
DEFAULTS = __DEFAULTS__
SLUGS = __SLUGS__
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
'''

CONFIG_JSON = {
    "_help": "Fill in only what is real and verified, then run: python scripts/configure.py. Empty values keep the placeholder.",
    "linkedin_url": "",
    "email": "",
    "projects": {
        "campus-club-hub": {"repo": "", "stack": [], "status": ""},
        "netsage-ai": {"repo": "", "stack": [], "status": ""},
        "netpulse": {"repo": "", "stack": [], "status": ""},
        "hypoguard-glucoguard-ai": {"repo": "", "stack": [], "status": ""},
        "safebite": {"repo": "", "stack": [], "status": ""},
    },
    "log": {"certifications": [], "technical_learning": [], "internships": [], "project_milestones": [], "hackathons": []},
}

WORKFLOW = '''name: Generate Symbiote Snake

# Builds a contribution-snake SVG from the live contribution calendar of the repository owner
# and writes it to assets/animations/contribution-snake.svg (the file the README already references).
# Setup: Settings > Actions > General > Workflow permissions > "Read and write permissions". See docs/DEPLOYMENT.md.

on:
  schedule:
    - cron: "17 3 * * *"       # daily, 03:17 UTC
  workflow_dispatch:           # manual "Run workflow" button
  push:
    branches: [main]
    paths:
      - ".github/workflows/snake.yml"

permissions:
  contents: write              # needed to commit the generated SVG back to the repo

concurrency:
  group: symbiote-snake
  cancel-in-progress: true

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Generate snake SVG (red symbiote palette)
        uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/snake.svg?color_snake=#E10600&color_dots=#101010,#3a0a0f,#7a0f1c,#b3122a,#ff2a1a&color_dot_border=#262626

      - name: Validate output
        run: |
          test -s dist/snake.svg
          head -c 200 dist/snake.svg | grep -q "<svg"

      - name: Install into assets and commit if changed
        run: |
          mkdir -p assets/animations
          cp dist/snake.svg assets/animations/contribution-snake.svg
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add assets/animations/contribution-snake.svg
          if git diff --cached --quiet; then
            echo "Snake unchanged."
          else
            git commit -m "chore: refresh contribution snake"
            git pull --rebase origin "${GITHUB_REF_NAME}"
            git push origin "HEAD:${GITHUB_REF_NAME}"
          fi
'''

if __name__ == '__main__':
    from build_svgs import ROOT
    W('README.md', readme())
    W('scripts/configure.py', CONFIGURE.replace('__DEFAULTS__', json.dumps(DEFAULTS, ensure_ascii=False, indent=4)).replace('__SLUGS__', json.dumps(SLUGS, indent=4)))
    W('profile.config.json', json.dumps(CONFIG_JSON, indent=2, ensure_ascii=False) + '\n')
    W('.github/workflows/snake.yml', WORKFLOW)
    print('readme ok')
