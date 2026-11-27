# Integritas Civica — design-system retrofit plan

Two existing static codebases, both plain CSS, both with some dark-mode
support already. This is a **normalization** retrofit: converge both onto one
token layer generated from the design system's `tokens.json`. Do it in
phases, one repo at a time, reviewing between phases. Each phase is a
separate Claude Code session prompt.

## Shared setup (once)

1. Commit `generate_tokens.py`, `tokens.json`, and `DESIGN_SYSTEM.md` into a
   `brand/` folder in each repo (same versions in both). `brand/` sits at the
   repo root, outside the Eleventy input dir and outside the Next app source
   and `public/`, so it never deploys.
2. Add the design-system block to each repo's `CLAUDE.md` (see
   `CLAUDE.md-snippet.md`).
3. Self-host the fonts (Lora, Inter, JetBrains Mono — all OFL 1.1). Put
   `woff2` files in each repo and `@font-face` them, or use `next/font/local`
   in the app. Don't rely on a font CDN.

## Phase 0 — Audit (read-only, do first, both repos)

Prompt Claude Code: *"Read `brand/DESIGN_SYSTEM.md` and `brand/tokens.json` in
this repo. Then audit this repo's CSS: list every hardcoded color,
font-family, border-radius, and spacing value, where each appears, and how the
current dark mode is implemented (data-theme, a class, or
prefers-color-scheme). Produce a mapping from each existing value to the
closest design-system token, and flag anything with no clean match."*

The audit tells you the real size of the job and surfaces drift (e.g. the
old accent appearing as several near-identical hexes). Review it before
changing anything.

### What the app audit found (and how v2 tokens answer it)

The app is Next 16 with ~129 Tailwind-heavy component files. Decisions already
made and baked into `tokens.json` v2:

- **Old accent is purple** (`#7c3aed`, 218 uses) + a runtime accent picker
  (`tailwind-palette.ts`). DECISION: picker STAYS as an override; gold is the
  default. The picker must also set `--accent-ink` per chosen color (and ideally
  `--accent-text`), or a pale override fails contrast. Reframe the palette list
  as override options with gold first.
- **Amber === the accent** (`amber-700` = `#b45309`, `amber-300` = `#fcd34d`,
  132 uses as warning). DECISION: warning is a VIOLET color token
  (`status-warning` / `status-warning-bg`), moved out of the warm band since gold
  and red occupy it. Each amber use that means "warning/caution" becomes
  `status-warning` (+ ⚠ glyph); any decorative amber becomes a `cat-*` color — a
  per-use pass, not a blind swap.
- **Red/green do double duty** (diff add/remove AND error/success, 279+98 uses).
  v2 broadens `signal-add`/`signal-del` to cover both meanings — no new tokens.
- **No categorical palette** (speaker chips, reference highlights, calendar
  dots, chart series). v2 adds `cat-1`…`cat-6`.
- **Spacing is rem at 110% root; tokens were px.** v2 converts spacing+radius to
  rem and expands the scale. `radius-xs` (4px) matches the current `rounded` so
  766 elements don't get rounder.
- **Shadows**: v2 adds `shadow-menu`, `shadow-overlay`, and `backdrop` for the
  14 menus/dialogs and scrims.
- **Dark mode is `prefers-color-scheme` only** — no `data-theme` path, no
  toggle. The design system needs the explicit path; adding it is Phase 1.
- **Tasks widget** (`todo.py`) sends a standalone page that can't see
  `tokens.css` or the fonts — a FastAPI-side fix (side stream).
- **`opacity-60/70` for muted text** (786 uses) is NOT `ink-muted` — opacity
  dims borders/icons too. Its own phase; expect to leave many as-is.

## Phase 1 — Token layer + dark-mode reconciliation

Generate `tokens.css` from `tokens.json` (`python brand/generate_tokens.py
brand/tokens.json > <css path>`) and import it first. Then reconcile dark mode:
the app is `prefers-color-scheme`-only today, so add the explicit path — a
`@custom-variant dark` rule in `globals.css`, `[data-theme]` selectors at the
media queries, and a toggle. After this, all three theme states work (`:root`
light; `prefers-color-scheme: dark` guarded by `:root:not([data-theme="light"])`;
explicit `[data-theme="dark"]`). **After regenerating, visually check a couple
of dense screens** — the px→rem spacing conversion shifts computed sizes
slightly.

## Phase 2 — Color, mechanical rows (safe to automate)

Replace the clean mappings broadly: `--foreground`→`--ink`, `--border`→`--rule`
(727 uses), `--muted`→`--surface-sunken`, `--accent-foreground`→`--accent-ink`,
the viz vars, zinc/gray→`--ink-muted`/`--surface-sunken`. Verify both themes.

## Phase 3 — Color, judgment rows (per-use, reviewed)

- **Red/green**: uses meaning error/removed → `--signal-del`; success/added →
  `--signal-add`. The few decorative reds/greens → a `cat-*` or neutral.
- **Amber → violet warning**: each `amber-*` meaning warning/caution becomes
  `status-warning` (+ ⚠ glyph), or a `cat-*` if it was decorative. Per-use.
- **Ad-hoc hues** (blue/sky info, emerald/fuchsia/rose/etc.) → `cat-*`, or
  neutral for info until an info token exists.

## Phase 4 — Type (judgment, not bulk replace)

Content/interface/data split. Reading text → Lora (`--font-serif`), interface →
Inter (`--font-sans`), data/IDs/counts → JetBrains Mono (`--font-mono`). The app
has NO serif today and 34 prose blocks + post/chat text in the sans — each needs
a content-vs-interface decision. Don't blanket-swap.

## Phase 5 — Radius, spacing, shadow (mechanical)

Replace literal radii/spacing/shadow with tokens. `rounded`→`--radius-xs`,
Tailwind spacing steps → `--space-*`, `shadow-lg`/`shadow-xl` →
`--shadow-menu`/`--shadow-overlay`, dialog scrims → `--backdrop`.

## Phase 6 — `opacity` for muted text (its own phase)

786 `opacity-60/70` uses. Replace with `--ink-muted` ONLY where the dimmed
element is text; leave uses where borders/icons should dim with it. Per-use
review; many may stay as-is.

## Phase 7 — Component pass

Bring components into line with `DESIGN_SYSTEM.md`: status pills, nav selection
(accent underline), diff lines, source cards, the violet warning.

**Buttons, tags and pills (shape language).** Solid = button, underlined text =
quiet button, outline = tag, pill = status.
- Buttons: primary (`--accent` fill), secondary (`--surface-strong` fill, `--ink`
  text), destructive (`--signal-del` fill, `--surface-page` text). Remove the
  ghost (accent-outline) style.
- Existing neutral-outline buttons: sort per use. An action that matters becomes
  secondary (solid); a minor or dismissive one becomes quiet (underlined text).
  None stay outlined.
- Delete, discard and remove actions become red underlined text (`--signal-del`).
  A solid red button appears only as the confirming action in a confirmation
  dialog.
- Status pills are tinted, never a solid accent or solid color fill.
- Anything that is a button but looks like a tag becomes solid; anything that is
  a category, topic or label but looks like a button becomes an outlined tag.
- Toggles: outlined when off, solid `--accent` when on; no weight change.
- Status chips (post, task, meeting, vault status) become pills like verdict and
  tier chips; label and filter chips stay rectangular outlined tags.
- Radius: every rectangular control, card and dialog uses `--radius-xs`;
  `--radius-sm`, `--radius-md` and `--radius-lg` no longer exist.

**Wordmark lockup (both repos).** Apply the wordmark wherever the org name shows
next to the logo, in the app AND the website. The lockup itself is the same in
both: "Integritas" and "Civica" in Lora (weight 600, `--ink`) with the
interpunct `·` in `--accent`, ~0.2em space each side, at the font's natural glyph
height — no `inline-flex`+`align-items:center`, no `position/top` offset (see the
Wordmark guidance; the earlier bug was a stray vertical offset). The dot uses
`--accent`, so it flexes caramel/gold by theme automatically.

- **App:** the name is visible only when the nav sidebar is EXPANDED → logo +
  full wordmark. When COLLAPSED → logo mark only; the wordtext and dot hide with
  the rest of the expanded content.
- **Website:** apply the lockup wherever the masthead/header (and footer, if it
  carries the name) shows it.
- Verify the lockup renders correctly in BOTH repos, in BOTH themes, and — in the
  app — in both sidebar states, with the dot at its natural height each time.

## Side streams (independent of the CSS phases)

- **Tasks widget**: make `todo.py`'s standalone page load `tokens.css` and the
  fonts (inline them, or serve them to that page).
- **CLAUDE.md / scripts mismatch**: root CLAUDE.md says build+dev run the
  `tokens` step but the scripts don't (only `make ci` guards it). Add a `tokens`
  script and have `build` and `serve`/`debug` depend on it, so dev never runs
  against a missing or stale `tokens.css`.

## Phase 8 — Verify

- Both themes legible, accent working on both backgrounds, toggle works.
- No white text on pale-gold fills (use `--accent-ink`); picker overrides set
  their own `--accent-ink`.
- Small gold text uses `--accent-text`, not `--accent`.
- Red/green appear only as diff or error/success.
- No amber-as-warning left; warnings use the violet `status-warning` token.
- Chips/series use `cat-*`, not semantic colors.
- No outlined buttons; no solid or pill-shaped tags; quiet buttons are underlined.
- No reference to `--radius-sm`, `--radius-md` or `--radius-lg` remains.
- Spacing scales with root font size (rem, not px).
- Wordmark lockup correct next to the logo in BOTH repos: website masthead, and
  the app sidebar (full wordmark + accent dot when expanded, logo only when
  collapsed); dot at natural height, both themes.
- Website and app visually consistent (same tokens, same fonts).

## Keeping in sync afterward

Change tokens in the design system → update `brand/tokens.json` in both repos →
rebuild (the `tokens` step regenerates `tokens.css`) → commit. Never hand-edit
`tokens.css`. If the brand book changes, re-copy `DESIGN_SYSTEM.md` the same
way. `brand/tokens.json` and `brand/DESIGN_SYSTEM.md` are authoritative for the
build; the Claude design-system artifact is where you edit them upstream.
