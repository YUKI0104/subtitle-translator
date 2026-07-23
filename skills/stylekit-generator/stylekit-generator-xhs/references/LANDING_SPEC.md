# Landing Page — Specification

## Page Structure (6 Sections, Top to Bottom)

### 1. Navigation Bar
- **Height**: 56-72px
- **Layout**: Brand logo (left) + Nav links (center/right) + CTA button (right)
- **Background**: Per style convention (transparent on hero, solid on scroll)
- **State indicator**: If style uses system status (HUD, dashboard styles), include it
- **Mobile**: Hamburger menu or simplified nav
- **Source**: Use `components.nav` if available, otherwise derive from aiRules

### 2. Hero Section
- **Min Height**: 80vh or 600px
- **Content**:
  - H1 headline (6-10 words, compelling)
  - H2 subheadline (12-20 words, descriptive)
  - Primary CTA button + Secondary CTA text link
  - Visual element: abstract geometry, illustration hint, or terminal text if sci-fi
- **Background treatment**: Follow style convention (gradient, pattern, dark, image placeholder)
- **Animation**: Subtle entrance animation on headline

### 3. Features Grid
- **3-6 feature cards** in 2x2 or 3x2 grid
- Each card: icon/shape + title + 2-line description
- **Icon style**: SVG geometric shapes matching style aesthetic (no emoji)
- **Card styling**: From `components.card` template
- **Hover effect**: Per style rules (glow, translate, border change, etc.)

### 4. Stats / Social Proof
- **3-4 metrics** in a row
- Large number + label below
- Optional: client logos row (placeholder grey boxes)
- Animation: count-up or fade-in on scroll (optional)

### 5. CTA Section
- **Background**: Contrasted from main background (slightly lighter/darker)
- **Content**: H2 headline + paragraph + primary CTA button
- **Urgency**: Gentle nudge, not aggressive
- **Layout**: Centered, max-width container

### 6. Footer
- **Layout**: 4-column grid of links + copyright at bottom
- **Columns**: Product, Company, Resources, Legal
- **Copyright**: "© 2026 {Brand Name}. All rights reserved."
- **Background**: Darker than main bg (or per style convention)

## Design Constraints

1. **Follow aiRules strictly**: Every MUST USE and MUST AVOID must be honored
2. **Follow doList/dontList**: Every item in doList should be visible; every dontList item must be absent
3. **Colors**: Use EXACTLY the hex values from `colors` object. Do not invent new colors.
4. **Typography**: Use font classes consistent with the style. Apply uppercase/tracking/mono per rules.
5. **Shadows & Glows**: Use exact shadow values from components or aiRules. Do not use generic shadow-md etc.
6. **Border radius**: Match the style's convention exactly. If aiRules says rounded-sm, use rounded-sm everywhere.
7. **Animations**: duration-100 to duration-300 unless aiRules specifies otherwise. All wrapped in motion-reduce:transition-none.

## Technical Implementation

- **Tailwind CSS CDN**: Standard `<script src="...">` approach
- **No JavaScript framework**: Vanilla JS only for scroll effects, mobile menu toggle
- **Responsive**: Mobile-first. Breakpoints at sm (640px), md (768px), lg (1024px)
- **Semantic HTML**: `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`
- **Accessibility**: 
  - All images: alt text or aria-hidden for decorative
  - All interactive: focus-visible styles
  - Skip-to-content link (optional but preferred)
  - prefers-reduced-motion media query

## Content Guidelines

- **Headlines**: Write actual compelling copy, not lorem ipsum. Make it product-neutral but evocative of the style.
- **Feature descriptions**: 1-2 sentences each, concrete not generic.
- **CTA text**: Action-oriented: "Get Started", "Explore Now", "Request Access", "Launch Dashboard", etc.
- **Stats numbers**: Use plausible numbers (not "1,000,000+" for everything)
- **Footer links**: Standard SaaS footer structure

## AI Slop Prevention
- NO purple-blue gradients unless in style's color palette
- NO emoji anywhere in the page
- NO "revolutionize", "unleash", "game-changer" buzzwords
- NO stock-photo-style descriptions
- NO random floating particles or unnecessary decorative elements
