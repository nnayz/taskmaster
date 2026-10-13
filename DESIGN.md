# Design Language

## Intent

Create a quiet, precise, softly structured interface. The overall impression should be calm, mature, and easy to inhabit for long periods. Visual confidence comes from alignment, proportion, and restraint.

The defining effect is a nearly monochrome environment with close tonal relationships, gently rounded geometry, modest text, and deliberate empty space. The interface feels lightweight while retaining a clear sense of structure.

Apply this language to whatever functionality the product requires. These guidelines describe visual treatment and interaction feel; they do not prescribe a screen composition or feature inventory.

The base surface colors below are sampled from visual references. Other values are recommended implementation targets. Typography, dimensions, and motion should be calibrated in context rather than treated as recovered source specifications.

## Visual Priorities

1. Establish a continuous, low-noise visual field.
2. Make the reading order clear through position, spacing, and text contrast.
3. Use small tonal differences to express structure and state.
4. Give broad shapes soft geometry and minimal depth.
5. Reserve strong contrast and saturated color for a few meaningful moments.

At a glance, the page should register as a coherent space. Individual boundaries become apparent as attention moves toward them.

## Color

Use neutral grays without a noticeable blue, purple, or brown cast. Most of the visible area should belong to three closely related surface tones. Keep large regions free of saturated color.

| Role | Light | Dark |
| --- | --- | --- |
| Foundation | `#FAFAFA` | `#080808` |
| Main visual field | `#FCFCFC` | `#0D0D0D` |
| Raised surface | `#FFFFFF` | `#161616` |
| Subtle emphasis | `#E8E8E8` | `#1A1A1A` |
| Quiet outline | `#EDEDED` | `#272725` |
| Primary text | `#191919` | `#E6E6E6` |
| Secondary text | `#6E6E6E` | `#A0A0A0` |
| Muted text | `#737373` | `#8C8C8C` |
| Accent | `#0088FF` | `#0088FF` |
| Accent for small text | `#006BD6` | `#2997FF` |

Keep the accent sparse. It should feel like a small signal within a neutral environment. A faint tint can support it, but large colored fields would change the character of the interface.

Meaningful state colors should occupy only the affected detail. Reinforce their meaning through text or another visible cue. Preserve the surrounding neutral field.

Use the quiet outline for visual separation. When a boundary is necessary to identify an interactive area, strengthen it enough to remain perceivable. Validate text contrast against the actual surface beneath it.

## Typography

Use a clean, contemporary sans serif with open letterforms and familiar proportions. A system sans serif is an appropriate starting point:

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

Regular weight should dominate. Use medium weight selectively to establish importance. Heavy typography should be rare. Avoid a large gap between the visual weight of headings and surrounding text.

| Text role | Starting size | Weight | Line height |
| --- | --- | --- | --- |
| Secondary detail | 12–13px | 400 | 1.4–1.5 |
| Standard interface text | 14–15px | 400–500 | 1.4–1.5 |
| Modest emphasis | 16–18px | 400–500 | 1.3–1.4 |
| Occasional major heading | 22–26px | 500 | 1.2–1.3 |

Use sentence case and natural letter spacing. Keep most labels on one line when practical. Longer content should retain comfortable line spacing and a readable measure of roughly 55–75 characters.

Hierarchy should remain shallow. A change in color or placement is often sufficient; avoid increasing size, weight, and contrast together for every level.

## Space and Composition

Combine compact functional spacing with generous space around the main focus. The interface can accommodate dense information while still feeling unhurried.

Use a consistent spacing scale:

```text
4, 8, 12, 16, 20, 24, 32, 48, 64
```

- Use 4–8px for tightly related details.
- Use 12–16px for routine internal spacing.
- Use 20–24px where content needs a comfortable inset.
- Use 32–64px between larger conceptual groups.

Align related content to shared edges. Keep repeated intervals stable. The result should feel carefully fitted without looking rigid or overdrawn.

Allow substantial empty space when the content is sparse. Do not stretch every group to fill the available area. Give the main focus a comfortable measure and balanced surrounding space.

When information becomes dense, tighten vertical rhythm while retaining clear alignment and consistent text sizing. The same visual language should support both open and compact compositions.

On smaller viewports, reduce outer margins and spacing progressively. Preserve reading order and comfortable interaction targets. Let content reflow before reducing type size.

## Geometry

Use softly rounded rectangular geometry. Curvature should be noticeable but controlled, with enough straight edge remaining to convey precision.

| Geometry scale | Starting radius |
| --- | --- |
| Compact | 6–8px |
| Medium | 10–12px |
| Broad | 16–20px |

Scale curvature with the footprint of a shape. Broad surfaces can feel softer than small interactive areas. Avoid assigning the same radius to every size.

Keep outlines thin, usually 1px. Avoid thick framing and repeated nested outlines. Separation should come primarily from space and small changes in surface tone.

## Depth and Surface Treatment

Keep depth close to the background plane. Surfaces should feel gently lifted, with no dramatic floating effect.

In the light theme, a restrained shadow can complement a quiet outline:

```css
box-shadow: 0 1px 2px rgb(0 0 0 / 0.025),
            0 2px 6px rgb(0 0 0 / 0.035);
```

In the dark theme, tonal separation and faint outlines should do most of the work. Shadows contribute little against nearly black surroundings and should not be made heavier to compensate.

Keep surfaces flat and matte. Avoid gloss, visible texture, colored lighting, pronounced gradients, and translucent effects. Depth should support legibility without becoming a visual subject.

## Small Visual Marks

Non-text marks should be compact, simple, and consistent in stroke weight. Use approximately 16–18px dimensions and 1.5–1.75px strokes as a starting point. Align them optically with nearby text.

Let their color follow the surrounding hierarchy. Keep silhouettes recognizable at small sizes and avoid unnecessary internal detail. Their visual weight should support the text beside them.

## Interaction Feel

Interaction should feel immediate, steady, and understated. State changes should clarify what can be acted on and what is currently active.

- Hover: introduce a small neutral tone change.
- Active state: use a persistent, modest tonal emphasis and clearer foreground contrast.
- Press: apply a brief tonal change with stable geometry.
- Keyboard focus: use a clearly visible 2px outline with approximately 2px offset.
- Unavailable state: reduce emphasis while keeping the label readable.

Do not make important actions discoverable only on hover. Maintain comfortable hit areas even when the visible treatment is compact. Aim for 40–44px targets where space permits.

Static references do not establish animation behavior. For implementation, use short transitions of roughly 120–180ms with a simple ease-out curve. Prefer color and opacity changes. Keep movement small, preserve layout stability, and respect reduced-motion preferences.

## Theme Relationship

Both themes should express the same mood and spatial logic. Preserve typography, proportions, spacing, and curvature across them.

The light theme feels airy through nearly white surfaces, quiet outlines, and faint shadows. The dark theme feels intimate through near-black foundations, charcoal surfaces, and soft light text.

Tune each theme independently. Preserve the relative importance of elements rather than mechanically inverting colors. Keep text comfortably distinct from its background while maintaining subtle surface transitions.

## Restraint Rules

- Keep broad backgrounds neutral.
- Use accent color sparingly and consistently.
- Keep most typography regular and moderately sized.
- Make spacing more prominent than decorative framing.
- Limit visible depth and avoid large shadow halos.
- Preserve generous empty space where the content allows it.
- Keep repeated geometry and alignment consistent.
- Avoid oversized promotional typography, decorative imagery, ornamental gradients, and excessive emphasis.

## Review Standard

The design is successful when it feels quiet at first glance, readable on closer inspection, and predictable in use. Structure should be easy to perceive without dominating the content. Dense and sparse areas should feel part of the same visual system.

Before accepting a screen, check that the reading order is clear, accent color remains rare, surface differences remain subtle, interaction states are visible, and the page retains room to breathe.
