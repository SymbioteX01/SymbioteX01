# Asset Credits and External Dependencies

## Original assets (in this repository)

Everything under `assets/` was created for this profile with the generator scripts in `scripts/build/`:

| File | What it is |
|---|---|
| `assets/banner.svg`, `assets/banner.gif` | Hero banner: custom vector SYMBIOTEX lettering, eyes, animated tendrils. The GIF is the same artwork rendered as frames. |
| `assets/terminal.svg` | Typing-animation terminal intro |
| `assets/identity-card.svg` | Symbiote dossier card |
| `assets/section-divider.svg` | Animated section divider |
| `assets/venom-eyes.svg` | Animated eyes |
| `assets/projects/file-01.svg` to `file-05.svg` | Project file headers |
| `assets/animations/symbiote-animation.svg` | Footer tendril animation |
| `assets/animations/contribution-snake.svg` | Neutral preview crawler; replaced by real generated output when the snake workflow runs |

The SYMBIOTEX wordmark is drawn as vector geometry, not set in a font, so no typeface is bundled or licensed. Text inside SVGs uses system monospace fonts that the viewer's device already provides.

## Trademark note

The look of this profile is an original, fan-style homage to the **Venom** character and symbiote aesthetic. Venom is a character owned by Marvel. No official artwork, logos or screenshots are used, and "SYMBIOTEX" is a personal brand name. If you ever use this profile commercially, or want to be conservative, remove the Venom references ("WE ARE VENOM.", the eyes) and keep the rest of the design.

## External services (runtime dependencies)

These are fetched live by the visitor's browser or by GitHub's image proxy. None require tokens or secrets in this repository. Each is optional; the README keeps working if one is down.

| Service | Used for | Failure mode |
|---|---|---|
| [shields.io](https://shields.io) | Technology badges, project stack badges, contact buttons. Logos come from the [Simple Icons](https://simpleicons.org) set. | If a logo name is unknown, the badge renders with text only. If shields.io is down, badges are blank and show alt text. |
| [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) (public Vercel instance) | Stats card, top languages | Can hit rate limits and show an error image. Refreshing later usually fixes it. |
| [github-readme-streak-stats](https://github.com/DenverCoder1/github-readme-streak-stats) (`streak-stats.demolab.com`) | Contribution streak | Occasionally slow. |
| [github-readme-activity-graph](https://github.com/Ashutosh00710/github-readme-activity-graph) | Activity graph | Occasionally slow. |
| [Platane/snk](https://github.com/Platane/snk) (GitHub Action, `svg-only` mode) | Generates the contribution snake inside your own repository | If the Action fails, the preview crawler remains in place. |
| [actions/checkout](https://github.com/actions/checkout) | Standard GitHub Action | n/a |

Logos displayed in badges are trademarks of their respective owners and are used only to identify the technologies listed.

## Licences

Check each linked project's repository for its own licence terms. Add a `LICENSE` file to this repository if you want to state reuse terms for the original assets.
