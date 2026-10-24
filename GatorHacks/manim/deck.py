"""Agents 101, Gator Hack V edition. One Slide subclass per slide (S01 to S18).

Look and feel follows ufgatorhack.com: paper white, UF blue and orange, Jost type,
square corners with thin blue borders, and a hard orange-tint "paper" shadow.
Render with render.ps1, present with present.bat.
"""
import json
import textwrap
from pathlib import Path

import numpy as np
from manim import *
from manim_slides import Slide

HERE = Path(__file__).parent
NOTES = json.load(open(HERE / "notes.json", encoding="utf-8"))
_JOST = register_font(str(HERE / "fonts" / "Jost-Variable.ttf"))  # keep a reference or the font is unregistered
_JOST.__enter__()

# ---------------------------------------------------------------- design tokens
PAPER = "#FFFFFF"
BLUE = "#0021A5"          # UF blue
ORANGE = "#FA4616"        # UF orange
INK = "#33418F"           # site body text
SOFT = "#6F7BB8"          # secondary text
TINT = "#FDD9CD"          # orange tint (shadows)
WASH_O = "#FEF0EB"
WASH_B = "#EEF1FB"
EDGE = "#C9D0EE"          # quiet hairlines
GOOD = "#16A34A"
WARN = "#E0A100"
WARN_TXT = "#B45309"
BAD = "#DC2626"
GOOD_BG, WARN_BG, BAD_BG = "#E8F7EE", "#FFF6DB", "#FDECEC"
MONO = "Consolas"
TOTAL = 20
LM = -6.4                 # left margin of all content
AIRBNB = "Diagram adapted from a talk by Airbnb senior staff engineers"


def T(s, size=26, color=INK, w="MEDIUM", font="Jost", **kw):
    return Text(s, font=font, font_size=size, color=color, weight=w, **kw)


def M(s, size=22, color=BLUE, **kw):
    return Text(s, font=MONO, font_size=size, color=color, weight="NORMAL", **kw)


def para(s, size=24, color=INK, width=26, **kw):
    return T(textwrap.fill(s, width), size, color, line_spacing=0.95, **kw)


def box(w, h, stroke=BLUE, fill=PAPER, sw=2.2, r=0.05):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=stroke, stroke_width=sw,
                            fill_color=fill, fill_opacity=1)


def card(title, body, accent, w, h, tsize=32, bsize=24, wrap=21):
    """Bordered card with a colored cap and a paper shadow. Text is anchored at the top-left."""
    b = box(w, h)
    sh = Rectangle(width=w, height=h, stroke_width=0, fill_color=TINT, fill_opacity=1).shift(RIGHT * 0.1 + DOWN * 0.1)
    cap = Rectangle(width=w, height=0.16, stroke_width=0, fill_color=accent, fill_opacity=1)
    cap.align_to(b, UP).align_to(b, LEFT)
    t = T(title, tsize, BLUE, "BOLD").move_to(b.get_corner(UL) + np.array([0.4, -0.55, 0]), aligned_edge=UL)
    parts = [sh, b, cap, t]
    if body:
        parts.append(para(body, bsize, INK, wrap).next_to(t, DOWN, buff=0.3, aligned_edge=LEFT))
    return VGroup(*parts)


def pill(label, stroke, fill, minw=1.6, h=0.7, size=24, color=BLUE, w="SEMIBOLD", r=0.06):
    t = T(label, size, color, w)
    b = box(max(minw, t.width + 0.7), h, stroke, fill, 2.2, r)
    t.move_to(b)
    return VGroup(b, t)


def padlock(color, k=1.0):
    body = RoundedRectangle(corner_radius=0.03, width=0.28 * k, height=0.21 * k, stroke_width=0, fill_color=color, fill_opacity=1)
    arch = Arc(radius=0.085 * k, start_angle=0, angle=PI, stroke_width=3.2 * k, stroke_color=color)
    arch.next_to(body, UP, buff=-0.01 * k)
    return VGroup(arch, body)


def dimmed(m, f):
    """Return an animation that fades every part of `m` to a fraction of its opacity."""
    tgt = m.copy()
    for sub in tgt.family_members_with_points():
        sub.set_fill(opacity=sub.get_fill_opacity() * f)
        sub.set_stroke(opacity=sub.get_stroke_opacity() * f)
    return Transform(m, tgt)


def facets(corner=1.0):
    """Little origami triangles, echoing the Gator Hack logo."""
    s = corner
    tri = lambda pts, col, op: Polygon(*[[x * s, y, 0] for x, y in pts], stroke_width=0, fill_color=col, fill_opacity=op)
    return VGroup(
        tri([(7.1, -3.2), (7.1, -2.2), (5.9, -3.2)], TINT, 0.9),
        tri([(7.1, -3.2), (7.1, -2.7), (6.5, -3.2)], ORANGE, 0.55),
        tri([(-7.1, -3.2), (-7.1, -2.5), (-6.2, -3.2)], WASH_B, 1.0),
    )


class Deck(Slide):
    n = 0
    title = None
    credit = None
    hero = False

    def chrome(self):
        g = Group()
        band_l = Rectangle(width=14.2 - 3.4, height=0.12, stroke_width=0, fill_color=BLUE, fill_opacity=1)
        band_l.move_to([-7.1 + band_l.width / 2, -3.94, 0])
        band_r = Rectangle(width=3.4, height=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1)
        band_r.move_to([7.1 - 1.7, -3.94, 0])
        g.add(band_l, band_r)
        foot = self.credit or "Gator Hack V   ·   UF AI Days 2026"
        g.add(T(foot, 16, SOFT).move_to([LM, -3.62, 0], aligned_edge=LEFT))
        g.add(T(f"{self.n} / {TOTAL}", 16, SOFT).move_to([6.4, -3.62, 0], aligned_edge=RIGHT))
        if not self.hero:
            logo = ImageMobject(str(HERE / "assets" / "logo.png")).scale_to_fit_height(0.7)
            logo.move_to([6.3, 3.45, 0])
            g.add(logo)
        return g

    def prep(self):
        self.camera.background_color = ManimColor(PAPER)
        if not self.hero:
            self.add(facets())
        self.add(self.chrome())
        self.next_slide(notes=NOTES[type(self).__name__])
        if self.title:
            t = T(self.title, 54, BLUE, "BOLD").move_to([LM, 3.62, 0], aligned_edge=UL)
            bar = Rectangle(width=0.9, height=0.09, stroke_width=0, fill_color=ORANGE, fill_opacity=1)
            bar.move_to([LM, 2.78, 0], aligned_edge=LEFT)
            self.play(FadeIn(t, shift=UP * 0.15), GrowFromEdge(bar, LEFT), run_time=0.5)

    def takeaway(self, text, color=BLUE, y=-2.7, size=30):
        mark = Square(0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([LM + 0.1, y, 0])
        t = T(text, size, color, "SEMIBOLD").move_to([LM + 0.5, y, 0], aligned_edge=LEFT)
        return VGroup(mark, t)

    def intro(self, text):
        return T(text, 26, INK).move_to([LM, 2.15, 0], aligned_edge=LEFT)

    def show(self, *mobs, shift=UP * 0.25, run_time=0.6, lag=0.0):
        self.play(LaggedStart(*[FadeIn(m, shift=shift) for m in mobs], lag_ratio=lag), run_time=run_time)


# ---------------------------------------------------------------- the loop diagram
class Loop:
    """Both loops, built on one grid. Looked up by name so slides can reveal and dim parts."""

    def __init__(self):
        self.m = {}
        ROW1, ROW2 = 0.72, -1.25
        dev = box(5.1, 4.3, ORANGE, "#FFF9F6", 2.0, 0.08).move_to([-4.1, -0.05, 0])
        dev_l = T("DEVELOPER LOOP", 19, BLUE, "BOLD").move_to(dev.get_corner(UL) + np.array([0.35, -0.38, 0]), aligned_edge=UL)
        dev_s = T("you", 18, ORANGE, "SEMIBOLD").next_to(dev_l, DOWN, buff=0.1, aligned_edge=LEFT)
        ell = DashedVMobject(Ellipse(width=6.9, height=4.5, color=BLUE, stroke_width=2.2).move_to([3.1, -0.05, 0]),
                             num_dashes=72)
        ag_l = T("AGENTIC AI LOOP", 19, BLUE, "BOLD").move_to([3.1, 1.95, 0])
        ag_s = T("the agent", 18, BLUE, "SEMIBOLD").next_to(ag_l, DOWN, buff=0.08)
        self.m["dev_region"] = VGroup(dev, dev_l, dev_s)
        self.m["agent_region"] = VGroup(ell, ag_l, ag_s)

        def node(name, label, x, y, w, kind):
            if kind == "you":
                p = pill(label, ORANGE, WASH_O, w, 0.7, 22)
            elif kind == "agent":
                p = pill(label, BLUE, WASH_B, w, 0.7, 22)
            else:
                p = pill(label, ORANGE, ORANGE, w, 0.7, 22, PAPER, r=0.35)
            p.move_to([x, y, 0])
            self.m[name] = p

        node("spec", "Feature spec", -5.35, ROW1, 1.95, "you")
        node("prompt", "Prompt", -2.85, ROW1, 1.6, "you")
        node("review", "Review", -2.85, ROW2, 1.6, "you")
        node("pr", "PR", -5.35, ROW2, 1.3, "pr")
        node("llm", "LLM", 1.7, ROW1, 1.5, "agent")
        node("env", "Environment", 4.5, ROW1, 2.1, "agent")
        node("config", "Config", 1.7, ROW2, 1.5, "you")
        node("guard", "Guardrails", 4.5, ROW2, 2.1, "you")

        def A(a, b, color=SOFT, dashed=False):
            if dashed:
                ln = DashedLine(a, b, dash_length=0.14, stroke_width=3, color=color)
                ln.add_tip(tip_length=0.2)
                return ln
            return Arrow(a, b, buff=0, stroke_width=3, color=color, tip_length=0.2, max_tip_length_to_length_ratio=1)

        def lab(text, x, y):
            return T(text, 20, SOFT, "MEDIUM").move_to([x, y, 0])

        E = self.m
        E["e_spec"] = A([-4.37, ROW1, 0], [-3.67, ROW1, 0])
        E["e_hand"] = A([-2.03, ROW1, 0], [0.93, ROW1, 0], ORANGE)
        E["l_hand"] = lab("hand off", -0.95, 1.07)
        E["e_load"] = A([1.7, ROW2 + 0.38, 0], [1.7, ROW1 - 0.38, 0])
        E["l_load"] = lab("load", 2.2, -0.3)
        E["e_use"] = A([2.47, ROW1, 0], [3.43, ROW1, 0])
        E["l_use"] = lab("use", 2.95, 1.07)
        E["e_enf"] = A([4.5, ROW1 - 0.38, 0], [4.5, ROW2 + 0.38, 0])
        E["l_enf"] = lab("enforce", 5.25, -0.3)
        E["e_chk"] = A([3.85, ROW2 + 0.38, 0], [2.45, ROW1 - 0.38, 0])
        E["l_chk"] = lab("check", 3.62, -0.05)
        E["e_out"] = A([0.2, ROW2, 0], [-2.03, ROW2, 0], dashed=True)
        E["l_out"] = lab("AI outputs", -0.75, -1.62)
        E["e_cc"] = A([-2.85, ROW2 + 0.38, 0], [-2.85, ROW1 - 0.38, 0])
        E["l_cc"] = lab("course correct", -4.0, -0.3)
        E["e_pr"] = A([-3.67, ROW2, 0], [-4.68, ROW2, 0])

        self.groups = {
            "dev": ["dev_region", "spec", "prompt", "e_spec"],
            "agent": ["agent_region", "e_hand", "l_hand", "llm", "env", "config", "guard", "e_load", "l_load",
                      "e_use", "l_use", "e_enf", "l_enf", "e_chk", "l_chk"],
            "out": ["e_out", "l_out", "review", "e_cc", "l_cc", "pr", "e_pr"],
        }

    def group(self, key):
        return VGroup(*[self.m[k] for k in self.groups[key]])

    def all(self):
        return VGroup(*self.m.values())

    def focus(self, names, f=0.2):
        return [dimmed(v, f) for k, v in self.m.items() if k not in names]


# ================================================================= 01 title
class S01(Deck):
    n = 1
    hero = True

    def construct(self):
        self.prep()
        self.add(facets(1.0))
        logo = ImageMobject(str(HERE / "assets" / "logo.png")).scale_to_fit_height(2.7).move_to([4.5, 0.6, 0])
        bar = Rectangle(width=1.4, height=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1)
        bar.move_to([LM, 2.75, 0], aligned_edge=LEFT)
        tag = T("Gator Hack V   ·   UF AI Days 2026", 24, ORANGE, "SEMIBOLD").move_to([LM, 2.2, 0], aligned_edge=LEFT)
        t = T("Agents 101", 104, BLUE, "BOLD").move_to([LM, 0.8, 0], aligned_edge=LEFT)
        sub = T("How to actually work with", 38, INK, "MEDIUM").move_to([LM, -0.65, 0], aligned_edge=LEFT)
        sub2 = T("AI coding agents", 38, INK, "MEDIUM").next_to(sub, DOWN, buff=0.12, aligned_edge=LEFT)
        rule = Line([LM, -1.85, 0], [LM + 5.2, -1.85, 0], stroke_color=EDGE, stroke_width=2)
        by = T("Presented by", 20, SOFT, "MEDIUM").move_to([LM, -2.2, 0], aligned_edge=LEFT)
        who = T("Nedas Jaronis", 36, BLUE, "BOLD").move_to([LM, -2.65, 0], aligned_edge=LEFT)
        club = T("AI2 Club", 26, ORANGE, "SEMIBOLD").next_to(who, RIGHT, buff=0.35, aligned_edge=DOWN)
        self.add(logo)
        self.play(GrowFromEdge(bar, LEFT), FadeIn(tag), run_time=0.5)
        self.play(FadeIn(t, shift=UP * 0.3), run_time=0.9)
        self.play(FadeIn(sub, shift=UP * 0.2), FadeIn(sub2, shift=UP * 0.2), run_time=0.6)
        self.play(Create(rule), FadeIn(by), FadeIn(who), FadeIn(club), run_time=0.7)
        self.wait(0.5)


# ================================================================= 02 two loops
class S02(Deck):
    n = 2
    title = "The two loops"
    credit = AIRBNB

    def construct(self):
        self.prep()
        L = Loop()
        L.all().scale(0.88, about_point=ORIGIN).shift(UP * 0.2)
        self.play(FadeIn(L.group("dev"), lag_ratio=0.1), run_time=1.0)
        self.next_slide()
        self.play(FadeIn(L.group("agent"), lag_ratio=0.05), run_time=1.6)
        self.next_slide()
        self.play(FadeIn(L.group("out"), lag_ratio=0.1), run_time=1.2)
        legend = T("LLM = the AI model     Config = standing instructions     PR = a proposed code change", 20, SOFT)
        legend.move_to([0, -2.1, 0])
        take = self.takeaway("You control what goes in and what comes out. The agent runs the middle.", y=-2.65, size=28)
        self.next_slide()
        self.play(FadeIn(legend), FadeIn(take, shift=UP * 0.2), run_time=0.7)


# ================================================================= 03 lifecycle
class S03(Deck):
    n = 3
    title = "The lifecycle is shifting"

    def construct(self):
        self.prep()
        X0 = -4.3

        def row(labels, y, special=None):
            items = []
            for i, lab in enumerate(labels):
                if special == i:
                    p = pill(lab, BLUE, WASH_B, 3.4, 0.95, 26)
                    p[1].shift(UP * 0.14)
                    p = VGroup(p, T("the agent loop", 18, BLUE, "SEMIBOLD").move_to(p[0]).shift(DOWN * 0.22))
                else:
                    p = pill(lab, ORANGE, WASH_O, 1.7, 0.95, 26)
                items.append(p)
            g = VGroup(*items).arrange(RIGHT, buff=0.55).move_to([X0, y, 0], aligned_edge=LEFT)
            arrows = VGroup(*[Arrow(items[i].get_right(), items[i + 1].get_left(), buff=0.06, stroke_width=3,
                                    color=SOFT, tip_length=0.16, max_tip_length_to_length_ratio=1)
                              for i in range(len(items) - 1)])
            return g, arrows

        r1, a1 = row(["Plan", "Build", "Test", "Review", "Ship"], 1.2)
        tag1 = T("BEFORE", 22, SOFT, "BOLD").move_to([LM, 1.2, 0], aligned_edge=LEFT)
        n1 = T("You did every step.", 24, SOFT).move_to([X0, 0.35, 0], aligned_edge=LEFT)
        r2, a2 = row(["Plan", "Build + Test", "Review", "Ship"], -0.95, special=1)
        tag2 = T("NOW", 22, ORANGE, "BOLD").move_to([LM, -0.95, 0], aligned_edge=LEFT)
        n2 = T("The agent does the middle.", 24, SOFT).move_to([X0, -1.85, 0], aligned_edge=LEFT)
        take = self.takeaway("Your time moves to planning and reviewing.")

        self.add(self.intro("The software development lifecycle: the steps every feature goes through."))
        self.play(FadeIn(tag1), LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in r1], lag_ratio=0.15), run_time=1.0)
        self.play(Create(a1), FadeIn(n1), run_time=0.7)
        self.next_slide()
        self.play(dimmed(r1, 0.35), dimmed(a1, 0.35), dimmed(tag1, 0.35), dimmed(n1, 0.35), run_time=0.5)
        self.play(FadeIn(tag2), LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in r2], lag_ratio=0.15), run_time=1.0)
        self.play(Create(a2), FadeIn(n2), run_time=0.7)
        self.next_slide()
        self.play(FadeIn(take, shift=UP * 0.2), run_time=0.6)


# ================================================================= 04 context window
class S04(Deck):
    n = 4
    title = "What is in the context window"

    def construct(self):
        self.prep()
        w, h = 4.15, 3.1
        cs = [card("Instructions", "System prompt, rules file (CLAUDE.md), skills", BLUE, w, h),
              card("What it read", "Files and tool output", BLUE, w, h),
              card("The conversation", "Everything you and the agent said", BLUE, w, h)]
        VGroup(*cs).arrange(RIGHT, buff=0.25).move_to([0, -0.1, 0])
        self.add(self.intro("The context window is everything the agent can see at one time."))
        self.show(*cs, run_time=1.2, lag=0.25)
        q = self.takeaway("The agent only knows what is in its context.")
        self.next_slide()
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.7)


# ================================================================= 05 dumb zone
class S05(Deck):
    n = 5
    title = "The dumb zone"

    def construct(self):
        self.prep()
        W, H, x0, y0, N = 11.6, 0.8, -5.8, 0.4, 90
        gcol = [ManimColor(GOOD), ManimColor(WARN), ManimColor(BAD)]

        def col(f):
            if f < 0.38:
                return gcol[0]
            if f < 0.55:
                return interpolate_color(gcol[0], gcol[1], (f - 0.38) / 0.17)
            if f < 0.8:
                return interpolate_color(gcol[1], gcol[2], (f - 0.55) / 0.25)
            return gcol[2]

        track = box(W + 0.12, H + 0.12, BLUE, WASH_B, 2.4, 0.06).move_to([0, y0, 0])
        segs = VGroup(*[Rectangle(width=W / N + 0.012, height=H, stroke_width=0, fill_color=col(i / N),
                                  fill_opacity=1).move_to([x0 + (i + 0.5) * W / N, y0, 0]) for i in range(N)])
        mk = lambda f: DashedLine([x0 + f * W, y0 + 0.62, 0], [x0 + f * W, y0 - 0.62, 0], color=BLUE, stroke_width=3,
                                  dash_length=0.1)
        names = VGroup(T("Smart zone", 28, GOOD, "BOLD").move_to([x0 + 0.2 * W, y0 - 1.0, 0]),
                       T("Slipping", 28, WARN_TXT, "BOLD").move_to([x0 + 0.55 * W, y0 - 1.0, 0]),
                       T("Dumb zone", 28, BAD, "BOLD").move_to([x0 + 0.85 * W, y0 - 1.0, 0]))
        ticks = VGroup(*[T(t, 20, SOFT).move_to([x0 + f * W, y0 - 1.55, 0]) for t, f in
                         (("0%", 0.0), ("40%", 0.4), ("70%", 0.7), ("100%", 1.0))])
        ticks[0].shift(RIGHT * 0.18)
        ticks[3].shift(LEFT * 0.3)
        take = self.takeaway("Quality starts to slip around 40% full and falls off fast past 70%.", size=28)

        self.add(self.intro("The fuller the window gets, the worse the agent performs."))
        self.play(FadeIn(track), FadeIn(ticks), run_time=0.6)
        self.next_slide()
        self.play(LaggedStart(*[FadeIn(s) for s in segs], lag_ratio=0.05), run_time=5.5, rate_func=linear)
        self.play(Create(mk(0.4)), Create(mk(0.7)), run_time=0.5)
        self.play(FadeIn(names, shift=UP * 0.15), run_time=0.6)
        self.next_slide()
        self.play(FadeIn(take, shift=UP * 0.2), run_time=0.6)


# ================================================================= 06 session timeline
class S06(Deck):
    n = 6
    title = "How a session grows and shrinks"

    def construct(self):
        self.prep()
        pts = [
            (6, "New session", "A new session starts",
             "Only the system prompt and your config files are loaded. The window is almost empty.", False),
            (22, "Read files", "Reading files fills the window",
             "Every file the agent opens is copied into its context. It stays until the session ends.", False),
            (46, "Tool output", "Tool output piles up",
             "Test logs, search results and shell output all add up. Quality starts to slip past 40%.", False),
            (14, "/compact", "/compact summarizes the history",
             "Long history is replaced by a short summary. Space comes back, but details are lost.", True),
            (32, "Keep working", "Work continues on the summary",
             "The window grows again. Anything the summary left out is gone, so old mistakes can return.", False),
            (5, "/clear", "/clear starts fresh from a file",
             "You write a plan or handoff file, clear the window, and the next session reads only that file.", True),
        ]
        xl, xr, y0, y1 = -4.8, 5.6, -0.7, 1.7
        Y = lambda p: y0 + (y1 - y0) * p / 100
        X = lambda i: xl + (xr - xl) * i / (len(pts) - 1)
        zc = lambda p: GOOD if p < 40 else (WARN if p < 70 else BAD)
        L, R = -5.5, 6.4
        band = lambda a, b, c: Rectangle(width=R - L, height=Y(b) - Y(a), stroke_width=0, fill_color=c,
                                         fill_opacity=1).move_to([(L + R) / 2, (Y(a) + Y(b)) / 2, 0])
        bands = VGroup(band(0, 40, GOOD_BG), band(40, 70, WARN_BG), band(70, 100, BAD_BG))
        frame = Rectangle(width=R - L, height=Y(100) - Y(0), stroke_color=BLUE, stroke_width=2.2, fill_opacity=0
                          ).move_to([(L + R) / 2, (Y(0) + Y(100)) / 2, 0])
        guides = VGroup(*[DashedLine([L, Y(v), 0], [R, Y(v), 0], stroke_width=1.6, color=SOFT, dash_length=0.12)
                          for v in (40, 70)])
        ylabs = VGroup(*[T(f"{v}%", 19, SOFT).move_to([L - 0.4, Y(v), 0], aligned_edge=RIGHT) for v in (0, 40, 70, 100)])
        zl = VGroup(T("Smart zone", 20, GOOD, "BOLD").move_to([L + 0.2, Y(32), 0], aligned_edge=LEFT),
                    T("Slipping", 20, WARN_TXT, "BOLD").move_to([L + 0.2, Y(55), 0], aligned_edge=LEFT),
                    T("Dumb zone", 20, BAD, "BOLD").move_to([L + 0.2, Y(85), 0], aligned_edge=LEFT))
        top_lab = T("How full the context window is", 20, SOFT).move_to([L, Y(100) + 0.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(bands), FadeIn(frame), FadeIn(guides), FadeIn(ylabs), FadeIn(zl), FadeIn(top_lab), run_time=0.8)

        def caption(i):
            _, _, ct, cb, _ = pts[i]
            b = box(R - L, 1.35, BLUE, PAPER, 2.2, 0.05).move_to([(L + R) / 2, -2.3, 0])
            a = T(ct, 30, BLUE, "BOLD").move_to(b.get_corner(UL) + np.array([0.35, -0.25, 0]), aligned_edge=UL)
            c = T(cb, 21, INK).next_to(a, DOWN, buff=0.14, aligned_edge=LEFT)
            return VGroup(b, a, c)

        prev, cap = None, None
        for i, (p, lab, ct, cb, drop) in enumerate(pts):
            d = Dot([X(i), Y(p), 0], radius=0.13, color=zc(p))
            ring = Circle(radius=0.2, stroke_color=PAPER, stroke_width=3, fill_opacity=0).move_to(d)
            lb = (M(lab, 20, BLUE) if drop else T(lab, 21, INK, "SEMIBOLD")).move_to([X(i), y0 - 0.4, 0])
            c = caption(i)
            anims = []
            if prev is not None:
                seg = DashedLine(prev.get_center(), d.get_center(), color=GOOD, stroke_width=5, dash_length=0.1) if drop \
                    else Line(prev.get_center(), d.get_center(), color=BLUE, stroke_width=5)
                anims.append(Create(seg))
            anims += [GrowFromCenter(VGroup(ring, d)), FadeIn(lb)]
            if cap is None:
                self.play(*anims, FadeIn(c), run_time=0.8)
            else:
                self.next_slide()
                self.play(*anims, FadeOut(cap), FadeIn(c), run_time=0.9)
            if drop:
                self.play(Flash(d, color=GOOD, flash_radius=0.45, line_length=0.15), run_time=0.5)
            cap, prev = c, d


# ================================================================= 07 smart zone
class S07(Deck):
    n = 7
    title = "Staying in the smart zone"

    def construct(self):
        self.prep()
        w, h = 4.15, 3.1
        cs = [card("Fresh sessions", "New task, new session. Clear the old one.", GOOD, w, h, 26),
              card("Compact on purpose", "Summarize the work into a plan file, then restart from it.", GOOD, w, h, 26),
              card("Sub-agents", "Push heavy exploration to a separate window.", GOOD, w, h, 26)]
        VGroup(*cs).arrange(RIGHT, buff=0.25).move_to([0, 0.0, 0])
        self.play(FadeIn(cs[0], shift=UP * 0.25), run_time=0.7)
        for c in cs[1:]:
            self.next_slide()
            self.play(FadeIn(c, shift=UP * 0.25), run_time=0.7)


# ================================================================= 08 skill
class S08(Deck):
    n = 8
    title = "What is a skill"

    def construct(self):
        self.prep()
        lines = [("---", SOFT), ("name: grill-me", INK),
                 ("description: Interview me about a plan until every branch is resolved.", INK),
                 ("---", SOFT), ("# Grill me", ORANGE), ("1. Ask one question at a time.", INK),
                 ("2. Offer your recommended answer.", INK), ("3. Stop when no open branches remain.", INK)]
        ts = VGroup(*[M(s, 20, c) for s, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        panel = box(ts.width + 1.0, ts.height + 0.7, BLUE, WASH_B, 2.2, 0.05).move_to([0, -0.2, 0])
        ts.move_to(panel)
        shadow = Rectangle(width=panel.width, height=panel.height, stroke_width=0, fill_color=TINT,
                           fill_opacity=1).move_to(panel).shift(RIGHT * 0.1 + DOWN * 0.1)
        file_lbl = M("SKILL.md", 20, SOFT).next_to(panel, UP, buff=0.12, aligned_edge=LEFT)
        hl = Rectangle(width=ts.width + 0.3, height=0.46, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                       fill_opacity=0.15).move_to(ts[2])
        take = self.takeaway("Only the short description sits in context. The body loads when needed.", size=27)

        self.add(self.intro("A skill is a short how-to file the agent loads for one kind of task."))
        self.play(FadeIn(shadow), FadeIn(panel), FadeIn(file_lbl), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in ts], lag_ratio=0.12), run_time=1.6)
        self.next_slide()
        self.play(Create(hl), *[ts[i].animate.set_opacity(0.3) for i in (0, 1, 3, 4, 5, 6, 7)], run_time=0.7)
        self.next_slide()
        self.play(FadeIn(take, shift=UP * 0.2), run_time=0.6)


# ================================================================= 09 Matt Pocock skills
class S09(Deck):
    n = 9
    title = "Matt Pocock's skills"
    credit = "github.com/mattpocock/skills"

    def construct(self):
        self.prep()
        cmd_t = M("claude plugin install mattpocock-skills@claude-plugins-official", 23, PAPER)
        cmd = box(cmd_t.width + 0.9, 0.7, BLUE, BLUE, 2.2, 0.05).move_to([0, 2.05, 0])
        cmd_t.move_to(cmd)
        groups = [
            ("Before coding", "Feeds the Prompt arrow",
             [("grill-me", "Quizzes you on your idea"),
              ("to-spec", "Turns the chat into a spec"),
              ("to-tickets", "Splits the spec into tasks")]),
            ("While coding", "Strengthens Guardrails",
             [("tdd", "Test-driven development: write the test first"),
              ("diagnosing-bugs", "A step-by-step way to find hard bugs")]),
            ("After coding", "Powers the Review step",
             [("code-review", "Checks changes against your spec")]),
        ]
        shells = [card(head, "", ORANGE, 4.15, 4.1, 30) for head, _, _ in groups]
        VGroup(*shells).arrange(RIGHT, buff=0.25).move_to([0, -0.5, 0])
        cards = []
        for shell, (head, sub, entries) in zip(shells, groups):
            subt = T(sub, 20, ORANGE, "SEMIBOLD").next_to(shell[3], DOWN, buff=0.08, aligned_edge=LEFT)
            rows = []
            for name, meaning in entries:
                nm = M(name, 22, BLUE)
                ds = para(meaning, 20, INK, 28).next_to(nm, DOWN, buff=0.04, aligned_edge=LEFT)
                rows.append(VGroup(nm, ds))
            col = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            col.next_to(subt, DOWN, buff=0.22, aligned_edge=LEFT)
            cards.append(VGroup(shell, subt, col))
        self.play(FadeIn(cmd, shift=DOWN * 0.15), FadeIn(cmd_t, shift=DOWN * 0.15), run_time=0.7)
        for c in cards:
            self.next_slide()
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.7)


# ================================================================= 10 demo
class S10(Deck):
    n = 10
    hero = True

    def construct(self):
        self.prep()
        self.add(facets(1.0))
        d = T("DEMO", 150, BLUE, "BOLD").move_to([0, 0.5, 0])
        s = T("Live: grill-me on a project idea", 40, INK, "MEDIUM").next_to(d, DOWN, buff=0.45)
        bar = Rectangle(width=1.6, height=0.14, stroke_width=0, fill_color=ORANGE, fill_opacity=1).next_to(d, UP, buff=0.5)
        self.play(GrowFromCenter(bar), FadeIn(d, scale=0.92), run_time=0.8)
        self.play(FadeIn(s, shift=UP * 0.2), run_time=0.6)
        self.wait(0.3)


# ================================================================= 11 environments
class S11(Deck):
    n = 11
    title = "Environments and sandboxes"

    def construct(self):
        self.prep()
        H = 4.0

        def panel(title, accent, items, w, x):
            c = card(title, "", accent, w, H, 30)
            c.move_to([x, 0.0, 0])
            rows = []
            for a, b in items:
                head = T(a, 28, BLUE, "SEMIBOLD")
                g = VGroup(head)
                if b:
                    g.add(T(b, 21, INK).next_to(head, DOWN, buff=0.06, aligned_edge=LEFT))
                rows.append(g)
            col = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            col.next_to(c[3], DOWN, buff=0.35, aligned_edge=LEFT)
            return VGroup(c, col)

        left = panel("What it can touch", BLUE, [("Files", ""), ("A shell", "runs commands"), ("The network and tools", "")], 5.4, -3.7)
        right = panel("More permission, more isolation", GOOD,
                      [("Git worktree", "its own branch folder"), ("Container", "a disposable mini computer"),
                       ("Cloud sandbox", "someone else's machine")], 6.9, 2.95)
        self.play(FadeIn(left, shift=UP * 0.2), run_time=0.8)
        self.next_slide()
        self.play(FadeIn(right, shift=UP * 0.2), run_time=0.8)
        arr = Arrow([2.95 - 2.4, -2.35, 0], [2.95 + 2.4, -2.35, 0], buff=0, stroke_width=4, color=GOOD, tip_length=0.2,
                    max_tip_length_to_length_ratio=1)
        lab = T("safer", 22, GOOD, "BOLD").next_to(arr, DOWN, buff=0.08)
        self.play(Create(arr), FadeIn(lab), run_time=0.6)


# ================================================================= 12 guardrails
class S12(Deck):
    n = 12
    title = "Guardrails"

    def construct(self):
        self.prep()
        w, h = 6.1, 2.35
        cs = [card("Permission prompts", "The agent asks you before it does anything risky.", WARN, w, h, 30, 21, 44),
              card("Allow and deny lists", "Pre-approve safe commands, like running tests. Block the rest.", WARN, w, h, 30, 21, 44),
              card("Hooks", "Scripts that block rm -rf (delete all) and force push (rewrite history).", GOOD, w, h, 30, 21, 44),
              card("Tests and linters", "Automatic checks that must pass. A linter spots mistakes and messy code.", GOOD, w, h, 30, 21, 44)]
        VGroup(*cs).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to([0, -0.2, 0])
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.6)
        for c in cs[1:]:
            self.next_slide()
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)


# ================================================================= 13 lock files
class S13(Deck):
    n = 13
    title = "Lock files pin versions"

    def construct(self):
        self.prep()
        rows = [('  "dependencies": {', INK), ('    "express": "4.19.2",', INK),
                ('+   "leftpad-utils": "0.0.1"', GOOD), ("  }", INK)]
        ts = VGroup(*[M(s, 27, c) for s, c in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        panel = box(ts.width + 1.4, ts.height + 0.9, BLUE, PAPER, 2.2, 0.05).move_to([0, 0.15, 0])
        shadow = Rectangle(width=panel.width, height=panel.height, stroke_width=0, fill_color=TINT,
                           fill_opacity=1).move_to(panel).shift(RIGHT * 0.1 + DOWN * 0.1)
        ts.move_to(panel)
        band = Rectangle(width=panel.width - 0.1, height=0.55, stroke_width=0, fill_color=GOOD_BG,
                         fill_opacity=1).move_to([panel.get_center()[0], ts[2].get_center()[1], 0])
        t1 = T("Pinned versions mean agents cannot silently add or upgrade packages.", 28, BLUE, "SEMIBOLD")
        t1.move_to([LM, -1.75, 0], aligned_edge=LEFT)
        t2 = T("Read every new line in the diff (the list of changes). Never heard of it? Stop and check.", 24, INK)
        t2.move_to([LM, -2.35, 0], aligned_edge=LEFT)
        self.add(self.intro("A lock file lists the exact version of every package your project uses."))
        self.play(FadeIn(shadow), FadeIn(panel), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in ts], lag_ratio=0.2), run_time=1.4)
        self.next_slide()
        self.add(band)
        self.add(ts)
        self.play(Indicate(ts[2], color=GOOD, scale_factor=1.05), run_time=0.9)
        self.play(FadeIn(t1, shift=UP * 0.2), FadeIn(t2, shift=UP * 0.2), run_time=0.6)


# ================================================================= 14 sub-agents
class S14(Deck):
    n = 14
    title = "Sub-agents are about context"

    def construct(self):
        self.prep()
        BW = 2.6

        def bar(frac, color, x, y):
            track = Rectangle(width=BW, height=0.18, stroke_color=EDGE, stroke_width=1.5, fill_color=WASH_B,
                              fill_opacity=1).move_to([x, y, 0])
            fill = Rectangle(width=max(BW * frac, 0.04), height=0.18, stroke_width=0, fill_color=color,
                             fill_opacity=1).move_to(track.get_left(), aligned_edge=LEFT)
            return track, fill

        main = pill("Main agent", BLUE, WASH_B, 3.6, 0.9, 30).move_to([0, 1.55, 0])
        msub = T("clean window", 20, INK).next_to(main, DOWN, buff=0.12)
        mt, mf = bar(0.15, GOOD, 0, 0.62)
        xs = [-4.2, 0, 4.2]
        names = [("Sub-agent A", "reads the auth code"), ("Sub-agent B", "reads the database code"),
                 ("Sub-agent C", "reads the tests")]
        subs, tracks, fills = [], [], []
        for (a, b), x in zip(names, xs):
            bx = box(3.5, 1.15, SOFT, PAPER, 2.0, 0.05).move_to([x, -1.0, 0])
            bx.set_stroke(opacity=1)
            ta = T(a, 27, BLUE, "BOLD").move_to([x, -0.82, 0])
            tb = T(b, 20, INK).move_to([x, -1.27, 0])
            t, f = bar(0.05, WARN, x, -1.85)
            subs.append(VGroup(bx, ta, tb))
            tracks.append(t)
            fills.append(f)
        down = [Arrow([x + 0.45, 0.2, 0], [x + 0.45, -0.38, 0], buff=0, stroke_width=3, color=SOFT, tip_length=0.18,
                      max_tip_length_to_length_ratio=1) for x in xs]
        dlab = [T("task", 20, SOFT).move_to([x + 1.05, -0.1, 0]) for x in xs]
        up = [Arrow([x - 0.45, -0.38, 0], [x - 0.45, 0.2, 0], buff=0, stroke_width=3, color=GOOD, tip_length=0.18,
                    max_tip_length_to_length_ratio=1) for x in xs]
        ulab = [T("summary", 20, GOOD, "BOLD").move_to([x - 1.25, -0.1, 0]) for x in xs]
        stems = [Line([x, 0.62 - 0.0, 0], [x, 0.2, 0], color=EDGE, stroke_width=2) for x in xs]
        take = self.takeaway("Each one reads a lot. Only a short result comes back.", size=28)

        self.play(FadeIn(main), FadeIn(msub), FadeIn(mt), FadeIn(mf), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(s) for s in subs], lag_ratio=0.2), *[FadeIn(t) for t in tracks],
                  *[FadeIn(f) for f in fills], run_time=1.0)
        self.next_slide()
        self.play(*[Create(a) for a in down], *[FadeIn(l) for l in dlab], run_time=0.6)
        grow = []
        for t, f in zip(tracks, fills):
            nf = Rectangle(width=BW * 0.9, height=0.18, stroke_width=0, fill_color=BAD,
                           fill_opacity=1).move_to(t.get_left(), aligned_edge=LEFT)
            grow.append(Transform(f, nf))
        self.play(*grow, run_time=2.0, rate_func=linear)
        self.next_slide()
        self.play(*[Create(a) for a in up], *[FadeIn(l) for l in ulab], run_time=0.7)
        small = [Transform(f, Rectangle(width=BW * 0.05, height=0.18, stroke_width=0, fill_color=GOOD,
                                        fill_opacity=1).move_to(t.get_left(), aligned_edge=LEFT))
                 for t, f in zip(tracks, fills)]
        nmf = Rectangle(width=BW * 0.22, height=0.18, stroke_width=0, fill_color=GOOD,
                        fill_opacity=1).move_to(mt.get_left(), aligned_edge=LEFT)
        self.play(Transform(mf, nmf), *small, FadeIn(take, shift=UP * 0.2), run_time=1.2)


# ================================================================= 15 multi-agent
class S15(Deck):
    n = 15
    title = "Multi-agent loops"

    def construct(self):
        self.prep()
        w, h = 4.15, 3.3
        cs = [card("Fan-out", "Ask several agents to research different questions at once.", BLUE, w, h, 32, 22, 25),
              card("Pipeline", "One agent plans, another writes the code, a third reviews it.", BLUE, w, h, 32, 22, 25),
              card("Until it passes", "The agent runs the tests, fixes what fails, and repeats until they pass.", BLUE, w, h, 32, 22, 25)]
        VGroup(*cs).arrange(RIGHT, buff=0.25).move_to([0, 0.15, 0])
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.6)
        for c in cs[1:]:
            self.next_slide()
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)
        warn = self.takeaway("More agents means more output for you to review.", WARN_TXT)
        self.next_slide()
        self.play(FadeIn(warn, shift=UP * 0.2), run_time=0.6)


# ================================================================= 16 agents lock files
class S16(Deck):
    n = 16
    title = "Agents lock files too"

    def construct(self):
        self.prep()
        names, ys = ["player.js", "animations.js", "level.js"], [0.95, -0.15, -1.25]

        def status(kind, y):
            if kind == "free":
                m = T("free", 20, GOOD, "SEMIBOLD")
            else:
                col, who = (ORANGE, "Animation agent") if kind == "anim" else (BLUE, "Review agent")
                m = VGroup(padlock(col), T(who, 19, col, "SEMIBOLD")).arrange(RIGHT, buff=0.12)
            return m.move_to([2.7, y, 0], aligned_edge=RIGHT)

        tiles, sts = [], []
        for nm, y in zip(names, ys):
            t = box(6.0, 0.85, EDGE, PAPER, 2.4, 0.05).move_to([0, y, 0])
            lab = M(nm, 22, BLUE).move_to([-2.75, y, 0], aligned_edge=LEFT)
            tiles.append(VGroup(t, lab))
            sts.append(status("free", y))
        anim = pill("Animation agent", ORANGE, WASH_O, 2.5, 0.95, 19).move_to([-5.35, -0.15, 0])
        rev = pill("Review agent", BLUE, WASH_B, 2.5, 0.95, 19).move_to([5.35, -0.15, 0])
        a_sub = T("builds the animations", 18, SOFT).next_to(anim, DOWN, buff=0.15)
        r_sub = T("checks the work", 18, SOFT).next_to(rev, DOWN, buff=0.15)

        def arrow(a, b, col):
            return Arrow(a, b, buff=0, stroke_width=3.5, color=col, tip_length=0.18, max_tip_length_to_length_ratio=1)

        self.add(self.intro("To avoid collisions, each agent claims the files it works on."))
        self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.15), *[FadeIn(x) for x in sts], run_time=1.0)
        self.play(FadeIn(anim), FadeIn(rev), FadeIn(a_sub), FadeIn(r_sub), run_time=0.7)

        # 1: the animation agent claims two files
        self.next_slide()
        a1, a2 = arrow([-4.1, 0.05, 0], [-3.05, ys[0], 0], ORANGE), arrow([-4.1, -0.15, 0], [-3.05, ys[1], 0], ORANGE)
        n0, n1 = status("anim", ys[0]), status("anim", ys[1])
        self.play(Create(a1), Create(a2), tiles[0][0].animate.set_stroke(ORANGE), tiles[1][0].animate.set_stroke(ORANGE),
                  FadeOut(sts[0]), FadeOut(sts[1]), FadeIn(n0), FadeIn(n1), run_time=0.9)
        sts[0], sts[1] = n0, n1

        # 2: the review agent claims level.js, then gets blocked on player.js
        self.next_slide()
        a3 = arrow([4.1, -0.35, 0], [3.05, ys[2], 0], BLUE)
        n2 = status("rev", ys[2])
        self.play(Create(a3), tiles[2][0].animate.set_stroke(BLUE), FadeOut(sts[2]), FadeIn(n2), run_time=0.8)
        sts[2] = n2
        blocked = DashedLine([4.1, 0.15, 0], [3.2, ys[0] - 0.05, 0], color=BAD, stroke_width=3.5, dash_length=0.12)
        cross = Cross(Square(0.26), stroke_color=BAD, stroke_width=5).move_to([3.2, ys[0] - 0.05, 0])
        note = para("Locked. Wait, or work on another file.", 20, BAD, 20, w="SEMIBOLD").move_to([5.35, 1.6, 0])
        self.play(Create(blocked), FadeIn(cross), FadeIn(note), run_time=0.8)

        # 3: the animation agent finishes and releases, then the review agent takes player.js
        self.next_slide()
        f0, f1 = status("free", ys[0]), status("free", ys[1])
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(blocked), FadeOut(cross), FadeOut(note),
                  tiles[0][0].animate.set_stroke(EDGE), tiles[1][0].animate.set_stroke(EDGE),
                  FadeOut(sts[0]), FadeOut(sts[1]), FadeIn(f0), FadeIn(f1), run_time=0.9)
        a4 = arrow([4.1, 0.1, 0], [3.05, ys[0], 0], BLUE)
        n0 = status("rev", ys[0])
        self.play(Create(a4), tiles[0][0].animate.set_stroke(BLUE), FadeOut(f0), FadeIn(n0), run_time=0.9)
        take = self.takeaway("One owner per file at a time, so agents never overwrite each other.", size=28)
        self.play(FadeIn(take, shift=UP * 0.2), run_time=0.6)


# ================================================================= 17 try it at your hackathon
class S17(Deck):
    n = 17
    title = "Try it in your hackathon project"

    def construct(self):
        self.prep()
        steps = [
            "Give each agent its own area: a folder or a git worktree (a separate working copy).",
            "Keep a claims file: LOCKS.md lists which agent owns which file.",
            "Put the rule in CLAUDE.md so every agent follows it.",
            "You read each diff and merge the branches yourself.",
        ]
        rows = []
        for i, txt in enumerate(steps):
            y = 1.7 - i * 1.08
            dot = Circle(0.25, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([LM + 0.25, y, 0])
            num = T(str(i + 1), 24, PAPER, "BOLD").move_to(dot)
            body = para(txt, 23, INK, 42, w="MEDIUM").move_to([LM + 0.8, y, 0], aligned_edge=LEFT)
            rows.append(VGroup(dot, num, body))

        def panel(label, cy, h):
            b = box(5.7, h, BLUE, WASH_B, 2.2, 0.05).move_to([3.55, cy, 0])
            sh = Rectangle(width=5.7, height=h, stroke_width=0, fill_color=TINT, fill_opacity=1).move_to(b).shift(RIGHT * 0.1 + DOWN * 0.1)
            lb = M(label, 20, SOFT).move_to(b.get_corner(UL) + np.array([0.3, -0.3, 0]), aligned_edge=UL)
            return VGroup(sh, b, lb), b, lb

        p1, b1, l1 = panel("LOCKS.md", 1.05, 2.0)
        lines = ["animations.js   animation-agent", "player.js       animation-agent", "level.js        review-agent"]
        ls = VGroup(*[M(t, 20, BLUE) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        ls.next_to(l1, DOWN, buff=0.22, aligned_edge=LEFT)
        p2, b2, l2 = panel("CLAUDE.md", -1.35, 2.4)
        rule = para("Before you edit a file, claim it in LOCKS.md. If another agent has it, work on something else. "
                    "Delete your row when you are done.", 20, INK, 40).next_to(l2, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(FadeIn(rows[0], shift=UP * 0.2), FadeIn(rows[1], shift=UP * 0.2), run_time=0.8)
        self.next_slide()
        self.play(FadeIn(p1), FadeIn(ls), run_time=0.8)
        self.next_slide()
        self.play(FadeIn(rows[2], shift=UP * 0.2), FadeIn(p2), FadeIn(rule), run_time=0.8)
        self.next_slide()
        self.play(FadeIn(rows[3], shift=UP * 0.2), run_time=0.6)


# ================================================================= 18 review
class S18(Deck):
    n = 18
    title = "Review is the bottleneck"

    def construct(self):
        self.prep()
        w, h = 4.15, 3.3
        cs = [card("Read the diff", "Check every changed line, not just the summary. A diff is the list of changes.", GOOD, w, h, 32, 22, 25),
              card("Run it", "Try the feature yourself. Passing tests only cover what someone thought to test.", GOOD, w, h, 32, 22, 25),
              card("Keep PRs small", "A PR (pull request) is a proposed change. Big ones get skimmed, so keep them small.", GOOD, w, h, 32, 22, 25)]
        VGroup(*cs).arrange(RIGHT, buff=0.25).move_to([0, 0.0, 0])
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.6)
        for c in cs[1:]:
            self.next_slide()
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)


# ================================================================= 19 human at the end
class S19(Deck):
    n = 19
    title = "The human at the end"
    credit = AIRBNB

    def construct(self):
        self.prep()
        L = Loop()
        L.all().scale(0.88, about_point=ORIGIN).shift(UP * 0.2)
        self.play(FadeIn(L.all(), lag_ratio=0.03), run_time=1.2)
        self.next_slide()
        self.play(*L.focus({"review", "pr", "e_pr", "e_cc", "l_cc", "prompt", "e_out", "l_out", "dev_region"}),
                  run_time=0.8)
        a = self.takeaway("The agent opens the PR. A human merges it.", y=-2.25, size=28)
        b = self.takeaway("If you cannot explain a line, it does not ship.", BAD, y=-2.75, size=28)
        self.play(FadeIn(a, shift=UP * 0.2), run_time=0.6)
        self.next_slide()
        self.play(FadeIn(b, shift=UP * 0.2), Indicate(L.m["pr"], color=ORANGE, scale_factor=1.15), run_time=0.8)


# ================================================================= 20 questions
class S20(Deck):
    n = 20
    hero = True

    def construct(self):
        self.prep()
        self.add(facets(1.0))
        logo = ImageMobject(str(HERE / "assets" / "logo.png")).scale_to_fit_height(2.2).move_to([4.9, 1.65, 0])
        q = T("Questions?", 100, BLUE, "BOLD").move_to([LM, 1.3, 0], aligned_edge=LEFT)
        bar = Rectangle(width=1.4, height=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1)
        bar.move_to([LM, 2.55, 0], aligned_edge=LEFT)
        l1 = M("github.com/mattpocock/skills", 26, INK)
        l2 = M("github.com/humanlayer/advanced-context-engineering-for-coding-agents", 22, INK)
        l3 = T("Dex Horthy, HumanLayer", 22, SOFT)
        links = VGroup(l1, l2, l3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([LM, -0.6, 0], aligned_edge=LEFT)
        rule = Line([LM, -1.85, 0], [LM + 5.2, -1.85, 0], stroke_color=EDGE, stroke_width=2)
        thanks = T("Thank you", 20, SOFT, "MEDIUM").move_to([LM, -2.2, 0], aligned_edge=LEFT)
        who = T("Nedas Jaronis", 36, BLUE, "BOLD").move_to([LM, -2.65, 0], aligned_edge=LEFT)
        club = T("AI2 Club", 26, ORANGE, "SEMIBOLD").next_to(who, RIGHT, buff=0.35, aligned_edge=DOWN)
        self.add(logo)
        self.play(GrowFromEdge(bar, LEFT), FadeIn(q, shift=UP * 0.3), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in links], lag_ratio=0.25), run_time=1.2)
        self.play(Create(rule), FadeIn(thanks), FadeIn(who), FadeIn(club), run_time=0.7)
