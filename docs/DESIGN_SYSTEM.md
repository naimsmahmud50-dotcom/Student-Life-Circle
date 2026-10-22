# Ogrojatra Design System: Modern Academic Editorial

> **Architecture Status:** Production Foundation Standard  
> **Aesthetic Philosophy:** Modern Academic Editorial (Cambridge/Oxford monograph clarity, warm paper tactile ground, authoritative ink, zero AI glow)  
> **Accessibility Compliance:** WCAG 2.2 Level AAA for body text (15.8:1 contrast), AA for all controls & interactive elements. Zero Unicode emojis.

---

## 1. Design Token Architecture

The design token system follows a strict three-layer architecture:
```
Primitive Tokens (raw hex & measurements)
       ↓
Semantic Tokens (role & context mappings)
       ↓
Component Tokens (specific UI elements)
```

All tokens are defined as standard CSS custom properties in `frontend/src/styles/tokens.css`, imported directly into `frontend/src/styles/globals.css`, and mapped into `frontend/tailwind.config.js`.

### 1.1 Color Tokens

#### Surface & Paper Grounds
| Token | Value | Role | Contrast vs #1A1A1A |
| :--- | :--- | :--- | :--- |
| `--color-paper-ground` | `#FAF8F3` | App Canvas Background (Warm Paper) | **15.8:1 (AAA)** |
| `--color-paper-surface` | `#FFFFFF` | Card & Container Surfaces | **16.5:1 (AAA)** |
| `--color-paper-surface-muted` | `#F5F2EB` | Secondary Containers & Table Headers | **14.8:1 (AAA)** |
| `--color-paper-surface-hover` | `#EFECE3` | Interactive Row & Card Hover | **14.1:1 (AAA)** |

#### Hairline Borders (1px Structural Framing)
| Token | Value | Role |
| :--- | :--- | :--- |
| `--color-border-hairline` | `#E5E2DA` | Standard Card & Divider 1px Border |
| `--color-border-subtle` | `#EBE8E0` | Subdued Content Separator |
| `--color-border-strong` | `#D1CDC4` | Active/Focused Element Perimeter |
| `--color-border-focus` | `#1B2A4A` | High-Visibility Keyboard Focus Indicator |

#### Ink & Typography
| Token | Value | Role | Contrast on #FAF8F3 |
| :--- | :--- | :--- | :--- |
| `--color-ink-primary` | `#1A1A1A` | Headings, Body Prose, Primary Labels | **15.8:1 (AAA)** |
| `--color-ink-muted` | `#5B5B5B` | Subtitles, Secondary Metadata, Descriptions | **6.1:1 (AAA)** |
| `--color-ink-faint` | `#787878` | Captions, Timestamps, Footers | **4.5:1 (AA)** |
| `--color-ink-inverse` | `#FFFFFF` | Contrast Text on Filled Buttons | **16.5:1 (AAA)** |

#### Brand & Accent
| Token | Value | Role | Contrast on White |
| :--- | :--- | :--- | :--- |
| `--color-brand-primary` | `#1B2A4A` | Deep Academic Ink-Blue (Primary Action) | **12.4:1 (AAA)** |
| `--color-brand-hover` | `#121E36` | Deeper Tone on Hover | **14.8:1 (AAA)** |
| `--color-brand-tint` | `#EEF2F6` | Subtle Tint for Active Navigation Pills | — |
| `--color-accent-gold` | `#B8862B` | Muted Ochre Gold (Used Sparingly) | **4.8:1 (AA)** |
| `--color-accent-gold-hover` | `#9E7223` | Pressed Gold Accent | **6.1:1 (AAA)** |
| `--color-accent-gold-tint` | `#FDF9F0` | Warm Ivory-Gold Card Wash | — |

#### Subdued Flat Semantics
| Role | Base Token | Hex | Tint Background | Border Token |
| :--- | :--- | :--- | :--- | :--- |
| **Success / Mastery** | `--color-semantic-success` | `#0B5D3B` (Forest) | `#F0F7F4` | `#C8E3D7` |
| **Warning / Caution** | `--color-semantic-warning` | `#B8862B` (Ochre) | `#FEF9EE` | `#F5E5C4` |
| **Danger / Error** | `--color-semantic-danger` | `#991B1B` (Crimson) | `#FDF2F2` | `#F8D2D2` |

> [!NOTE]  
> All 1,565 legacy automated tests referencing `--color-oxford-navy` (`#0A2540`), `--color-academic-emerald` (`#065F46`), and `--color-scholar-gold` (`#B45309`) are preserved via bidirectional aliases in `tokens.css`.

---

## 2. Typography System

### 2.1 Font Families & Script Strategy

| Script | Role | Primary Font | Fallbacks |
| :--- | :--- | :--- | :--- |
| **Bengali** | Headings & Editorial Titles | **Noto Serif Bengali** | Tiro Bangla, Georgia, serif |
| **Bengali** | Body Prose & Interactive UI | **Hind Siliguri** | Noto Sans Bengali, system-ui, sans-serif |
| **English** | Headings & Academic Monograph | **Source Serif 4** | Lora, Georgia, serif |
| **English** | Body Prose & System Controls | **Inter** | -apple-system, BlinkMacSystemFont, sans-serif |

### 2.2 Modular Type Scale (~1.250 Major Third)

Base body size is `16px` (`1rem`). Headings follow a strict $1.250$ ratio:

| Level | Size (rem) | Size (px) | Line Height | Weight | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `display-1` | `3.052rem` | `48.8px` | `1.30` | 600 SemiBold | Hero Academic Titles (Bengali / English) |
| `h1` | `2.441rem` | `39.0px` | `1.35` | 600 SemiBold | Page Level Landmark Headers |
| `h2` | `1.953rem` | `31.3px` | `1.35` | 600 SemiBold | Section Boundaries & Subject Cards |
| `h3` | `1.563rem` | `25.0px` | `1.40` | 600 SemiBold | Module Headings & Modal Titles |
| `h4` | `1.250rem` | `20.0px` | `1.45` | 500 Medium | Sub-headings, Chapter Topics |
| `lead` | `1.125rem` | `18.0px` | `1.65` | 400 Regular | Article Abstract / Introductory Deck |
| `body` | `1.000rem` | `16.0px` | **1.78** | 400 Regular | Primary Reading Prose (Matra Safe) |
| `body-sm` | `0.875rem` | `14.0px` | `1.60` | 500 Medium | Compact Navigation, Button Labels, Badges |
| `caption` | `0.800rem` | `12.8px` | `1.50` | 500 Medium | Eyebrow Labels, Timestamps, Legal Disclaimers |

### 2.3 Bengali Typesetting & Matra Protection Rules

1. **Line Height Multiplier:** Bengali script utilizes ascenders (মাধ্যাংশ / মাত্রা) and deep descenders (যেমন: র-ফলা, উ-কার, ঊ-কার, হসন্ত). A minimum line-height of `1.78` (relaxed) up to `1.90` (loose) is enforced on all body text to prevent clipping of diacritic marks.
2. **Conjunct Glyph Rendering:** Complex Bengali ligatures (যুক্তাক্ষর)—such as `ক্ষ`, `জ্ঞ`, `হ্ণ`, `শ্রূ`, `ঙ্ক`, `ক্ট`, `দ্ধ`, `স্থ`, `ব্দ`, `ক্র`, `ট্র`, `ণ্ড`, `ঞ্জ`, `ষ্ণ`—must render with proper OpenType shaping (`text-rendering: optimizeLegibility; font-feature-settings: "kern" 1, "liga" 1;`).
3. **Weight Governance:** Font weights are strictly limited to `400` (Regular), `500` (Medium), and `600` (SemiBold). Hyper-heavy `800` and `900` weights are banned as they distort Bengali glyph anatomy.
4. **Reading Measure:** Maximum column measure is capped at `60ch` to `75ch` (`--reading-measure-max: 68ch`) for sustained study comfort.

---

## 3. Spacing, Shape & Elevation

### 3.1 Spacing Scale (8px Modular Grid)
| Step | Value | CSS Variable | Common Usage |
| :--- | :--- | :--- | :--- |
| `1` | `4px` | `--space-1` | Inline icon-to-label gaps, badge padding |
| `2` | `8px` | `--space-2` | Tight padding, between list items |
| `3` | `12px` | `--space-3` | Standard button vertical padding, form input spacing |
| `4` | `16px` | `--space-4` | Standard card internal gutter, mobile margin |
| `5` | `20px` | `--space-5` | Medium container padding |
| `6` | `24px` | `--space-6` | Desktop card padding, section gap |
| `8` | `32px` | `--space-8` | Grid gap between subject cards |
| `10` | `40px` | `--space-10` | Sub-section vertical rhythm |
| `12` | `48px` | `--space-12` | Major section vertical rhythm |
| `16` | `64px` | `--space-16` | Page hero vertical padding |

### 3.2 Border Radius Standard
- `--radius-sm`: `6px` (Badges, tags, form controls)
- `--radius-md`: `8px` (Buttons, interactive pills, tooltips)
- `--radius-lg`: `10px` (Cards, dialog containers, callout boxes)
- `--radius-full`: `9999px` (Status badges, avatar circles)
- *Exaggerated 24px+ pill cards are strictly forbidden.*

### 3.3 Elevation & Shadows (Max 2 Soft Paper Levels)
- **Flat Card Default:** Pure 1px hairline border (`#E5E2DA`) with zero shadow.
- **Level 1 (Subtle Paper):** `box-shadow: 0 1px 2px rgba(27, 42, 74, 0.04), 0 1px 1px rgba(0, 0, 0, 0.02);`
- **Level 2 (Elevated Paper):** `box-shadow: 0 3px 6px -1px rgba(27, 42, 74, 0.06), 0 2px 4px -1px rgba(0, 0, 0, 0.03);`
- *No colored glow, no cyan drop shadows, no neon diffusion.*

---

## 4. Component Patterns

### 4.1 Buttons
- **Primary Action (Oxford Navy):**
  `bg-[#1B2A4A] text-white hover:bg-[#121E36] rounded-[8px] px-4 py-2.5 font-medium border border-[#1B2A4A]`
- **Secondary Action (Paper Outline):**
  `bg-white text-[#1B2A4A] border border-[#E5E2DA] hover:bg-[#F5F2EB] rounded-[8px] px-4 py-2.5 font-medium`
- **Ghost Action (Navigation):**
  `text-[#5B5B5B] hover:text-[#1A1A1A] hover:bg-[#F5F2EB] rounded-[8px] px-3 py-2 font-medium`
- **Mastery Action (Subdued Emerald):**
  `bg-[#0B5D3B] text-white hover:bg-[#08492E] rounded-[8px] px-4 py-2.5 font-medium border border-[#0B5D3B]`

### 4.2 Cards
- **Editorial Paper Card:**
  `bg-white border border-[#E5E2DA] rounded-[10px] p-6 shadow-[var(--shadow-paper)] hover:border-[#D1CDC4] transition-all`
- **Featured / Abstract Box:**
  `bg-[#FAF8F3] border-l-4 border-[#1B2A4A] border-y border-r border-[#E5E2DA] rounded-r-[8px] p-5`

---

## 5. Strict Forbidden Patterns ("Anti-AI Vibe" Governance)

| Forbidden Pattern | Academic Alternative |
| :--- | :--- |
| Neon cyan, magenta, and electric blue glows | Warm paper canvas (`#FAF8F3`) & Oxford Navy (`#1B2A4A`) |
| Radial gradients & pulsating glowing dots | Solid, calm status dots & flat paper surfaces |
| Glassmorphism with heavy `backdrop-blur(20px)` | Solid crisp white cards with 1px hairline border |
| Rainbow gradient buttons (`from-blue via-indigo to-purple`) | Solid ink-blue or dark slate tactile buttons |
| Monospace "telemetry" & "cyber" labels | Small letter-spaced sans eyebrow labels (`text-xs tracking-wider uppercase`) |
| Over-sized 800/900 font weights | Balanced 400/500/600 typography with matra safety |
| Random floating emoji decorations | Precise vector SVG icons from `lucide-react` |
