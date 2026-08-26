---
name: ask-components-then-build
description: "Before authoring a project's card set, ask Yon the concrete component questions (what he owns / will order) in one batch, then run the whole creation process autonomously"
metadata:
  type: feedback
---

When Yon hands over a new project build ("create projects 5-8"), he expects: (1) a short
batch of concrete COMPONENT questions first — thickness of his polygal, 2WD vs 4WD, which
control modules exist, CAM/programmer/buck owned or to order, sensor model, OLEDs in the
drawer — then (2) the full card-creation process run end-to-end without further check-ins.

**Why:** his words on 2026-08-20: "if you have questions about the components we have then
ask and then go through the task cards creation process." The hardware in the workshop
drawer drives the design (e.g. the single-3V3-pin DevKit forced breadboard rails; his
8-10mm polygal changed the template's cut guidance), so guessing parts wastes a build.

**How to apply:** use AskUserQuestion with 2-4 tight questions (recommended option first),
state remaining assumptions explicitly in the reply, then build. A terse repeated
directive ("for p6 use DHT22" twice) is a firm decision even if I raised a concern —
communicate the consequence, find the design that honors it (OLED became the I2C device),
and proceed. Related: [[autonomous-batch-execution]], [[global-rules-no-carveouts]].
