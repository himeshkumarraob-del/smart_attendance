---
name: Precision Intelligence Dashboard
colors:
  surface: '#fcf8fa'
  surface-dim: '#dcd9db'
  surface-bright: '#fcf8fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f5'
  surface-container: '#f0edef'
  surface-container-high: '#eae7e9'
  surface-container-highest: '#e4e2e4'
  on-surface: '#1b1b1d'
  on-surface-variant: '#45464d'
  inverse-surface: '#303032'
  inverse-on-surface: '#f3f0f2'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#0058be'
  on-secondary: '#ffffff'
  secondary-container: '#2170e4'
  on-secondary-container: '#fefcff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#271901'
  on-tertiary-container: '#98805d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#fcdeb5'
  tertiary-fixed-dim: '#dec29a'
  on-tertiary-fixed: '#271901'
  on-tertiary-fixed-variant: '#574425'
  background: '#fcf8fa'
  on-background: '#1b1b1d'
  surface-variant: '#e4e2e4'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-tabular:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  container-max: 1440px
  sidebar-width: 280px
---

## Brand & Style
The design system is engineered for high-stakes administrative environments where data clarity and system reliability are paramount. It adopts a **Corporate / Modern** aesthetic, prioritizing a "technical professional" atmosphere that feels both authoritative and innovative.

The target audience consists of HR administrators, department heads, and IT managers. The UI evokes a sense of **precision, efficiency, and calm control** through the use of generous whitespace, a structured grid, and a purposeful color application that draws the eye to critical status indicators without causing cognitive fatigue.

## Colors
The palette is built on a foundation of **Deep Navy** to establish professional gravity. **Electric Blue** is reserved strictly for primary interactive elements and focus states. 

Functional colors (Emerald, Amber, Rose) are mapped to attendance states:
- **Emerald:** Present / Verified / System Healthy.
- **Amber:** Late / Pending Verification / Syncing.
- **Rose:** Absent / Unauthorized / System Error.

In **Dark Mode**, surfaces shift to **Slate-900**, utilizing subtle border increments rather than heavy shadows to define depth, ensuring the "glow" of the data visualization remains the focal point.

## Typography
This design system utilizes **Inter** for its exceptional legibility in data-dense environments. 

- **Numerical Data:** For attendance counts and percentages, utilize `data-tabular` settings (Tabular Lnum) to ensure numbers align vertically in tables.
- **Hierarchy:** Headlines use a tighter letter-spacing and heavier weights to stand out against the UI chrome.
- **Labels:** Use `label-md` for table headers and sidebar category titles to create clear structural breaks.

## Layout & Spacing
The layout follows a **Fixed-Fluid hybrid grid**:
- **Sidebar:** Fixed at `280px` for persistent navigation.
- **Main Content:** Fluid 12-column grid with a `1440px` max-width.
- **Gutter/Margins:** `24px` (lg) on desktop, reducing to `16px` (md) on mobile.

Spacing follows an 8pt rhythm. Vertical rhythm in data tables should be strictly maintained with `12px` (1.5 units) of padding for compact views and `16px` (2 units) for standard views.

## Elevation & Depth
The system uses **Tonal Layers** combined with **Ambient Shadows** to signify hierarchy:

- **Level 0 (Background):** `bg_light` (#F8FAFC). No shadow.
- **Level 1 (Cards/Sidebar):** White surface with a `0 1px 3px rgba(15, 23, 42, 0.08)` shadow.
- **Level 2 (Modals/Dropdowns):** White surface with a `0 10px 15px -3px rgba(15, 23, 42, 0.12)` shadow.

In Dark Mode, elevation is communicated through **Surface Tints**. The higher the elevation, the lighter the Slate hex code (e.g., Level 0 is Slate-950, Level 1 is Slate-900).

## Shapes
The design system employs **Soft** geometry (`0.25rem` base) to maintain a modern feel without appearing overly casual. 

- **Inputs/Buttons:** `4px` (rounded-sm) for a crisp, professional look.
- **Cards/Containers:** `8px` (rounded-lg) to provide a distinct container boundary.
- **Status Badges:** `9999px` (pill-shaped) to differentiate data tags from interactive buttons.

## Components
- **Buttons:** Primary buttons use `primary_color_hex` with white text. Secondary actions use a ghost style (border only) or a light blue tint.
- **Data Tables:** High-contrast rows. Use a 1px border-bottom (#E2E8F0) between rows. Zebra striping is not required if the border is distinct.
- **Attendance Chips:** Small, pill-shaped indicators. Emerald background with 10% opacity + solid emerald text for "Present". 
- **Cards:** White background, 1px border (#F1F5F9). Title always in `headline-md` weight.
- **Sidebar:** Dark theme by default (using `primary_color_hex`). Active states should use a left-edge 4px "Electric Blue" border accent and a subtle white-opacity background highlight.
- **Charts:** Use a 2px stroke width for line charts. Use the functional color palette (Success, Warning, Danger) for multi-series data representing attendance trends.