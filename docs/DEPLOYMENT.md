# Deployment Guide

How to put SYMBIOTEX live on <https://github.com/SymbioteX01>.

GitHub shows a README on your profile only when it lives in a **public repository whose name is exactly your username**: `SymbioteX01`.

## 1. Create the profile repository

1. Go to <https://github.com/new>.
2. **Repository name:** `SymbioteX01` (exact spelling and capitalization; GitHub will show a note that this is a special repository).
3. Set visibility to **Public**.
4. Leave "Add a README" **unchecked** (this project already has one). Click **Create repository**.

## 2. Upload the files

Upload the **contents** of the `SymbioteX-Profile/` folder, not the folder itself. `README.md` must end up at the repository root.

### Option A: GitHub website (no tools needed)

1. Unzip `SymbioteX-Profile.zip`.
2. In the new repository, click **uploading an existing file**.
3. Open the unzipped `SymbioteX-Profile` folder, select everything inside it (`README.md`, `assets`, `docs`, `scripts`, `.github`, `profile.config.json`) and drag it into the browser. Folders are preserved when dragged in.
4. If your file manager hides folders starting with a dot, the `.github` folder may not be selected. Enable "show hidden files" and drag it in as well. It must contain `workflows/snake.yml`.
5. Commit directly to the `main` branch.

### Option B: Git command line

```bash
cd SymbioteX-Profile
git init -b main
git add .
git commit -m "feat: launch SYMBIOTEX profile"
git remote add origin https://github.com/SymbioteX01/SymbioteX01.git
git push -u origin main
```

## 3. Enable the contribution snake

The snake workflow commits a generated SVG back to the repository, so it needs write access:

1. Repository **Settings** > **Actions** > **General**.
2. Under **Workflow permissions**, choose **Read and write permissions** and save.
3. Open the **Actions** tab. If asked, click **I understand my workflows, go ahead and enable them**.
4. Select **Generate Symbiote Snake** > **Run workflow**.
5. When it finishes (about a minute), `assets/animations/contribution-snake.svg` is replaced by a snake built from your real contribution calendar. After that it refreshes daily at 03:17 UTC.

Until the first run, the README shows a neutral preview crawler on an empty grid (clearly labelled as a preview). It contains no contribution data.

If the run fails:

| Symptom | Fix |
|---|---|
| `Permission denied` / `403` on push | Step 3.2 was skipped. Set **Read and write permissions**. |
| `Platane/snk` step errors on the colour parameters | The query string in `snake.yml` follows the snk v3 documentation at the time of writing. Check <https://github.com/Platane/snk> for current option names, or delete everything after `snake.svg` to use the default palette. |
| Workflow never appears | `.github/workflows/snake.yml` was not uploaded. Re-add the hidden `.github` folder. |

## 4. Fill in the pending items

LinkedIn, email, project repository links, project tech stacks and the achievements log are intentionally left as placeholders until you confirm the real values. See `docs/CUSTOMIZATION.md`, section "Filling in placeholders".

Quick version: open `profile.config.json`, fill in what is true, then run:

```bash
python scripts/configure.py --check   # shows what is still pending
python scripts/configure.py           # applies your values to README.md
```

Commit the updated `README.md`.

## 5. Verify

Open <https://github.com/SymbioteX01> in a private window (so you see what visitors see) and check:

- [ ] Banner, terminal, dossier card and project file headers all render and animate.
- [ ] Stats cards load. If one shows a broken image, wait a minute and refresh; the free services can be rate-limited.
- [ ] GitHub and Portfolio buttons open the right pages.
- [ ] The footer animation shows at the bottom.

GitHub caches images aggressively through its proxy, so changes to an SVG can take a few minutes to appear.

## Stats cards for private contributions

The stats cards only count what GitHub exposes publicly. To include private contributions, enable **Contributions** > **Include private contributions on my profile** in your GitHub profile settings. No tokens are required for this project's setup.

## Known limits

- **Animations are always on.** SVG animation inside an `<img>` cannot read the visitor's reduced-motion preference. If that matters to you, replace `assets/banner.svg` with a still export or remove the animated assets from the README.
- **Fonts.** SVG text uses a monospace system-font stack (SF Mono, Consolas, Liberation Mono, Menlo, DejaVu Sans Mono). Spacing is stable, but letterforms differ slightly per operating system. The `SYMBIOTEX` wordmark is drawn as vector paths and looks identical everywhere.
- **No JavaScript.** GitHub strips scripts, iframes and CSS from READMEs. Everything here uses plain Markdown, GitHub-safe HTML, SVG and a GIF.
