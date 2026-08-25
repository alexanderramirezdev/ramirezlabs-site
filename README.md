# ramirezlabs.app

Source for the Ramirez Labs site. Plain HTML, no build step, no framework.

```
index.html          studio landing page
404.html            not found
tokens.css          palette, reset, body and link styles — single source of truth
styles.css          sub-page layout, loaded after tokens.css
robots.txt
sitemap.xml
favicon.svg         browser tab
apple-touch-icon.png  180px, iOS home screen
icon-512.png        512px, maskable / PWA fallback
og.png              1200x630 link preview card

beth/               index.html · privacy.html · research.html
cairnskin/          index.html · privacy.html
clearchart/         index.html · privacy.html
florafang/          index.html · privacy.html
hakicheck/          index.html · privacy.html
peelback/           index.html · privacy.html
```

## Deploying

Connected to Cloudflare Pages. Pushing to `main` deploys automatically.

Build settings: no build command, output directory `/`.

Cloudflare Pages serves `404.html` for unmatched routes automatically; no
configuration needed.

## Stylesheets

`tokens.css` holds the palette, the reset, and the base body and link styles.
Every page loads it first. `styles.css` adds the sub-page document layout on
top; the landing page skips it and uses its own inline block instead, because
its masthead and hero don't share a layout with anything else.

The palette is defined in exactly one place. If a colour needs to change,
change `tokens.css` and nothing else.

## Adding an app

Create a folder named after the app containing `index.html` (support) and
`privacy.html`. App Store Connect requires a reachable URL for both before a
submission can go through.

Copy the head block from an existing page and update `canonical`, `og:title`,
`og:description`, and `og:url`. Leave `og:image` pointing at the shared
`/og.png` unless the app gets its own card.

Then add the app to three places, all easy to forget:

- the work section in `index.html`, with a 64x64 inline SVG mark
- `sitemap.xml`
- the project list in `404.html`

## App icons in the work section

Each project in `index.html` carries a 64x64 mark. Two kinds are supported and
they render identically:

- **Unshipped apps** use an inline `<svg class="mark">` drawn in the studio
  palette. Rounded by `svg.mark` in CSS.
- **Shipped apps** use `<img class="mark" src="/icons/appname.png" alt="">`
  pointing at the real App Store artwork, so someone who saw the icon here
  recognises it when they go looking for it. Rounded by `img.mark`.

To swap one when it ships, export the 1024 marketing icon from the asset
catalog, downscale to 192x192 (3x of the 64px slot), save it **square and
unmasked** into `icons/`, and replace the whole `<svg class="mark">...</svg>`
block with the one-line `<img>` tag. The corner radius is applied in CSS; do
not bake a rounded corner or a squircle mask into the PNG or it will be
double-rounded.

Do this per app as it ships. Mixing the two kinds is expected and fine.

Currently real artwork: FloraFang, HakiCheck. Still stylized: Cairn Skin,
Peelback Mechanic, ClearChart, B.E.T.H.

## Regenerating the images

`favicon.svg` is hand-written. The PNGs are generated from the same cairn
geometry by `tools/make_assets.py`, which needs `pillow` and a copy of IBM
Plex Mono. Re-run it only if the mark or the headline changes.

## Open TODOs in the source

Grep for `TODO(alex)`. Currently:

- `index.html` — swap Cairn Skin's status line and add the store link on approval
- `beth/research.html` — no TODO, but the per-build percentages are still
  described qualitatively. Add the numbers from the FINDINGS.md run tables
  when they are stable. Build A = macOS 27 beta, Build B = macOS 26.6.2.
