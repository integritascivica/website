# Integritas Civica Website

Eleventy 3.0 static site deployed on Netlify.

## Commands

- `npm run serve` — Local dev server with hot reload (http://localhost:8080)
- `npm run build` — Production build to `_site/`
- `npm run debug` — Build with Eleventy debug logging (`DEBUG=Eleventy*`)

## Architecture

### Eleventy Config (`eleventy.config.js`)

- Input: `src/` → Output: `_site/`
- Template formats: Markdown, Nunjucks, HTML
- Markdown and HTML both use Nunjucks as their template engine
- `src/css/` is passthrough-copied (not processed)

### Source Layout (`src/`)

```
src/
├── _data/site.json      # Global data: site name, tagline, description, social links, nav items
├── _includes/base.njk   # Single base layout (HTML shell, header, nav, footer, JSON-LD)
├── css/style.css         # All styles — single file, CSS custom properties
├── index.md              # Homepage
├── about/index.md        # Content pages follow /section/index.md pattern
├── programs/index.md
├── connect/index.md
├── resources/index.md
└── privacy/index.md
```

### Data Flow

- `src/_data/site.json` → available as `site` in all templates
- Page front matter provides `layout`, `title`, `description`
- `base.njk` reads `site.name`, `site.nav`, `site.social`, `page.url`
- Navigation uses `aria-current="page"` for active state

### Template Pattern

Every content page uses this front matter:

```yaml
---
layout: base.njk
title: Page Title
description: "Page description text."
---
```

Markdown content can include inline HTML (cards, CTAs, hero sections).

## Styling

Single CSS file (`src/css/style.css`) using custom properties defined on `:root`:

- Colors: `--color-text`, `--color-bg`, `--color-surface`, `--color-accent`, `--color-accent-dark`, `--color-border`, `--color-text-light`
- Spacing: `--space-xs` through `--space-xl`
- Layout: `--max-width: 48rem`
- Component classes: `.hero`, `.card-grid`, `.card`, `.btn`, `.btn-primary`, `.btn-secondary`, `.social-links`, `.cta-group`
- Mobile breakpoint at 640px

## Deployment

Netlify (`netlify.toml`): runs `npm install && npm run build`, publishes `_site/`, Node 20.

## Open Brain (Semantic Knowledge)
- Use open-brain-ic (not open-brain-personal) for all Open Brain operations in this project.

## Design system (add this block to each repo's CLAUDE.md)

The Integritas Civica design system is the single source of truth for all
visual styling. It lives as a published artifact; read it before changing
any UI.

- Brand book: `project/README.md` in the design system — read first.
- Tokens: `project/tokens.json` — colors (light/dark), type, spacing, radius.
- Components: `project/components/<Name>/README.md` + `preview.html`.

### Rules

- Never hardcode a color, font-family, border-radius, or spacing value.
  Reference the generated CSS custom properties (`var(--accent)`,
  `var(--ink)`, `var(--space-4)`, `var(--radius-sm)`, `var(--font-serif)`…).
- The accent is one color with two theme values: burnt caramel `#b45309`
  (light) / bright gold `#fcd34d` (dark). Use `--accent` for fills,
  `--accent-ink` for text ON a fill (white on caramel, near-black on gold —
  never reversed), and `--accent-text` for small accent-colored text on a
  surface (deeper in light mode so it stays legible on white).
- Red and green are RESERVED for diff/revision semantics only
  (`--signal-add`, `--signal-del`). Never use them as accent or decoration.
- Content vs. interface font split: text people READ in sentences is Lora
  (`--font-serif`); interface people SCAN or operate is Inter
  (`--font-sans`); data/diffs/IDs/counts are JetBrains Mono
  (`--font-mono`).
- Theme switching: `:root` is light; dark comes from
  `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])` and
  from an explicit `[data-theme="dark"]`. Keep all three in sync.

### Regenerating tokens

`tokens.css` is GENERATED from `tokens.json` by `generate_tokens.py` — do
not edit `tokens.css` by hand. When a token changes in the design system,
re-run the generator and commit the output. The same `tokens.json` feeds
both the Next app and the Eleventy site; keep them on the same version.
