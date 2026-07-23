# Component Showcase Page — Specification

## Page Metadata

- **Container**: 750px × 1000px fixed container (3:4 ratio), centered on page
- **Background**: White or near-white (#f8fafc / #ffffff), NOT the style's dark background
- **Purpose**: Reference card for designers/developers showing all UI components in one view

## Layout Structure

```
┌──────────────────────────────────────┐
│  HEADER: Style Name + Category Tag   │
├──────────────────────────────────────┤
│  SECTION 1: Buttons (4 variants)     │
│  [Primary] [Secondary] [Outline] [Ghost] │
├──────────────────────────────────────┤
│  SECTION 2: Form Elements            │
│  [Input Search]     [Toggle ON/OFF]  │
├──────────────────────────────────────┤
│  SECTION 3: Content Components       │
│  [Content Card]    [Badge x N]       │
├──────────────────────────────────────┤
│  SECTION 4: Progress                 │
│  [Circle Progress] [Bar Progress]    │
├──────────────────────────────────────┤
│  SECTION 5: Navigation               │
│  [Tabs]                              │
│  [Navigation Bar]                    │
├──────────────────────────────────────┤
│  SECTION 6: Color Palette (5 shades) │
│  [██] [██] [██] [██] [██]           │
├──────────────────────────────────────┤
│  SECTION 7: Accordion                │
│  [▶ Section 1]                       │
│  [▼ Section 2 (expanded)]            │
│  [▶ Section 3]                       │
└──────────────────────────────────────┘
```

## Component Requirements

### 1. Button Primary
- Full style from `components.button` primary variant
- Show default, hover (CSS :hover), and active (:active) states
- Label: "Primary Action"

### 2. Button Secondary  
- Lower visual weight than primary
- Different bg/border treatment
- Derive from aiRules: secondary = lighter bg, subtler border

### 3. Button Outline
- Transparent bg, visible border in primary color
- Hover fills background slightly

### 4. Button Ghost
- No border, no bg
- Hover shows subtle background
- Label should be styled same as primary text color

### 5. Input Search
- Search icon (SVG magnifying glass) on left side
- Placeholder text
- Focus ring/glow per style rules
- Clear button on right (optional)

### 6. Toggle (On/Off)
- Track + Thumb design
- On state: primary color fill
- Off state: secondary/muted fill
- Smooth slide transition (duration-200)
- Label: "Toggle"

### 7. Content Card
- From `components.card` template
- Title + description text
- Corner decoration if style supports it
- Shadow/glow hover effect per style

### 8. Progress Circle
- SVG-based circular progress
- Value: 72% (hardcoded)
- Primary color stroke, secondary color track
- Animated on page load (optional)

### 9. Progress Bar
- Horizontal bar, full width
- Value: 65% (hardcoded)
- Primary color fill
- Shine/sweep animation if style supports it

### 10. Tabs
- 3-4 tab items: "Overview", "Analytics", "Settings", "Logs"
- Active tab: primary color indicator
- Inactive tabs: muted color
- Bottom border or pill background for active state

### 11. Badge
- 3-4 variants: Default, Success, Warning, Danger
- Small pill/tag shape
- Colors derived from style's accent/status colors

### 12. Navigation Bar
- From `components.nav` template
- Brand logo + nav links (simplified for showcase)
- Status indicator if style uses one

### 13. Color Palette
- 5 swatches in a row
- Colors: Primary, Secondary, Accent 1, Accent 2, Accent 3
- Each swatch shows hex code below
- Rounded or square per style convention

### 14. Accordion
- 3 collapsible sections
- First item expanded by default
- Chevron icon rotates on expand/collapse
- Section titles descriptive (e.g., "Getting Started", "Configuration", "API Reference")
- Content area with placeholder text
- Smooth height transition

## Technical Implementation

- Tailwind CSS CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Custom styles in `<style>` block for animations, SVG progress, etc.
- No external JS frameworks — vanilla JS only if needed for toggle/accordion interactivity
- All components MUST strictly follow the style's aiRules, doList, and dontList
- Components not defined in StyleKit data (Toggle, Progress, Tabs, Badge, Accordion) should be inferred from aiRules parameters

## AI Slop Prevention
- NO purple-blue gradients unless explicitly in style's colors
- NO emoji as icons — use SVG or CSS shapes
- NO excessive glow/blur unless the style calls for it
- NO random decorative elements
- NO "✨" "🚀" "💡" emoji anywhere

## Accessibility
- All interactive elements: focus-visible ring
- Toggle: role="switch" + aria-checked
- Tabs: role="tablist" / role="tab" / role="tabpanel"
- Accordion: aria-expanded + button elements
- Progress: aria-valuenow + role="progressbar"
- prefers-reduced-motion: disable all animations
