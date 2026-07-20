# Proof Layouts

This skill is tuned for mathematical explainer scenes, not flashy motion-first reels.

## Layout Principles

- Put the main claim near the top or center and keep it anchored.
- Keep supporting objects close to the statement they explain.
- Reuse stable positions so the viewer does not need to reparse the screen.
- Use one color per semantic role and keep that mapping fixed.

Example role mapping:

- yellow: current focus
- blue: first object or set
- green: second object or set
- red: contradiction, forbidden case, or error term

## Preferred Emphasis

- `SurroundingRectangle` for the current line or equation part
- `Brace` for grouped terms or grouped cases
- `Arrow` for implication or dependence
- `Indicate` and `Circumscribe` for quick attention, not for every beat

## Good Motion

- Move objects only when the movement itself explains the math.
- Prefer transforms that preserve identity.
- Use `TransformMatchingTex` when algebraic parts correspond across steps.
- Use `FadeIn` and `FadeOut` for context that appears or leaves without correspondence.

## Bad Motion

- Large camera moves in a proof scene with only a few objects
- Decorative spinning, bouncing, or scaling with no mathematical meaning
- Rebuilding the entire screen every step when a targeted transform would do

## Useful Math Patterns

- Small finite families: `VGroup(...).arrange(...)`
- Case splits: two columns with shared title and equal vertical rhythm
- Graph theory objects: `Graph` for small graphs, `LabeledDot` or `MathTex` labels where needed
- Counting tables: `MathTable` or `MobjectTable` for compact comparisons

## Example

```python
line1 = MathTex(r"|A \cup B| = |A| + |B| - |A \cap B|")
line2 = MathTex(r"|A \cup B| = m + n - t")

self.play(Write(line1))
self.play(TransformMatchingTex(line1, line2))
self.play(Circumscribe(line2[-1], color=YELLOW))
```
