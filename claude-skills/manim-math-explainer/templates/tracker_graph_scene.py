from manim import *


class TrackerGraphBeat(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=5,
        )
        graph = axes.plot(lambda x: x**2 / 2 + 1, color=BLUE)
        label = axes.get_graph_label(graph, MathTex(r"f(x) = x^2/2 + 1"), x_val=1.4)

        x_tracker = ValueTracker(-2)
        dot = always_redraw(
            lambda: Dot(axes.i2gp(x_tracker.get_value(), graph), color=YELLOW)
        )
        value = always_redraw(
            lambda: (
                DecimalNumber(x_tracker.get_value(), num_decimal_places=2)
                .scale(0.7)
                .to_corner(UR)
            )
        )

        self.play(Create(axes))
        self.play(Create(graph), FadeIn(label))
        self.add(dot, value)
        self.play(x_tracker.animate.set_value(2), run_time=3, rate_func=linear)
        self.wait()
