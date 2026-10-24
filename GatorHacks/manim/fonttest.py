from manim import *


class F(Scene):
    def construct(self):
        self.camera.background_color = ManimColor("#FFFFFF")
        with register_font(r"C:\Users\jaron\OneDrive\Documents\GitHub\Workshop-1\GatorHacks\manim\fonts\Jost-Variable.ttf"):
            rows = []
            for name, w in [("NORMAL", NORMAL), ("BOOK", "BOOK"), ("MEDIUM", "MEDIUM"), ("SEMIBOLD", "SEMIBOLD"), ("BOLD", BOLD)]:
                try:
                    rows.append(Text(f"{name}: Agents 101 hackathon", font="Jost", font_size=40, color=BLACK, weight=w))
                except Exception as e:
                    rows.append(Text(f"{name} failed", font_size=30, color=RED))
            g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            self.add(g)
