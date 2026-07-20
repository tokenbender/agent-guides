# Core Workflow

## Mental Model

- `Scene` owns the timeline.
- `Mobject` is visible state on screen.
- `Animation` changes mobject state over time.

In practice:

- `self.add(...)` shows static objects immediately.
- `self.play(...)` renders one animation beat.
- `self.wait(...)` holds the frame long enough to read or think.

## Build Order

1. Create the mobjects.
2. Position them with layout helpers.
3. Style them.
4. Add static context.
5. Animate one conceptual beat at a time.

This usually stays clearer than mixing creation, layout, and motion in the same line.

## Scene Choice

- Use `Scene` by default.
- Use `MovingCameraScene` only for deliberate zoom or pan.
- Use `ThreeDScene` only when 3D structure matters.

## Minimal Template

```python
from manim import *


class MyScene(Scene):
    def construct(self):
        title = Text("Title", font_size=40).to_edge(UP)
        statement = MathTex(r"a^2 + b^2 = c^2").next_to(title, DOWN, buff=0.6)

        self.play(Write(title))
        self.play(Write(statement))
        self.wait()
```

## Animation Defaults

- Use `.animate` for simple property changes.
- Use `Transform` or `ReplacementTransform` when one object becomes another.
- Use `TransformMatchingTex` when equation parts should visually track across steps.
- Keep most `run_time` values between `0.5` and `2` seconds.

## Render Workflow

```bash
manim -pql scene.py MyScene
manim -sql scene.py MyScene
manim -pqm scene.py MyScene
```

- Iterate at low quality.
- Use last-frame renders to debug layout.
- Only switch to higher quality once the scene logic works.

## Pitfalls

- Do not expect bare `Mobject()` instances to render meaningfully.
- Screen coordinates are centered at the origin, not at the top left.
- Draw order matters: later-added objects appear on top.
- Updaters keep running during waits and later animations until removed.
