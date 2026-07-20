# Dynamics And Graphing

## Dynamic Parameters

Use `ValueTracker` when a number drives geometry or text.

```python
tracker = ValueTracker(0)
number = always_redraw(lambda: DecimalNumber(tracker.get_value()))

self.add(number)
self.play(tracker.animate.set_value(5))
```

## Updater Choice

- Use `always_redraw(...)` when a mobject is naturally rebuilt from current state.
- Use `add_updater(...)` when only one property needs to follow another object.
- Clear updaters when the relationship is no longer needed.

## Graphing Defaults

- Use `Axes` for function plots.
- Use `NumberPlane` when the grid itself teaches something.
- Use `c2p(...)` for coordinate conversion.
- Use `i2gp(...)` for points tied to a plotted graph.

## Plot Pattern

```python
axes = Axes(x_range=[-3, 3, 1], y_range=[-2, 4, 1])
graph = axes.plot(lambda x: x**2, color=BLUE)
label = axes.get_graph_label(graph, MathTex(r"y=x^2"), x_val=1.5)

self.play(Create(axes))
self.play(Create(graph), FadeIn(label))
```

## Moving Point Pattern

```python
x = ValueTracker(-2)
dot = always_redraw(lambda: Dot(axes.i2gp(x.get_value(), graph), color=YELLOW))

self.add(dot)
self.play(x.animate.set_value(2), run_time=3, rate_func=linear)
```

## Camera Guidance

- Stay in `Scene` unless zoom or pan carries meaning.
- Use `MovingCameraScene` for local inspection.
- Use `ThreeDScene` only when a genuinely 3D object or surface is the concept.

## Pitfalls

- Too many updaters can make renders harder to reason about.
- Undefined or discontinuous functions need careful `x_range` choices.
- A moving dot without a visual cue for the underlying graph often feels arbitrary.
