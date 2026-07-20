# Text And Math

## Choose The Right Class

- Use `Text` for ordinary prose.
- Use `MarkupText` when one prose block needs mixed styling.
- Use `MathTex` for formulas.
- Use `Tex` only when you intentionally mix prose and LaTeX in one object.

## TeX Rules

- Use raw strings: `r"..."`.
- Split equations into parts when you plan to animate or recolor those parts.
- Use `substrings_to_isolate` when repeated substrings must be matched reliably.

## Reliable Formula Animation

```python
expr1 = MathTex(
    r"x^2 - 1",
    substrings_to_isolate=["x", "1"],
)
expr2 = MathTex(
    r"(x-1)(x+1)",
    substrings_to_isolate=["x", "1"],
)

self.play(TransformMatchingTex(expr1, expr2))
```

## Debugging Formula Parts

Use `index_labels(...)` when part boundaries are unclear.

```python
expr = MathTex(r"\frac{a+b}{c}")
self.add(index_labels(expr[0]), expr)
```

## Coloring Guidance

- Prefer semantic coloring, not rainbow coloring.
- Color the same symbol the same way across the scene.
- If `set_color_by_tex(...)` misses a target, isolate substrings first.

## Text Pitfalls

- System fonts must actually be installed for `Text`.
- Character-level coloring in `Text` can interact badly with ligatures.
- If character slicing behaves oddly, use `MarkupText` or disable ligatures.

## Extra Packages

If a formula needs non-default LaTeX packages, create a `TexTemplate` and add the package to its preamble instead of forcing strange workarounds.
