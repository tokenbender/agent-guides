---
name: manim-math-explainer
description: |
  Trigger when: (1) the user asks for Manim, Manim Community, or ManimCE,
  (2) code contains `from manim import *`, or (3) the task is to build a
  mathematical explainer animation.

  Opinionated Manim Community skill for concise math scenes. Focuses on scene
  structure, proof-style layout, visual language, text and formulas, trackers
  and updaters, graphing, and a fast render workflow.

  Not for ManimGL (`from manimlib import *`, `manimgl`).
---

## Scope

- Default to Manim Community Edition.
- Build scenes that explain one idea at a time.
- Prefer official Manim APIs and example-gallery patterns over low-level point editing.
- Optimize for quick iteration first, polish second.

## Read First

- `rules/core-workflow.md`
- `rules/visual-style.md`
- `rules/proof-layouts.md`
- `rules/text-and-math.md`
- `rules/dynamics-and-graphing.md`

When a request is mainly about aesthetics, composition, pacing, or visual tone,
prioritize `rules/visual-style.md` and keep the rest secondary.

## Default Operating Rules

1. Confirm the stack before writing code.
   If imports or commands suggest `manimgl` or `manimlib`, stop and switch mental models.
2. Start with one compact scene in one file.
3. Build in this order: create, position, style, animate.
4. Prefer `Create`, `Write`, `FadeIn`, `FadeOut`, `Transform`, `ReplacementTransform`, `TransformMatchingTex`, and `.animate`.
5. Use `Text` for prose, `MathTex` for formulas, and `Tex` only when mixing prose with LaTeX intentionally.
6. Use `ValueTracker` with `always_redraw(...)` or simple updaters for dynamic geometry.
7. Keep color semantics stable across the whole scene.
8. Use camera movement only when it adds meaning.

## Visual Defaults

- Editorial, proof-first composition
- One focal point per beat
- Stable layout and restrained camera motion
- Limited semantic palette instead of decorative multicolor styling
- Smooth, identity-preserving transforms over flashy effects
- Clean negative space and readable frame density

## Render Loop

```bash
manim -pql scene.py SceneName
manim -sql scene.py SceneName
manim -pqm scene.py SceneName
manim -qh scene.py SceneName
```

- `-pql`: fast development loop
- `-sql`: save last frame only
- `-pqm`: medium-quality check
- `-qh`: final render

## Preferred Toolbox

- Layout: `VGroup`, `Group`, `arrange`, `arrange_in_grid`, `next_to`, `align_to`, `to_edge`, `to_corner`
- Emphasis: `SurroundingRectangle`, `Brace`, `Arrow`, `Indicate`, `Circumscribe`
- Equation work: `MathTex`, `TransformMatchingTex`, `substrings_to_isolate`, `index_labels`
- Dynamic scenes: `ValueTracker`, `always_redraw`, `add_updater`, `TracedPath`
- Plotting: `Axes`, `NumberPlane`, `axes.plot`, `axes.get_graph_label`, `axes.i2gp`

## Red Flags

- `from manimlib import *` in a ManimCE task
- `Tex` used for ordinary prose when `Text` is enough
- Direct `VMobject.points` manipulation without a concrete need
- Formula coloring without isolating substrings first
- Heavy camera motion in proof-like scenes
- Too many simultaneous animations for a single conceptual beat

## Templates

- `templates/basic_scene.py`
- `templates/tracker_graph_scene.py`
