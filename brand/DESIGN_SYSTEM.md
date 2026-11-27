# Integritas Civica — Design System

The self-contained design-system reference for this repo. Committed alongside
`tokens.json` in `brand/`. This is the source of truth for all visual styling;
read it before changing any UI. (The canonical system is also maintained as a
Claude design-system artifact, but this repo does not depend on that at build
or runtime — this file and `brand/tokens.json` are authoritative here.)

One accent color, three typefaces, and a strict split between the content
people read and the interface they operate.

## Principles

**A calm, partisan-neutral ground.** The light theme uses a near-neutral,
faintly cool off-white (`#f6f7f7`), not a warm cream. For a political
publication this is deliberate: low-saturation reads as calm and lowers the
reader's guard, and a temperature-neutral ground signals no side before a word
is read. The warmth that makes the product feel personal and real comes from
Lora's letterforms and the gold accent, not the page. The dark theme stays warm
(brown-black ground, gold accent) — a different reading context with its own
character.

**One default accent, two faces of it.** The brand runs on a single gold
accent that shows up differently by mode: burnt caramel (`#b45309`) in light
mode, bright gold (`#fcd34d`) in dark mode. This isn't two colors — it's one
accent tuned for each background. The split is a feature: caramel reads as
grounded and editorial, gold reads as the "gold standard" of verification. The
gold is the **default**; the app lets a user override the accent at runtime.
When the accent is overridden, the override MUST also set `accent-ink` (the
on-accent text color) for the chosen color, or a pale custom accent gets white
text that fails contrast. Recompute `accent-text` too, or keep the gold value
only when the override is near gold.

**Red and green are spoken for.** Semantic red and green mean two related
things — removals/additions in diffs, and error/success UI states — and
nothing else. They are never used decoratively or as an accent. The gold
accent sits far from both so a glance never confuses an accent with a status.

**Warning is violet.** The warm band is taken — gold is the accent, red is
error — so warning moves out of it to violet (`status-warning`: `#7e22ce`
light / `#c084fc` dark, with `status-warning-bg` behind badges/banners). Violet
is the one hue clearly separable from accent, red, and green, and as a small
status color it carries none of the "overused brand purple" baggage. Pair it
with a ⚠ glyph for redundancy with color. Never use amber/orange for warnings;
amber is the accent.

**Categorical colors are separate from status.** Chips, speaker tags,
reference highlights, calendar dots, and chart series use `cat-1`…`cat-6` —
hues distinguishable from each other and from every semantic color. They never
signal status. Teal (`cat-1`) and cyan (`cat-3`) are close; don't rely on just
those two together. For charts needing few series, prefer cat-1/2/4/5 (teal,
blue, slate, plum) for maximum separation.

**Shape and fill say what a thing is.** Four visual languages, never mixed:
- **Solid fill = button** (an action). Primary is `accent`, secondary is neutral `surface-strong`, destructive is `signal-del`. No outlined buttons.
- **Underlined text = quiet button** (a minor or dismissive action such as Cancel). It has no button shape, so it looks like a link.
- **Outline = tag** (a category, topic, label or filter). Never solid, never a pill.
- **Pill = status** (verdict, tier, verified/disputed, warning). Never outlined, never clickable-looking.
A toggle is the one exception: outlined when off, solid `accent` when on. Everything rectangular shares one corner, `radius-xs` (4px); only pills and avatars are round.

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
| `surface-strong` | Fill of the secondary (neutral solid) button |
| `ink` / `ink-muted` | Primary and secondary text |
| `rule` | Hairline borders and dividers |
| `accent` | Accent **fill**: buttons, nav selection, selection highlight, the wordmark dot |
| `accent-ink` | Text/icon **on** an accent fill (white on caramel, near-black on gold) |
| `accent-text` | Accent color for **small text on a surface** |
| `accent-tint` | Low-saturation accent wash for chips, selected rows, hover |
| `accent-hover` | Hover and pressed fill for accent buttons (text stays `accent-ink`) |
| `signal-add` / `signal-del` | Reserved green / red for additions+success and removals+error |
| `signal-add-bg` / `signal-del-bg` | Backgrounds behind an addition/success or removal/error |
| `status-warning` / `status-warning-bg` | Violet warning/caution and its background |
| `backdrop` | Scrim behind modal dialogs and overlays |
| `cat-1`…`cat-6` | Categorical palette for chips, tags, highlights, chart series (never status) |

Shadows: `shadow-card` (resting), `shadow-menu` (dropdowns, popovers,
tooltips), `shadow-overlay` (modals). Spacing and radius tokens are in **rem**
so they scale with the app's 110% root font size — don't substitute px.
Spacing runs `space-0.5`…`space-12`. Radius has two values only: `radius-xs`
(4px) for everything rectangular (buttons, inputs, tags, cards, dialogs) and
`radius-pill` for status pills and avatars.

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

The reading tier is `body` (Lora, 17/28). The pixel sizes are for the app's dense interface; the website keeps its own fluid `rem`/`clamp()` sizes and takes only families, weights and line heights from the tokens. When in doubt about whether text is
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

**Integritas · Civica** set in Lora at display weight, with a middle dot
(interpunct) in the accent color. The dot follows the accent — caramel in light
mode, bright gold in dark — so it's consistent with every other accent in the
product.

The interpunct is period-appropriate: the Romans used exactly this mark to
separate words, which suits the Latin name. Give it ~0.2em of space on each
side and let it sit at the font's natural glyph height — do NOT nudge it
vertically. The dot bridges a lowercase `s` (end of "Integritas") and a capital
`C` (start of "Civica"), so there is no single "correct" centering to derive;
Lora's natural near-cap-height position reads as balanced. Set the words and dot
as plain inline text on one baseline (no `inline-flex` + `align-items: center`,
no `position/top` offset). A stray vertical offset is the bug to avoid here.

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
Every button is a **solid fill**, except the quiet tier. No outlined buttons:
an outline means a Tag.
- **Primary**: `accent` fill, `accent-ink` text. One per action group. An action
  repeated on every row of a list is secondary, not primary.
- **Secondary**: `surface-strong` fill, `ink` text. The neutral solid button;
  most former neutral-outline buttons become this.
- **Destructive (default)**: red underlined text (`signal-del`, no fill, no
  border). Every ordinary delete, discard or remove.
- **Destructive (confirm)**: `signal-del` fill, `surface-page` text (plain white
  fails contrast on the dark-theme red). ONLY the confirming action inside a
  confirmation dialog, paired with an underlined Cancel.
- **Quiet**: text only, styled as a link: underlined, `ink-muted` (or
  `accent-text`), `ink` on hover. For minor or dismissive actions (Cancel,
  Dismiss). Former neutral-outline buttons that were minor become quiet.
  Icon-only buttons are exempt from the underline.
- **Toggle**: outlined (`rule` border, `ink-muted` text) when off, solid `accent`
  with `accent-ink` when on. Change fill and color only, never font weight.
The old ghost (accent-outline) variant is removed. Radius `radius-xs`, label in
`ui-strong`. Disabled is 45% opacity, not a recolor.
Hover: primary goes to `accent-hover`. Focus ring: a 2px `accent` outline with a small offset on every focusable control. Border widths, layout widths and breakpoints are not tokens; set them locally.

### Tag
Categories, topics, labels, filters. **Outlined, never solid, never a pill.**
Rectangular, `radius-xs`, 1px border and text in the same color, regular weight.
Neutral tag: `rule` border, `ink-muted` text. Categorical tag: one `cat-*` hue
for border and text. A selected filter chip takes an `accent-tint` fill with an
`accent` border and `accent-text` label, a light wash and not a solid fill.

### StatusPill
**Verified** (`accent-tint` bg, `accent-text` label — the affirmative status of its set), **In review**
(`surface-sunken` bg, `ink-muted`), **Disputed** (`signal-del-bg` bg,
`signal-del` label). Label in `eyebrow`, radius `radius-pill`. A leading dot in
the label color is optional, and a finished status can have a leading check
mark (✓) in the label color in place of the dot. Pills are tinted, never a solid fill (a solid pill
reads as a button). One active or affirmative status per set may use the accent
tint, never solid: Verified among verdicts, In progress among task statuses.
The other statuses in a set are neutral (`surface-strong` + `ink`, or
`surface-sunken` + `ink-muted`), with no other hues. A set that needs three
neutral steps can use `surface-sunken` with `ink` as the middle step. Pills are for status only: verdicts, tiers, and
the status of posts, tasks and meetings. A source tier or a "supported" verdict
is never green; green is for additions and success.

### Warning (violet)
A warning uses `status-warning` (violet): `status-warning` text/icon, often on a
`status-warning-bg` ground, with a ⚠ glyph for redundancy. Use it everywhere the
app currently reaches for amber. Distinct from error (`signal-del`) and from the
accent. On a solid violet fill use white text in light mode, near-black in dark.

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
