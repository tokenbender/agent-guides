from manim import *


class BasicMathBeat(Scene):
    def construct(self):
        title = Text("Claim", font_size=40).to_edge(UP)
        statement = MathTex(r"a^2 + b^2 = c^2").next_to(title, DOWN, buff=0.6)
        focus_box = SurroundingRectangle(statement, color=YELLOW, buff=0.2)

        self.play(Write(title))
        self.play(Write(statement))
        self.play(Create(focus_box))
        self.wait()


class MatchingTexBeat(Scene):
    def construct(self):
        expr1 = MathTex(r"x^2 - 1", substrings_to_isolate=["x", "1"])
        expr2 = MathTex(r"(x-1)(x+1)", substrings_to_isolate=["x", "1"])

        self.play(Write(expr1))
        self.play(TransformMatchingTex(expr1, expr2))
        self.play(Circumscribe(expr2, color=YELLOW))
        self.wait()
