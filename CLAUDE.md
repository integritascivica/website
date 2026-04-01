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
