# Customization Guide

## Filling in placeholders

Everything that needs your confirmation sits between marker comments in `README.md`, for example
`<!--@P1_REPO-->…<!--/@P1_REPO-->`. You never edit those by hand: put your values in `profile.config.json` and run the script.

```json
{
  "linkedin_url": "https://www.linkedin.com/in/your-real-id",
  "email": "you@example.com",
  "projects": {
    "campus-club-hub": {
      "repo": "https://github.com/SymbioteX01/campus-club-hub",
      "stack": ["React", "Firebase"],
      "status": "In development"
    }
  },
  "log": {
    "certifications": ["Certificate name, issuer, year"],
    "hackathons": ["Event name, year, outcome"]
  }
}
```

(The values above are examples of the format only. Use your own verified details.)

```bash
python scripts/configure.py --check   # list what is still a placeholder
python scripts/configure.py           # write your values into README.md
```

Rules of the script:

- An empty value keeps the placeholder, so you can fill things in gradually.
- It only rewrites text inside the markers and is safe to re-run.
- `stack` entries that match a known technology (for example `Python`, `React`, `Firebase`, `TensorFlow`) get its logo. Other names appear as plain text badges.
- `status` appears only if you provide it. Leave it empty unless it is verified.
- Entries under `log` are listed under the matching Clearance Log row. `technical_learning` is added beneath the existing education line.

| Marker | What it controls |
|---|---|
| `LINKEDIN`, `EMAIL` | Contact buttons (shown as "NOT CONFIGURED" until set) |
| `P1_…` to `P5_…` | Project 1 to 5: `STACK`, `REPO`, `STATUS` |
| `A_CERT`, `A_LEARN`, `A_INTERN`, `A_MILE`, `A_HACK` | Clearance Log rows |

Project order: 1 Campus Club Hub, 2 NetSage AI, 3 NetPulse, 4 HypoGuard / GlucoGuard AI, 5 SafeBite.

If you would rather not show an empty Clearance Log row (for example Internship), delete that whole `<tr>…</tr>` line from `README.md`.

## Palette

All assets share one palette. To retheme, find and replace the hex values across `assets/**/*.svg` and in the stat-card URLs in `README.md` (colours there are written without `#`).

| Role | Hex |
|---|---|
| Background | `#000000`, panels `#050505` / `#0A0A0A` |
| Blood red (primary accent) | `#E10600` |
| Hot red (pulses, highlights) | `#FF2A1A` |
| Metallic silver (body text) | `#C9CDD2` |
| White highlight | `#F2F4F6` |
| Dim label grey | `#6B7078` |
| Borders | `#2A2A2A` |

## Editing text inside SVGs

Open any SVG in a text editor and search for the visible words.

- **Dossier fields:** `assets/identity-card.svg`. Each row is a `LABEL` text plus a value text. Keep values under about 42 characters or they will run past the right edge.
- **Terminal lines:** `assets/terminal.svg` is generated with timed reveals, so edit it through the generator described below rather than by hand.
- **Project file titles:** `assets/projects/file-01.svg` to `file-05.svg`.
- **Banner name line:** `assets/banner.svg`, near the bottom of the file (`S Y M B I O T E X // A Y U S H …`).

## Regenerating all assets

The SVGs and the GIF were produced by small Python scripts. They are included in `scripts/build/` so you can change copy or colours and rebuild.

```bash
pip install pillow numpy
python scripts/build/build_svgs.py     # all SVG assets
python scripts/build/build_gif.py      # assets/banner.gif
python scripts/build/build_readme.py   # README.md, configure.py, workflow
```

Note that `build_readme.py` regenerates `README.md` from its template. Run it **before** `scripts/configure.py`, not after.

The generators write into the repository root automatically (two folders above `scripts/build/`). The GIF script needs the DejaVu Sans Mono font (present on most Linux systems); edit the `FONT` paths at the top of `build_gif.py` for macOS or Windows.

## Using `banner.gif`

The README uses the lighter, sharper `assets/banner.svg`. `assets/banner.gif` is the same banner rendered as an animated GIF (960 × 320, about 1 MB). Use it where SVG is not accepted: the repository social preview (Settings > General > Social preview, which needs a PNG or JPG, so export one frame), LinkedIn, Discord, slides, or as a drop-in replacement if SVG ever misbehaves:

```html
<img src="assets/banner.gif" alt="SYMBIOTEX — WE ARE VENOM." width="100%">
```

## Stats services

| Card | URL base | Customise with |
|---|---|---|
| Stats and languages | `github-readme-stats.vercel.app` | Parameters documented at <https://github.com/anuraghazra/github-readme-stats> |
| Streak | `streak-stats.demolab.com` | <https://github.com/DenverCoder1/github-readme-streak-stats> |
| Activity graph | `github-readme-activity-graph.vercel.app` | <https://github.com/Ashutosh00710/github-readme-activity-graph> |

If a card is unreliable for you, delete its `<img>` line. Nothing else depends on it.
