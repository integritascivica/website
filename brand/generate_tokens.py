#!/usr/bin/env python3
"""
Generate tokens.css (CSS custom properties, light + dark) from the
Integritas Civica design system's tokens.json.

Usage:
    python generate_tokens.py tokens.json > tokens.css

Run with -I for isolation if tokens.json came from an untrusted path:
    python3 -I generate_tokens.py tokens.json > tokens.css

Single source of truth: commit this script + tokens.json, regenerate into
BOTH the Next app and the Eleventy site whenever a token changes.
"""
import json
import sys


def esc(name: str) -> str:
    # tokens.json allows "." in names (e.g. space-1.5); CSS needs it escaped
    return name.replace(".", "\\.")


def color_blocks(color: dict) -> str:
    themes = color.get("themes", [{"id": "light"}])
    first = themes[0]["id"]
    tokens = color.get("tokens", [])

    def val_for(tok, theme_id):
        v = tok["value"]
        if isinstance(v, str):
            return v if theme_id == first else None
        return v.get(theme_id)

    out = []
    # First theme lives on :root (and the explicit light selector)
    lines = []
    for t in tokens:
        v = val_for(t, first)
        if v is not None:
            lines.append(f"  --{esc(t['name'])}: {v};")
    out.append(':root,\n:root[data-theme="light"] {\n' + "\n".join(lines) + "\n  color-scheme: light;\n}")

    # Remaining themes: emit under both prefers-color-scheme and [data-theme]
    for th in themes[1:]:
        tid = th["id"]
        lines = []
        for t in tokens:
            v = val_for(t, tid)
            if v is not None:
                lines.append(f"  --{esc(t['name'])}: {v};")
        body = "\n".join(lines)
        scheme = "dark" if tid == "dark" else "light"
        # system preference, guarded so an explicit opposite choice still wins
        out.append(
            f"@media (prefers-color-scheme: {scheme}) {{\n"
            f'  :root:not([data-theme="light"]) {{\n'
            + "\n".join("  " + l for l in lines)
            + f"\n    color-scheme: {scheme};\n  }}\n}}"
        )
        # explicit toggle
        out.append(f'[data-theme="{tid}"] {{\n{body}\n  color-scheme: {scheme};\n}}')
    return "\n\n".join(out)


def scalar_block(selector_tokens: list) -> str:
    lines = []
    for fam in selector_tokens:
        for t in fam.get("tokens", []):
            lines.append(f"  --{esc(t['name'])}: {t['value']};")
    return ":root {\n" + "\n".join(lines) + "\n}"


def type_block(type_obj: dict) -> str:
    out = []
    fams = type_obj.get("families", {})
    lines = [f"  --font-{k}: {v};" for k, v in fams.items()]
    out.append(":root {\n" + "\n".join(lines) + "\n}")
    # one class per type style
    for group in type_obj.get("groups", []):
        gfam = group.get("family")
        for s in group.get("styles", []):
            decls = [f"  font-family: var(--font-{s.get('family', gfam)});"]
            if "fontSize" in s: decls.append(f"  font-size: {s['fontSize']};")
            if "lineHeight" in s: decls.append(f"  line-height: {s['lineHeight']};")
            if "fontWeight" in s: decls.append(f"  font-weight: {s['fontWeight']};")
            if "letterSpacing" in s: decls.append(f"  letter-spacing: {s['letterSpacing']};")
            if "fontStyle" in s: decls.append(f"  font-style: {s['fontStyle']};")
            out.append(f".{esc(s['name'])} {{\n" + "\n".join(decls) + "\n}")
    return "\n\n".join(out)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "tokens.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    parts = [f"/* {data.get('name', 'Design system')} — generated from tokens.json. Do not edit by hand. */"]
    if "color" in data:
        parts.append(color_blocks(data["color"]))
    scalars = [data[k] for k in ("spacing", "radius") if k in data]
    if scalars:
        parts.append(scalar_block(scalars))
    if "shadow" in data:
        # shadow may be per-theme; emit light values on :root, dark under the guards
        sh = data["shadow"]["tokens"]
        first = data.get("color", {}).get("themes", [{"id": "light"}])[0]["id"]
        def sv(t, theme):
            v = t["value"]
            return v if isinstance(v, str) else v.get(theme)
        parts.append(":root {\n" + "\n".join(
            f"  --{esc(t['name'])}: {sv(t, first)};" for t in sh if sv(t, first)) + "\n}")
        themes = data.get("color", {}).get("themes", [])
        for th in themes[1:]:
            tid = th["id"]; scheme = "dark" if tid == "dark" else "light"
            body = "\n".join(f"  --{esc(t['name'])}: {sv(t, tid)};" for t in sh if sv(t, tid))
            parts.append(f'@media (prefers-color-scheme: {scheme}) {{\n  :root:not([data-theme="light"]) {{\n'
                         + "\n".join("  " + l for l in body.splitlines()) + f"\n  }}\n}}")
            parts.append(f'[data-theme="{tid}"] {{\n{body}\n}}')
    if "type" in data:
        parts.append(type_block(data["type"]))

    sys.stdout.write("\n\n".join(parts) + "\n")


if __name__ == "__main__":
    main()
