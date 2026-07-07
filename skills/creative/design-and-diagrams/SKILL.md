---
name: design-and-diagrams
description: Visual design and diagramming — architecture diagrams (SVG/HTML), hand-drawn diagrams (Excalidraw), design token specs (DESIGN.md), brand design systems, and one-off HTML artifacts.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [design, diagrams, SVG, HTML, Excalidraw, DESIGN.md, design-systems, tokens, UI, UX, prototype, architecture, visualization]
    related_skills: []
---

# Design & Diagrams — Unified Guide

This umbrella skill consolidates all visual design and diagramming capabilities. Each tool serves a different purpose:

- **architecture-diagram**: Dark-themed SVG diagrams for software/cloud infrastructure
- **excalidraw**: Hand-drawn style diagrams (.excalidraw files)
- **design-md**: Google's DESIGN.md token spec files
- **popular-web-designs**: 54 brand design system templates
- **claude-design**: Design process and taste for HTML artifacts

**Choose your tool based on the task:**

| Task | Tool |
|------|------|
| Software architecture diagram (dark theme) | `architecture-diagram` |
| Hand-drawn flowchart/sequence diagram | `excalidraw` |
| Formal design token spec file | `design-md` |
| Match Stripe/Linear/Vercel look | `popular-web-designs` |
| Design a landing page/prototype from scratch | `claude-design` |

---

## 1. Architecture Diagram (SVG/HTML)

### Scope

**Best suited for:**
- Software system architecture (frontend/backend/database layers)
- Cloud infrastructure (VPC, regions, subnets, managed services)
- Microservice/service-mesh topology
- Database + API map, deployment diagrams

**Look elsewhere for:**
- Physics, chemistry, math, biology (scientific subjects)
- Physical objects (vehicles, hardware, anatomy)
- Floor plans, narrative journeys
- Hand-drawn whiteboard sketches → use `excalidraw`
- Animated explainers → use animation skill

### Color Palette (Semantic Mapping)

| Component Type | Fill (rgba) | Stroke (Hex) |
|----------------|-------------|--------------|
| **Frontend** | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan) |
| **Backend** | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) |
| **Database** | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet) |
| **AWS/Cloud** | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber) |
| **Security** | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose) |
| **Message Bus** | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange) |
| **External** | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate) |

### Typography & Background

- **Font:** JetBrains Mono (Google Fonts)
- **Sizes:** 12px (Names), 9px (Sublabels), 8px (Annotations), 7px (Tiny)
- **Background:** Slate-950 (`#020617`) with 40px grid pattern

### Output Format

- Single self-contained `.html` file
- No external dependencies (except Google Fonts)
- No JavaScript — pure CSS for animations
- Opens in any browser, works offline

### Usage

```bash
# Generate diagram, save to path
write_file(path="~/my-architecture.html", content="<html>...</html>")

# Preview
xdg-open ~/my-architecture.html  # Linux
open ~/my-architecture.html      # macOS
```

### Template Reference

Load the HTML template:
```
skill_view(name="design-and-diagrams", file_path="templates/architecture-diagram/template.html")
```

---

## 2. Excalidraw (Hand-Drawn Diagrams)

### Overview

Create diagrams using standard Excalidraw element JSON. Files can be opened at [excalidraw.com](https://excalidraw.com) for viewing and editing.

### Workflow

1. Write elements JSON array
2. Save as `.excalidraw` file
3. Optionally upload for shareable link

### Saving a Diagram

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "hermes-agent",
  "elements": [ ...your elements... ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  }
}
```

Save to: `~/diagrams/my_diagram.excalidraw`

### Uploading for Shareable Link

```bash
python skills/diagramming/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw
```

Requires: `pip install cryptography`

### Element Format

**Required fields (all elements):** `type`, `id`, `x`, `y`, `width`, `height`

**Defaults (auto-applied):**
- `strokeColor`: `"#1e1e1e"`
- `backgroundColor`: `"transparent"`
- `fillStyle`: `"solid"`
- `strokeWidth`: `2`
- `roughness`: `1` (hand-drawn look)
- `opacity`: `100`

### Element Types

**Rectangle:**
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }
```
- `roundness: { "type": 3 }` for rounded corners
- `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` for filled

**Ellipse:**
```json
{ "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**Diamond:**
```json
{ "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

### Labeled Shapes (Container Binding)

**CRITICAL:** Do NOT use `"label": { "text": "..." }` on shapes — this is invalid and produces blank shapes.

**Correct approach:** Create bound text element:

```json
{
  "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,
  "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid",
  "boundElements": [{ "id": "t_r1", "type": "text" }]
},
{
  "type": "text", "id": "t_r1", "x": 105, "y": 110, "width": 190, "height": 25,
  "text": "Hello", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "r1", "originalText": "Hello", "autoResize": true
}
```

Works on: rectangle, ellipse, diamond. Text is auto-centered by Excalidraw.

### Labeled Arrow

```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow",
  "boundElements": [{ "id": "t_a1", "type": "text" }]
},
{
  "type": "text", "id": "t_a1", "x": 370, "y": 130, "width": 60, "height": 20,
  "text": "connects", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "a1", "originalText": "connects", "autoResize": true
}
```

### Standalone Text (Titles/Annotations)

```json
{
  "type": "text", "id": "t1", "x": 150, "y": 138,
  "text": "Hello", "fontSize": 20, "fontFamily": 1,
  "strokeColor": "#1e1e1e", "originalText": "Hello", "autoResize": true
}
```

- `x` is LEFT edge. To center at `cx`: `x = cx - (text.length * fontSize * 0.5) / 2`
- Do NOT rely on `textAlign` or `width` for positioning

### Arrow

```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow"
}
```

- `points`: `[dx, dy]` offsets from element `x`, `y`
- `endArrowhead`: `null` | `"arrow"` | `"bar"` | `"dot"` | `"triangle"`
- `strokeStyle`: `"solid"` (default) | `"dashed"` | `"dotted"`

### Arrow Bindings

```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0,
  "points": [[0,0],[150,0]], "endArrowhead": "arrow",
  "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },
  "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }
}
```

`fixedPoint`: `top=[0.5,0]`, `bottom=[0.5,1]`, `left=[0,0.5]`, `right=[1,0.5]`

### Drawing Order (z-order)

- Array order = z-order (first = back, last = front)
- Emit progressively: bg zones → shape → bound text → arrows → next shape

**BAD:** all rectangles, then all texts, then all arrows
**GOOD:** bg_zone → shape1 → text_for_shape1 → arrow1 → arrow_label_text → shape2 → ...

### Color Palette

| Use | Fill Color | Hex |
|-----|-----------|-----|
| Primary / Input | Light Blue | `#a5d8ff` |
| Success / Output | Light Green | `#b2f2bb` |
| Warning / External | Light Orange | `#ffd8a8` |
| Processing / Special | Light Purple | `#d0bfff` |
| Error / Critical | Light Red | `#ffc9c9` |
| Notes / Decisions | Light Yellow | `#fff3bf` |
| Storage / Data | Light Teal | `#c3fae8` |

### Tips

- Use color palette consistently
- **Text contrast is CRITICAL** — never light gray on white. Minimum text: `#757575`
- Do NOT use emoji in text
- For dark mode diagrams, see `references/dark-mode.md`

---

## 3. DESIGN.md (Design Token Specs)

### Overview

DESIGN.md is Google's open spec for describing visual identity to coding agents. One file combines:

- **YAML front matter** — machine-readable design tokens
- **Markdown body** — human-readable rationale

### When to Use

- User asks for DESIGN.md file, design tokens, or design system spec
- User wants consistent UI/brand across projects
- User wants contrast/WCAG accessibility validation

### File Anatomy

```md
---
version: alpha
name: Heritage
description: Architectural minimalism meets journalistic gravitas.
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
---

## Overview

Architectural Minimalism meets Journalistic Gravitas...

## Colors

- **Primary (#1A1C1E):** Deep ink for headlines.
- **Tertiary (#B8422E):** "Boston Clay" — interaction driver.

## Typography

Public Sans for everything...

## Components

`button-primary` is the only high-emphasis action...
```

### Token Types

| Type | Format | Example |
|------|--------|---------|
| Color | `#` + hex (sRGB) | `"#1A1C1E"` |
| Dimension | number + unit | `48px`, `-0.02em` |
| Token reference | `{path.to.token}` | `{colors.primary}` |
| Typography | object with fontFamily, fontSize, fontWeight, etc. | see above |

**Component property whitelist:** `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`

**Variants are separate keys:** `button-primary-hover`, NOT `button-primary.hover`

### Canonical Section Order

1. Overview (alias: Brand & Style)
2. Colors
3. Typography
4. Layout (alias: Layout & Spacing)
5. Elevation & Depth (alias: Elevation)
6. Shapes
7. Components
8. Do's and Don'ts

Unknown sections are preserved. Unknown token names accepted if valid type.

### Workflow: Authoring

1. Ask user (or infer) brand tone, accent color, typography
2. Write `DESIGN.md` in project root
3. Use token references (`{colors.primary}`) in components
4. Lint it — fix broken references or WCAG failures
5. Export to Tailwind or DTCG if needed

### CLI Commands

```bash
# Validate structure + token references + WCAG contrast
npx -y @google/design.md lint DESIGN.md

# Compare two versions, fail on regression
npx -y @google/design.md diff DESIGN.md DESIGN-v2.md

# Export to Tailwind theme JSON
npx -y @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json

# Export to W3C DTCG JSON
npx -y @google/design.md export --format dtcg DESIGN.md > tokens.json

# Print spec
npx -y @google/design.md spec --rules-only --format json
```

### Lint Rules

- `broken-ref` (error) — `{colors.missing}` points at non-existent token
- `duplicate-section` (error) — same `## Heading` appears twice
- `invalid-color`, `invalid-dimension`, `invalid-typography` (error)
- `wcag-contrast` (warning) — component textColor vs backgroundColor ratio
- `unknown-component-property` (warning) — outside whitelist

### Pitfalls

- Don't nest component variants — use sibling keys
- Hex colors must be quoted strings
- Negative dimensions need quotes: `letterSpacing: "-0.02em"`
- Section order is enforced — reorder prose to match canonical list
- Token references resolve by dotted path: `{colors.primary}` works, `{primary}` does not

### Spec Source

- Repo: https://github.com/google-labs-code/design.md (Apache-2.0)
- CLI: `@google/design.md` on npm

---

## 4. Popular Web Designs (Brand Templates)

### Overview

54 production-quality design systems extracted from real websites. Each template includes colors, typography, components, layout rules, and ready-to-use CSS values.

### How to Use

1. Pick a design from the catalog
2. Load it: `skill_view(name="design-and-diagrams", file_path="templates/<site>.md")`
3. Use design tokens and component specs when generating HTML

### Font Substitution Reference

| Proprietary Font | CDN Substitute | Character |
|------------------|----------------|-----------|
| Geist / Geist Sans | Geist (Google Fonts) | Geometric, compressed tracking |
| sohne-var (Stripe) | Source Sans 3 | Light weight elegance |
| Berkeley Mono | JetBrains Mono | Technical monospace |
| Airbnb Cereal VF | DM Sans | Rounded, friendly geometric |
| Circular (Spotify) | DM Sans | Geometric, warm |
| figmaSans | Inter | Clean humanist |
| UberMove | DM Sans | Bold, tight |
| IBM Plex Sans/Mono | IBM Plex Sans/Mono | Available on Google Fonts |

### Design Catalog (Selected)

**AI & Machine Learning:**
- `claude.md` — Warm terracotta accent, clean editorial
- `ollama.md` — Terminal-first, monochrome simplicity
- `voltagent.md` — Void-black canvas, emerald accent

**Developer Tools:**
- `linear.app.md` — Ultra-minimal dark-mode, purple accent
- `vercel.md` — Black and white precision, Geist font
- `supabase.md` — Dark emerald theme, code-first
- `sentry.md` — Dark dashboard, data-dense, pink-purple

**Infrastructure:**
- `stripe.md` — Signature purple gradients, weight-300 elegance
- `hashicorp.md` — Enterprise-clean, black and white

**Productivity:**
- `notion.md` — Warm minimalism, serif headings
- `figma.md` — Vibrant multi-color, playful yet professional

**Fintech:**
- `coinbase.md` — Clean blue identity, trust-focused
- `wise.md` — Bright green accent, friendly and clear

### Choosing a Design

- **Developer tools/dashboards:** Linear, Vercel, Supabase, Sentry
- **Documentation:** Mintlify, Notion, Sanity
- **Marketing/landing:** Stripe, Framer, Apple
- **Dark mode UIs:** Linear, Cursor, ElevenLabs, Warp
- **Light/clean:** Vercel, Stripe, Notion
- **Playful:** PostHog, Figma, Lovable, Miro
- **Premium:** Apple, BMW, Stripe, Superhuman
- **Data-dense:** Sentry, Kraken, Cohere, ClickHouse

---

## 5. Claude Design (HTML Artifacts)

### Overview

Design one-off HTML artifacts (landing pages, prototypes, decks, component labs) with process and taste.

### When to Use vs Others

| Skill | What it gives you | Use when... |
|-------|-------------------|-------------|
| **claude-design** | Design process and taste | From-scratch designed artifact, no specific brand |
| **popular-web-designs** | 54 ready-to-paste design systems | "Make it look like Stripe/Linear/Vercel" |
| **design-md** | Formal DESIGN.md spec file | Output is token spec file, not rendered artifact |

### Decision Table

- **Process + taste, one-off artifact** → claude-design
- **Match a known brand's look** → popular-web-designs (let claude-design drive process)
- **Author the tokens spec** → design-md

These compose: use popular-web-designs for visual vocabulary, claude-design for process, design-md for token files.

### When To Use

- Landing pages, teaser pages
- High-fidelity prototypes
- Interactive product mockups
- Visual option boards
- Component explorations
- Design-system previews
- HTML slide decks
- Motion studies
- Onboarding flows
- Dashboard concepts
- Redesigns based on screenshots, repos, brand docs

### Design Principle: Start From Context

1. Brand docs
2. Existing product screenshots
3. Current repo components
4. Design tokens
5. UI kits
6. Prior mockups

If repo available, inspect actual source files before inventing UI.

### Workflow

1. **Understand the brief** — What, who, artifact, constraints
2. **Gather context** — Read docs, screenshots, repo files
3. **Define design system** — Colors, type, spacing, radii, shadows, motion
4. **Choose format** — Static visual, clickable prototype, deck, component lab
5. **Build artifact** — Prefer single self-contained HTML file
6. **Verify** — Confirm files exist, run syntax checks, open in browser
7. **Report** — Exact path, what created, caveats, next decision

### Artifact Format Rules

- Create descriptive filename: `Landing Page.html`, `Prototype.html`
- Embed CSS in `<style>`, JS in `<script>`
- Openable directly in browser
- Avoid remote dependencies unless stable
- Include responsive behavior

### HTML/CSS/JS Standards

- CSS variables for tokens
- CSS grid for layout
- Container queries when helpful
- `text-wrap: pretty` where supported
- Real focus states, hover states
- `prefers-reduced-motion` handling
- Responsive scaling
- Semantic HTML where practical

### React Guidance

Use plain HTML/CSS/JS by default. Use React only when:
- Artifact needs meaningful state
- Variants/toggles easier as components
- Target implementation is React/Next.js

### Deck Rules

- Fixed-size canvas: 1920×1080, 16:9
- Keyboard navigation
- Visible slide count
- localStorage persistence for current slide
- No speaker notes unless asked
- Text at least 24px for 1920×1080

### Prototype Rules

- Primary path clickable
- Include key states: default, hover/focus, loading, empty, error, success
- Expose variations with in-page controls
- Persist important state in localStorage

### Variation Rules

Default to at least three options:
1. **Conservative** — closest to existing patterns
2. **Strong-fit** — best interpretation of brief
3. **Divergent** — more novel, discover taste boundaries

### Anti-Slop Rules

Avoid:
- Aggressive gradient backgrounds
- Glassmorphism by default
- Emoji unless brand uses them
- Generic SaaS cards with icons everywhere
- Left-border accent callout cards
- Fake dashboards with arbitrary numbers
- Stock-photo hero sections
- Oversized rounded rectangles as hierarchy substitute
- Rainbow palettes
- Vague labels like "Insights," "Growth" without content

### Typography

- Editorial: serif/humanist headline, restrained sans body
- Software: precise sans with strong numeric treatment
- Luxury/minimal: fewer weights, more spacing
- Technical: mono accents only, not mono everywhere
- Deck: large, clear, high contrast

### Color

- Use brand/design-system colors first
- Define small system: neutrals, surface, ink, muted text, border, accent
- Prefer oklch for harmonious invented palettes
- Check contrast for important text and controls

### Layout and Composition

- Scale, whitespace, density, alignment, repetition, contrast, interruption
- Avoid every section being same card grid
- Product UIs: speed of comprehension over decoration
- Marketing: one idea per section
- Dashboards: only show data that helps decide

### Motion

Good motion:
- Clarifies state changes
- Reduces anxiety during loading
- Shows continuity between surfaces
- Stays subtle

Bad motion:
- Loops without purpose
- Delays user
- Calls attention to itself
- Hides poor hierarchy

### Images and Icons

- Use real supplied imagery when available
- Use clean placeholder if asset missing
- Use typography, layout, or abstract texture instead
- Do NOT draw elaborate fake SVG illustrations unless explicitly illustration work
- Avoid iconography unless it improves scanning

### Verification

Minimum:
- File exists at stated path
- HTML saved completely
- Obvious syntax issues checked

Better:
- Open in browser tool, check console errors
- Inspect screenshots at primary viewport
- Test key interactions

---

## Quick Reference

| Task | Primary Tool | Secondary |
|------|--------------|-----------|
| Software architecture diagram | architecture-diagram | excalidraw |
| Hand-drawn flowchart | excalidraw | — |
| Design token spec file | design-md | — |
| Match brand look | popular-web-designs | claude-design |
| Design landing page | claude-design | popular-web-designs |
| Design prototype | claude-design | — |
| Design slide deck | claude-design | — |
| WCAG contrast check | design-md (lint) | — |
| Export tokens to Tailwind | design-md | — |