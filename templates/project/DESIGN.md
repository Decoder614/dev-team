# UI/UX Design System & Tokens — [Project Name]

> **Target Project Design Guidelines**  
> Visual language, design tokens, typography, color palettes, and component patterns for [Project Name].  
> *(Note: This document is optional for backend services, libraries, and CLI tools without a graphical user interface).*

---

## 1. Design Philosophy & Visual Language

- **Core Theme:** [e.g., Clean, modern, accessible, high-contrast, data-dense]
- **Design Metaphor:** [e.g., Material 3, Human Interface Guidelines, Custom Brand Guidelines]
- **Target Form Factors:** [Mobile (Phone / Tablet), Desktop, Web Responsive]
- **Accessibility Level:** Target WCAG 2.1 AA compliance (contrast ratios, tap target sizing, screen reader semantics).

---

## 2. Color Palette & Tokens

### 2.1 Semantic Color Roles

| Token | Light Theme | Dark Theme | Description & Usage |
|---|---|---|---|
| `color-primary` | `#[HEX]` | `#[HEX]` | Primary brand actions, active states, key buttons |
| `color-on-primary` | `#[HEX]` | `#[HEX]` | Text/icons displayed on top of primary color |
| `color-secondary` | `#[HEX]` | `#[HEX]` | Secondary accents, highlights, floating chips |
| `color-background` | `#[HEX]` | `#[HEX]` | Application window and page background |
| `color-surface` | `#[HEX]` | `#[HEX]` | Cards, modals, elevated sheets, input fields |
| `color-text-primary` | `#[HEX]` | `#[HEX]` | High-emphasis headings, titles, primary body |
| `color-text-secondary` | `#[HEX]` | `#[HEX]` | Medium-emphasis labels, subtitles, captions |
| `color-border` | `#[HEX]` | `#[HEX]` | Dividers, card strokes, input outlines |
| `color-success` | `#[HEX]` | `#[HEX]` | Confirmations, success badges, checkmarks |
| `color-warning` | `#[HEX]` | `#[HEX]` | Warnings, caution alerts, non-blocking notices |
| `color-error` | `#[HEX]` | `#[HEX]` | Destructive actions, validation errors, alerts |

---

## 3. Typography Scale

- **Primary Font Family:** `[Font Name, e.g., Inter, Roboto, Poppins, sans-serif]`
- **Monospace Font Family:** `[Font Name, e.g., JetBrains Mono, Fira Code, monospace]`

| Style Role | Font Size | Weight | Line Height | Letter Spacing |
|---|---|---|---|---|
| `display-large` | 32px / 2.0rem | Bold (700) | 40px | -0.5px |
| `title-medium` | 20px / 1.25rem | Semi-Bold (600)| 28px | 0px |
| `body-large` | 16px / 1.0rem | Regular (400) | 24px | 0.15px |
| `body-medium` | 14px / 0.875rem | Regular (400) | 20px | 0.25px |
| `label-small` | 11px / 0.6875rem | Medium (500) | 16px | 0.5px |

---

## 4. Spacing & Elevation

### 4.1 Spacing Scale (8-Point Grid)
- `space-2` (4px): Micro padding, badge margins, inline icon gaps
- `space-4` (8px): Compact item padding, chip gaps
- `space-8` (16px): Standard content padding, card padding, form control spacing
- `space-12` (24px): Section separators, modal gutters
- `space-16` (32px): Major layout divisions, page boundaries

### 4.2 Radii & Elevation
- **Border Radius:**
  - `radius-sm` (4px): Small buttons, tags, chips
  - `radius-md` (8px): Inputs, cards, dialogs
  - `radius-lg` (16px): Bottom sheets, modal windows
  - `radius-full` (9999px): Circular avatars, pill buttons
- **Elevation / Shadows:**
  - `elevation-0`: Flat surface, bordered
  - `elevation-1`: Subtle drop shadow for cards and list tiles
  - `elevation-2`: Raised modals, floating action buttons, dropdown menus

---

## 5. Standard Component Guidelines

1. **Buttons:**
   - Primary: High emphasis, filled background. Exactly one primary action per screen context.
   - Secondary / Outlined: Medium emphasis for secondary flows.
   - Text / Flat: Low emphasis, cancel actions, subtle toolbars.
   - Minimum tap target: 48x48 px (or 44x44 pt on iOS).
2. **Form Inputs:**
   - Clear labels, persistent helper or error text below the field.
   - Visual focus rings matching `color-primary`.
   - Disabled states must maintain legible contrast.
3. **Empty & Loading States:**
   - Skeleton loaders or progress spinners for asynchronous fetching.
   - Informative illustrations or icons with action buttons for empty lists.
4. **Motion & Transitions:**
   - Fast, subtle easing (150ms–250ms) for micro-interactions and transitions.
   - Respect user preferences for reduced motion (`prefers-reduced-motion`).

