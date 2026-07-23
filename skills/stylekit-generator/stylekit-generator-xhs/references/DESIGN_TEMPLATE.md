# DESIGN.md Template

When generating DESIGN.md, follow this exact structure. Replace `{placeholder}` values with data from the `fetch_style.py` output.

---

# {name} ({nameEn}) — Design Specification

> Category: {category} | Tags: {tags}

## Design Philosophy

{philosophy — keep the original text, do not rephrase}

## Color System

| Role | Hex | Swatch | CSS Variable |
|------|-----|--------|-------------|
| Primary | `{colors.primary}` | ██ | `--color-primary` |
| Secondary | `{colors.secondary}` | ██ | `--color-secondary` |
| Accent 1 | `{colors.accent[0]}` | ██ | `--color-accent-1` |
| Accent 2 | `{colors.accent[1]}` | ██ | `--color-accent-2` |
| Accent 3 | `{colors.accent[2]}` | ██ | `--color-accent-3` |

## Typography

Infer from tags, keywords, and aiRules. Common patterns:

- **Headings**: font-bold / font-black, tracking-tight or tracking-wider depending on style
- **Body**: font-sans or font-mono, leading-relaxed
- **Labels**: uppercase, tracking-wider, text-xs or text-sm
- **Mono use cases**: sci-fi, tech, terminal, HUD, cyberpunk styles → font-mono
- **Serif use cases**: editorial, luxury, magazine, classical styles → font-serif

| Level | Size | Weight | Line Height | Letter Spacing |
|-------|------|--------|-------------|----------------|
| h1 | {inferred} | {inferred} | {inferred} | {inferred} |
| h2 | {inferred} | {inferred} | {inferred} | {inferred} |
| h3 | {inferred} | {inferred} | {inferred} | {inferred} |
| Body | {inferred} | {inferred} | {inferred} | {inferred} |
| Caption | {inferred} | {inferred} | {inferred} | {inferred} |

## Component Specifications

### Button

Extract from `components.button`:
- **Padding**: {extract px/py values}
- **Border**: {extract border classes}
- **Border Radius**: {extract rounded value}
- **Background**: {extract bg classes}
- **Text**: {extract text color/size/font/transform classes}
- **Hover**: {extract hover classes}
- **Active**: {extract active classes}
- **Transition**: {extract transition classes}

### Card

Extract from `components.card`:
- **Background & Backdrop**: {extract bg/backdrop classes}
- **Border & Glow**: {extract border + shadow classes}
- **Padding**: {extract p value}
- **Hover**: {extract hover classes}
- **Decorations**: {corner accents, scanlines, etc.}

### Input

Extract from `components.input`:
- **Background**: {extract bg}
- **Border**: {extract border classes}
- **Border Radius**: {extract rounded}
- **Focus**: {extract focus classes}
- **Placeholder**: {extract placeholder color}
- **Text**: {extract text classes}

### Navigation

Extract from `components.nav`:
- **Background & Backdrop**: {extract}
- **Border**: {extract bottom border}
- **Height/Padding**: {extract}
- **Brand**: {extract logo/title styling}

## Do ✅

{Convert doList to markdown checklist, one per line}

## Don't ❌

{Convert dontList to markdown checklist, one per line}

## AI Rules

```
{aiRules — keep the original text verbatim}
```

## Keywords

{keywords as comma-separated list}
