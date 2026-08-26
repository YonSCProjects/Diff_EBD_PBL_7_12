---
name: Chromium break-inside: avoid is unreliable in tight print layouts
description: When Chromium cannot fit an element whole on the remaining page, it sometimes violates break-inside: avoid rather than push the element to the next page. Use deterministic page-break-before rules as a safety net.
type: feedback
---

For card/PDF print layouts rendered via puppeteer, `break-inside: avoid` + `page-break-inside: avoid` on a block element is **not a guarantee**. Chromium will split the block across pages if pushing it whole to the next page would leave page 1 too empty by its internal heuristic. Even `!important` doesn't help.

**Why:** verified on T1·M3 card — the blue `.why` callout box sat below an ASCII `.wiring-block`. Despite having `break-inside: avoid !important; display: flow-root; page-break-inside: avoid` + proper block markup (no `<br>`), Chromium still split the box across pages — title on page 1, body on page 2.

**How to apply:** when a layout *must* keep a specific callout intact and the surrounding content is heavy (ASCII diagrams, code blocks, long lists), add a deterministic sibling-selector rule like:

```css
.wiring-block + .why,
.code-block + .why,
pre + .why {
  page-break-before: always;
  break-before: page;
}
```

This trades a bit of page-1 whitespace for a guaranteed intact callout. Also documented in [C:\Users\Yon\.claude\plans\flickering-pondering-snowglobe.md](C:\Users\Yon\.claude\plans\flickering-pondering-snowglobe.md).
