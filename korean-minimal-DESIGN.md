# 韩式极简 (Korean Minimal) — Design Specification

> Category: minimal | Tags: minimal, modern

## Design Philosophy

Korean Minimal（韩式极简）源自韩国当代设计美学中对"留白"与"克制"的深度追求，融合了K-beauty的柔和质感和韩国现代建筑的简洁线条。

核心理念：
- 留白即美：大面积的空白不是空虚，而是一种呼吸感。韩式极简将留白视为最重要的设计元素，让内容在宁静中自然浮现
- 粉彩温度：不同于北欧极简的冷灰色调，韩式极简选择带有微暖底色的粉彩——腮红粉、鼠尾草绿、沙色——赋予界面柔和而不冰冷的个性
- 克制装饰：装饰性元素被压缩到极致，一条细线、一个微妙的圆角、一抹淡淡的阴影就是全部。多一分则过，少一分则失
- 精致触感：受K-beauty产品设计影响，每一个交互都追求丝滑、精致和高品质感

韩式极简在全球设计界的影响力日益增长，特别是在美妆、生活方式和高端消费品领域。它证明了极简主义不必是冰冷的——它可以温暖、柔和，同时保持优雅的克制。

## Color System

| Role | Hex | Swatch | CSS Variable |
|------|-----|--------|-------------|
| Primary | `#3d4a5c` | ██ | `--color-primary` |
| Secondary | `#faf9f7` | ██ | `--color-secondary` |
| Accent 1 | `#d4a5a5` | ██ | `--color-accent-1` |
| Accent 2 | `#a8c5b8` | ██ | `--color-accent-2` |
| Accent 3 | `#e8d4b8` | ██ | `--color-accent-3` |

## Typography

Inferred from minimal aesthetic — lightweight, wide tracking, serene rhythm.

| Level | Size | Weight | Line Height | Letter Spacing |
|-------|------|--------|-------------|----------------|
| h1 | 4xl / 5xl (md) | font-light | leading-tight | tracking-wide |
| h2 | 2xl / 3xl (md) | font-light | leading-relaxed | tracking-wide |
| h3 | xl | font-normal | leading-relaxed | tracking-wide |
| Body | base | font-light | leading-relaxed | tracking-wide |
| Caption | sm | font-light | leading-relaxed | tracking-normal |

## Component Specifications

### Button

Extracted from `components.button`:
- **Padding**: px-10 py-3.5 (horizontal 40px, vertical 14px)
- **Border**: border border-[#3d4a5c]/10
- **Border Radius**: rounded-2xl (16px)
- **Background**: bg-[#faf9f7] (Warm White)
- **Text**: text-[#3d4a5c], font-light, tracking-wide
- **Shadow**: shadow-[0_4px_15px_rgba(232,212,184,0.18)]
- **Hover**: hover:-translate-y-0.5, hover:text-[#2f3946], hover:shadow-[0_16px_36px_rgba(168,197,184,0.18)]
- **Active**: active:bg-[#f3f0ea]
- **Transition**: transition-all duration-700 ease-in-out

### Card

Extracted from `components.card`:
- **Background**: bg-[#faf9f7]
- **Border**: border border-[#3d4a5c]/10
- **Border Radius**: rounded-2xl
- **Padding**: p-10
- **Shadow**: shadow-[0_8px_24px_rgba(232,212,184,0.14)]
- **Hover**: hover:-translate-y-0.5, hover:shadow-[0_24px_50px_rgba(212,165,165,0.16)]
- **Transition**: transition-all duration-1000 ease-in-out
- **Decoration**: w-8 h-px bg-[#d4a5a5]/80 divider line at top

### Input

Extracted from `components.input`:
- **Background**: bg-[#faf9f7]
- **Border**: border border-[#3d4a5c]/10
- **Border Radius**: rounded-2xl
- **Text**: text-[#3d4a5c], font-light, tracking-wide
- **Placeholder**: placeholder-[#3d4a5c]/25
- **Focus**: focus:border-[#d4a5a5]/50, focus:shadow-[0_0_0_3px_rgba(212,165,165,0.1)], focus:outline-none
- **Transition**: transition-all duration-300

### Navigation

Not provided in style data (empty). Derived from aiRules:
- **Background**: bg-[#faf9f7] or transparent
- **Border**: thin bottom border border-b border-[#3d4a5c]/8
- **Layout**: flex, items-center, px-8 py-4
- **Brand**: font-light tracking-wide text-[#3d4a5c]

## Do ✅

- [x] Use generous whitespace p-8 md:p-12 lg:p-16
- [x] Use warm white bg-[#faf9f7] as main background
- [x] Use slate blue text-[#3d4a5c] as main text color
- [x] Use pastel accents as subtle highlights text-[#d4a5a5], bg-[#a8c5b8]/10
- [x] Use delicate large rounded corners rounded-2xl or rounded-3xl
- [x] Use ultra-thin borders border border-[#3d4a5c]/10
- [x] Use soft shadows shadow-sm or custom light shadows
- [x] Use light, clean fonts font-light or font-normal, tracking-wide

## Don't ❌

- [ ] No high-saturation pure colors (bg-red-500, bg-blue-600)
- [ ] No thick borders (border-2, border-4)
- [ ] No heavy shadows (shadow-xl, shadow-2xl)
- [ ] No uppercase or tracking-widest
- [ ] No dark/black backgrounds (bg-black, bg-[#0a0a0a])
- [ ] No excessive decorations or element stacking
- [ ] No neon or fluorescent colors

## AI Rules

```
You are a Korean Minimal design style frontend development expert. All generated code must strictly follow these constraints:

## Absolutely Forbidden

- High saturation pure colors (bg-red-500, bg-blue-600, bg-green-500)
- Thick borders (border-2, border-4)
- Heavy shadows (shadow-xl, shadow-2xl)
- Uppercase text and ultra-wide tracking (uppercase tracking-widest)
- Dark/black backgrounds (bg-black, bg-[#0a0a0a])
- Neon or fluorescent colors
- Excessive decorations or visual clutter

## Must Follow

- Warm white background bg-[#faf9f7]
- Slate blue text text-[#3d4a5c]
- Generous whitespace and padding (p-8, p-10, p-12)
- Delicate rounded corners rounded-2xl
- Ultra-thin borders border border-[#3d4a5c]/8 or /10
- Soft subtle shadows shadow-sm
- Light font weights font-light or font-normal
- Wide but gentle tracking tracking-wide

## Color Palette

Primary:
- Slate Blue: #3d4a5c
- Warm White: #faf9f7
- Blush Pink: #d4a5a5
- Sage Green: #a8c5b8
- Sand: #e8d4b8

## Design Principles

- Whitespace is the primary design element
- Less is always more
- Subtle is always better than obvious
- Every element must have room to breathe
- Decorations should be minimal (thin lines, small dots)

## Animation & Interaction Rules

- Lazy Breathing: transitions should use duration-700+ and ease-in-out, staying languid and unhurried.
- Micro Lift: hover displacement stays at -translate-y-0.5, expressed through ultra-light warm shadow diffusion.
- Muted Whisper: text and borders only do same-color-family slight transitions, avoiding high-contrast jumps that break the quiet atmosphere.
- Soft Press: active feedback prefers slight background deepening, no obvious scaling or bouncing.
```

## Keywords

韩式, 极简, K-beauty, 留白, 粉彩, 克制, 精致
