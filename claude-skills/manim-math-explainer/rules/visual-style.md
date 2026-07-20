# Visual Style

This rule is only about visual and aesthetic choices.

## Overall Look

- Aim for an editorial, mathematical, proof-first feel.
- Treat each frame like a clean lecture note or textbook diagram in motion.
- Prefer clarity, elegance, and hierarchy over spectacle.
- Keep the background quiet unless the project already has a strong house style.

## Composition

- One focal point per beat.
- Anchor important objects in stable positions.
- Reuse screen regions so the viewer does not need to re-scan the whole frame.
- Leave generous negative space around the main object.
- Avoid filling every corner just because the screen is available.

## Typography

- Use a clear size hierarchy: title, main statement, supporting annotation.
- Keep prose short and subordinate to the math.
- Let `MathTex` or the main diagram carry the visual center.
- Keep alignment crisp across successive steps.
- Avoid long paragraphs on screen.

## Color System

- Use a small palette.
- Keep one semantic meaning per accent color and preserve it across the scene.
- Use neutral scaffolding colors for context and brighter accents for focus.
- Good default roles:
- yellow for current focus
- blue and green for compared objects or cases
- red for contradiction, forbidden cases, cancellation, or warning
- Avoid rainbow coloring and avoid changing a symbol's color meaning mid-scene.

## Emphasis

- Prefer `SurroundingRectangle`, `Brace`, `Arrow`, and local color contrast.
- Use `Circumscribe` and `Indicate` sparingly.
- Use opacity and brightness changes to push old context into the background.
- Highlight only what the viewer should read right now.

## Motion

- Motion should explain structure, not advertise itself.
- Prefer smooth transforms that preserve object identity.
- If two expressions correspond, morph them instead of fading both out and in.
- Keep most motion local.
- Avoid decorative spinning, bouncing, large zooms, and restless camera pans.

## Diagrams And Graphs

- Make scaffolding lighter than the primary object.
- Keep axes, grids, and helper lines visually subordinate.
- Place labels close to the thing they label.
- Use one bright accent for the current moving point or active region.
- Keep graph labels compact and legible.

## Camera

- Default to a static camera.
- Zoom only when a local detail genuinely needs inspection.
- Pan only when the composition no longer fits the frame.
- In proof-style scenes, camera motion should be rare.

## Rhythm

- Introduce one conceptual beat at a time.
- Give the viewer a short pause after each important transformation.
- Do not add many unrelated objects in the same beat.
- Keep frame density low enough that any paused frame still reads clearly.

## Anti-Patterns

- Too many simultaneous accents
- Constant motion with no mathematical purpose
- Large blocks of prose
- Centering everything by default
- Recoloring the same symbol with different meanings
- Heavy grids, thick axes, or over-styled labels that overpower the content
