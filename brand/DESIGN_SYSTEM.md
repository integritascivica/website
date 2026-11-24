# Integritas Civica — Design System

The self-contained design-system reference for this repo. Committed alongside
`tokens.json` in `brand/`. This is the source of truth for all visual styling;
read it before changing any UI. (The canonical system is also maintained as a
Claude design-system artifact, but this repo does not depend on that at build
or runtime — this file and `brand/tokens.json` are authoritative here.)

One accent color, three typefaces, and a strict split between the content
people read and the interface they operate.

## Principles

**One accent, two faces of it.** The brand runs on a single gold accent that
shows up differently by mode: burnt caramel (`#b45309`) in light mode, bright
gold (`#fcd34d`) in dark mode. This isn't two colors — it's one accent tuned
for each background. The split is a feature: caramel reads as grounded and
editorial, gold reads as the "gold standard" of verification. Both point at
trustworthiness, which is the whole job of a fact-checking product.

**Red and green are spoken for.** Semantic red and green mean one thing only —
removals and additions in revisions and diffs. They are never used
decoratively or as an accent. The gold accent was chosen specifically to sit
far from both so a glance never confuses an accent with a status.

**Content is serif, interface is sans, data is mono.** Three typefaces, three
jobs, no overlap:
- **Lora** sets everything meant to be *read*: mastheads, headlines, post and
  article body, pull quotes. Its gentle calligraphic warmth gives the content
  personality without tipping into playful or tabloid.
- **Inter** runs everything meant to be *operated* or *scanned*: buttons, nav,
  bylines, timestamps, section labels, status pills, source citations, chips.
- **JetBrains Mono** carries *data and machinery*: diff lines, raw source,
  reference IDs, and tabular counts.

## Color

Use the semantic tokens (CSS custom properties generated from
`brand/tokens.json`), never raw hex. Each resolves per theme automatically.

| Token | Role |
| --- | --- |
| `surface-page` / `surface-card` / `surface-sunken` | Backgrounds, from ground to raised to recessed |
| `ink` / `ink-muted` | Primary and secondary text |
| `rule` | Hairline borders and dividers |
| `accent` | Accent **fill**: buttons, nav selection, selection highlight, the wordmark dot |
| `accent-ink` | Text/icon **on** an accent fill (white on caramel, near-black on gold) |
| `accent-text` | Accent color for **small text on a surface** |
| `accent-tint` | Low-saturation accent wash for chips, selected rows, hover |
| `signal-add` / `signal-del` | Reserved green / red for additions and removals |
| `signal-add-bg` / `signal-del-bg` | Background fills behind addition / removal lines |

### The small-gold-text rule

This is the one place the two-color accent needs a third value. Pale gold is
too faint for small text on white, so:

- Gold as a **fill** (button, pill background, large block) → `accent`
  (`#b45309` light / `#fcd34d` dark).
- Gold as **small text or a small glyph on a light surface** (eyebrows, chips,
  ref IDs, links, the rating label) → `accent-text` (`#8a4206` light /
  `#fcd34d` dark). The deeper caramel keeps small gold legible on white. In
  dark mode both are the same bright gold, so the token resolves to the accent.

Button text always uses `accent-ink` — white on the caramel fill, near-black
on the gold fill — never the reverse, because white text on pale gold fails
contrast.

## Typography

Three families, generated into type classes from `brand/tokens.json`. Pick the
style from the group that matches the job:

- **Content (Lora)** — `display`, `headline`, `body`, `pullquote`
- **Interface (Inter)** — `ui-strong`, `ui`, `ui-small`, `eyebrow`
- **Data (JetBrains Mono)** — `mono`, `mono-num`

The reading tier is `body` (Lora, 17/28). When in doubt about whether text is
"content" or "interface," ask whether someone reads it in sentences (Lora) or
scans/acts on it (Inter). CSS variables for the families: `--font-serif`,
`--font-sans`, `--font-mono`.

## Theme switching

- `:root` is the light theme (default).
- Dark comes from `@media (prefers-color-scheme: dark)
  :root:not([data-theme="light"])` (system preference) and from an explicit
  `[data-theme="dark"]` (toggle).
- Keep all three in sync — the generator produces them together; don't
  hand-edit the generated CSS.

## The wordmark

**Integritas · Civica** set in Lora at display weight, with a raised middle
dot (interpunct) in the accent color. The dot follows the accent — caramel in
light mode, bright gold in dark — so it's consistent with every other accent
in the product.

The interpunct is period-appropriate: the Romans used exactly this mark to
separate words, which suits the Latin name. Give it generous letter-spacing
around the dot and raise it to the serif's optical midline.

Rules:
- Never recolor the whole wordmark in the accent on a light surface — the deep
  caramel reads thin on white at display weight. Keep the words in `ink` and
  let the dot carry the color.
- On a dark surface a full-gold wordmark is legible and bold; use it only
  where the mark stands alone (splash, exported card), not inline with reading
  text.
- Holds down to nav-bar scale (~16px cap height). Below that, drop the tagline.

## Components

### Button
Three weights: **primary** (`accent` fill, `accent-ink` text), **ghost**
(transparent, 1.5px `accent` inset border, `accent-text` label), **quiet**
(`ink-muted` text, no fill). One primary per action group. Radius
`radius-sm`, label in `ui-strong`. Disabled → 45% opacity, don't recolor.
Never white text on a pale-gold fill — that's what `accent-ink` is for.

### StatusPill
**Verified** (`accent-tint` bg, `accent-text` label — the only status that
uses the accent, because the accent means endorsement), **In review**
(`surface-sunken` bg, `ink-muted`), **Disputed** (`signal-del-bg` bg,
`signal-del` label). Label in `eyebrow`, radius `radius-pill`, leading dot in
the label color.

### Nav
Selected item: `ink` label in `ui-strong` with a 2px `accent` underline on the
nav's bottom rule. Inactive: `ink-muted`, no underline. The underline is the
selection signal, not a fill. For a vertical sidebar, move the 2px marker to
the leading edge and add an `accent-tint` row fill for the active item.

### DiffLine
Removals: `signal-del` on `signal-del-bg`. Additions: `signal-add` on
`signal-add-bg`. Set in `mono`. A corrected value inside an addition may take
an `accent-tint` highlight — the one place the accent enters a diff. These
colors are reserved; never use red/green where the meaning isn't
removed/added.

### SourceCard
A cited source: a **ref ID** (`[S1]`…) in `mono`, colored `accent-text`; a
**description** in `ui`; the **publisher** in `ui-small` muted; an optional
**link** in `ui-small` `accent-text`. Keep the ID column fixed-width so a
stacked list aligns. Source descriptions are interface text (Inter), scanned
not read. A source-quality tier, if shown, uses a StatusPill — never
red/green.

## Cross-surface mapping

| Surface | Masthead / titles | Reading body | Labels / data | Control |
| --- | --- | --- | --- | --- |
| **App** | Lora | Lora | Inter / JetBrains Mono | Full |
| **Website** | Lora | Lora | Inter / JetBrains Mono | Full |
| **Substack (Classic theme)** | Lora | Spectral | Substack defaults | Partial |

On Substack, Lora is available for the masthead/titles. The body is
**Spectral** — it pairs seamlessly with Lora and is built for on-screen
long-form reading. The accent reaches Substack mainly through the uploaded
wordmark logo and any available color settings.

## Fonts & licensing

All typefaces are SIL Open Font License (OFL 1.1): free for commercial use,
free to self-host and bundle, no UI attribution required. Don't sell the font
files standalone or rename a modified font to its reserved name. Include the
OFL license text alongside self-hosted font files.

- **Lora** — OFL 1.1
- **Inter** — OFL 1.1
- **JetBrains Mono** — OFL 1.1
- **Spectral** (Substack body) — OFL 1.1

Self-host for the app and website rather than relying on a CDN.

## Regenerating tokens

`tokens.css` is GENERATED from `brand/tokens.json` by
`brand/generate_tokens.py` — do not edit `tokens.css` by hand. When a token
changes, update `brand/tokens.json`, re-run the generator (the `tokens` build
step does this), and the change flows into the CSS. The same `tokens.json`
feeds both the app and the website; keep them on the same version.
