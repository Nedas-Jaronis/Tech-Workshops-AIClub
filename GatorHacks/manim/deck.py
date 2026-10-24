"""Agents 101: an animated Manim Slides deck.

One Slide subclass per slide. Render with render.ps1, present with present.ps1.
"""
import textwrap

import numpy as np
from manim import *
from manim_slides import Slide

# ---------------------------------------------------------------- design tokens
BG = "#000000"
FG = "#F5F5F7"
MUTED = "#86868B"
DIM = "#6E6E73"
HAIR = "#3A3A3C"
CARD = "#111113"
GREEN = "#30D158"
YELLOW = "#FFD60A"
RED = "#FF453A"
BLUE = "#0A84FF"
GREEN_BG = "#0D2B17"
BLUE_BG = "#0A2342"
FONT = "Segoe UI"
MONO = "Consolas"
TOTAL = 18


def T(s, size=26, color=FG, bold=False, font=FONT, **kw):
    return Text(s, font=font, font_size=size, color=color, weight=BOLD if bold else NORMAL, **kw)


def para(s, size=22, color=MUTED, width=34, **kw):
    return T(textwrap.fill(s, width), size, color, line_spacing=0.95, **kw)


def card(title, body, accent, w=3.8, h=2.5, body_width=24, title_size=28, body_size=21):
    box = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=HAIR, stroke_width=1.5,
                           fill_color=CARD, fill_opacity=1)
    bar = Line(box.get_corner(UL) + RIGHT * 0.3, box.get_corner(UR) + LEFT * 0.3,
               stroke_color=accent, stroke_width=6)
    t = T(title, title_size, FG, True)
    t.move_to(box.get_top() + DOWN * 0.7).align_to(box, LEFT).shift(RIGHT * 0.35)
    if body:
        b = para(body, body_size, MUTED, body_width)
        b.next_to(t, DOWN, buff=0.28).align_to(t, LEFT)
    else:
        b = Dot(t.get_left(), radius=0, fill_opacity=0)
    return VGroup(box, bar, t, b)


def pill(label, color=HAIR, fill=CARD, w=1.7, h=0.62, text_color=FG, size=20, r=0.18):
    box = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=2.2,
                           fill_color=fill, fill_opacity=1)
    t = T(label, size, text_color, True).move_to(box)
    return VGroup(box, t)


def heading(text):
    return T(text, 50, FG, True).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.8)


def mono_pill(text, size=24, color=GREEN):
    t = T(text, size, FG, font=MONO)
    box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.8, height=t.height + 0.55,
                           stroke_color=HAIR, stroke_width=1.5, fill_color="#0C0C0E", fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


class Deck(Slide):
    """Base slide: black background with a soft blue glow, title, footer and notes."""
    n = 0
    title = None
    notes = ""
    credit = None

    def prep(self):
        self.camera.background_color = ManimColor(BG)
        glow = VGroup(*[
            Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.022).move_to(UP * 5.2)
            for r in (7.0, 5.6, 4.2, 2.9)
        ])
        self.add(glow)
        foot = T(f"{self.n} / {TOTAL}", 16, DIM).to_corner(DR, buff=0.35)
        self.add(foot)
        if self.credit:
            self.add(T(self.credit, 15, DIM).to_corner(DL, buff=0.35))
        self.next_slide(notes=self.notes)
        if self.title:
            h = heading(self.title)
            self.play(FadeIn(h, shift=UP * 0.15), run_time=0.5)
            self.h = h

    def reveal(self, *mobs, shift=UP * 0.25, run_time=0.6, lag=0.12):
        self.play(LaggedStart(*[FadeIn(m, shift=shift) for m in mobs], lag_ratio=lag), run_time=run_time)


AIRBNB = "Diagram adapted from a talk by Airbnb senior staff engineers"


# ---------------------------------------------------------------- the loop diagram
class Loop:
    """Both loops. Build once, reuse on slides 2 and 17. Nodes and edges are looked up by name."""

    def __init__(self, shift=ORIGIN, scale=1.0):
        self.m = {}
        cx_dev, cy = -4.15, -0.25
        dev = RoundedRectangle(corner_radius=0.5, width=5.0, height=5.2, stroke_color=HAIR, stroke_width=2,
                               fill_color="#0A0A0C", fill_opacity=1).move_to([cx_dev, cy, 0])
        dev_l = T("DEVELOPER LOOP", 15, FG, True).move_to(dev.get_top() + DOWN * 0.38).align_to(dev, LEFT).shift(RIGHT * 0.35)
        dev_s = T("you", 15, MUTED).next_to(dev_l, DOWN, buff=0.1).align_to(dev_l, LEFT)
        ell = DashedVMobject(Ellipse(width=6.6, height=5.4, color=MUTED, stroke_width=2).move_to([3.2, cy, 0]),
                             num_dashes=70)
        ag_l = T("AGENTIC AI LOOP", 15, FG, True).move_to([3.2, cy + 2.2, 0])
        ag_s = T("the agent", 15, MUTED).next_to(ag_l, DOWN, buff=0.1)
        self.m["dev_region"] = VGroup(dev, dev_l, dev_s)
        self.m["agent_region"] = VGroup(ell, ag_l, ag_s)

        def node(name, label, pos, kind="neutral", w=1.6, pill_shape=False):
            if kind == "you":
                p = pill(label, GREEN, GREEN_BG, w, 0.62, r=0.31 if pill_shape else 0.18)
            elif kind == "pr":
                p = pill(label, FG, FG, w, 0.62, text_color=BG, r=0.31)
            else:
                p = pill(label, "#5A5A5E", "#1C1C1E", w, 0.62)
            p.move_to(pos)
            self.m[name] = p

        node("spec", "Feature spec", [-5.35, 1.15, 0], "you", 1.7, True)
        node("prompt", "Prompt", [-2.95, 1.15, 0], "you", 1.5)
        node("review", "Review", [-2.95, -1.75, 0], "you", 1.5)
        node("pr", "PR", [-5.35, -1.75, 0], "pr", 1.1, True)
        node("config", "Config", [1.9, -1.75, 0], "you", 1.5)
        node("llm", "LLM", [1.9, 1.15, 0], "neutral", 1.5)
        node("env", "Environment", [4.7, 1.15, 0], "neutral", 2.0)
        node("guard", "Guardrails", [4.7, -1.75, 0], "you", 1.8)

        def A(a, b, dashed=False, color=MUTED):
            if dashed:
                ln = DashedLine(a, b, dash_length=0.14, stroke_width=3, color=color)
                ln.add_tip(tip_length=0.2)
                return ln
            return Arrow(a, b, buff=0, stroke_width=3, color=color, tip_length=0.2, max_tip_length_to_length_ratio=1)

        def lab(text, pos):
            return T(text, 17, MUTED).move_to(pos)

        E = self.m
        E["e_spec"] = A([-4.5, 1.15, 0], [-3.7, 1.15, 0])
        E["e_hand"] = A([-2.2, 1.15, 0], [1.15, 1.15, 0], color=GREEN)
        E["l_hand"] = lab("hand off", [-0.55, 1.5, 0])
        E["e_load"] = A([1.9, -1.4, 0], [1.9, 0.82, 0])
        E["l_load"] = lab("load", [2.35, -0.3, 0])
        E["e_use"] = A([2.68, 1.15, 0], [3.65, 1.15, 0])
        E["l_use"] = lab("use", [3.17, 0.82, 0])
        E["e_enf"] = A([4.7, 0.82, 0], [4.7, -1.4, 0])
        E["l_enf"] = lab("enforce", [5.35, -0.3, 0])
        E["e_chk"] = A([3.95, -1.4, 0], [2.6, 0.82, 0])
        E["l_chk"] = lab("check", [3.95, -0.2, 0])
        E["e_out"] = A([0.45, -1.75, 0], [-2.2, -1.75, 0], dashed=True)
        E["l_out"] = lab("AI outputs", [-0.9, -2.1, 0])
        E["e_cc"] = A([-2.95, -1.4, 0], [-2.95, 0.82, 0])
        E["l_cc"] = lab("course correct", [-1.6, -0.3, 0])
        E["e_pr"] = A([-3.7, -1.75, 0], [-4.8, -1.75, 0])
        for v in self.m.values():
            v.scale(scale, about_point=ORIGIN).shift(shift)

        # which parts belong to each stage of the walkthrough
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

    def focus(self, names, dim=0.18):
        """Animations that dim everything except `names`."""
        anims = []
        for k, v in self.m.items():
            anims.append(v.animate.set_opacity(1 if k in names else dim))
        return anims


# ================================================================= 01 title
class S01(Deck):
    n = 1
    notes = ("Welcome. Goal for the next hour: you leave knowing how to get good work out of an AI coding agent, "
             "and how to avoid the common ways it goes wrong.\n\n"
             "An agent here means an AI model that can read files, run commands, and edit code on its own in a loop, "
             "instead of just answering one question.\n\n"
             "This is not a hype talk. We will cover what the agent sees, what it can touch, and where you stay in control.")

    def construct(self):
        self.prep()
        t = T("Agents 101", 110, FG, True).shift(UP * 0.6)
        sub = T("How to actually work with AI coding agents", 34, MUTED).next_to(t, DOWN, buff=0.45)
        tag = T("GatorHacks workshop", 22, DIM).next_to(sub, DOWN, buff=0.9)
        line = Line(LEFT * 1.2, RIGHT * 1.2, stroke_color=BLUE, stroke_width=5).next_to(t, UP, buff=0.5)
        self.play(GrowFromCenter(line), run_time=0.5)
        self.play(FadeIn(t, shift=UP * 0.3), run_time=0.9)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(tag), run_time=0.5)
        self.wait(0.5)


# ================================================================= 02 two loops
class S02(Deck):
    n = 2
    title = "The two loops"
    credit = AIRBNB
    notes = ("Read the diagram left to right. An LLM is the large language model, the AI brain.\n\n"
             "Click 1: the outer loop is you. You take a feature spec and write a prompt.\n"
             "Click 2: you hand it off. The inner dashed loop is the agent. It loads its config (the system prompt, "
             "the standing instructions), calls the LLM, uses its environment (files, shell, tools), and guardrails "
             "check each step.\n"
             "Click 3: outputs come back to you for review. If it is not right, you course correct and re-prompt. "
             "If it is right, it becomes a PR (pull request, a proposed code change someone must approve).\n\n"
             "Green boxes are where you have leverage: the prompt, the config, the guardrails, and the review.\n\n"
             "Tie to the software development lifecycle (SDLC): plan, build, test, review, ship. The old loop had a "
             "human doing every step. Now the agent does build and test inside its loop, and the human moves up to "
             "planning and review.")

    def construct(self):
        self.prep()
        L = Loop(shift=UP * 0.12, scale=0.86)
        self.play(FadeIn(L.group("dev"), lag_ratio=0.1), run_time=1.0)
        self.next_slide()
        self.play(FadeIn(L.group("agent"), lag_ratio=0.05), run_time=1.6)
        self.next_slide()
        self.play(FadeIn(L.group("out"), lag_ratio=0.1), run_time=1.2)
        legend = T("LLM: the AI model   ·   Config: standing instructions   ·   PR: a proposed code change", 17, MUTED)
        legend.move_to([0, -2.7, 0])
        take = T("You control what goes in and what comes out. The agent runs the middle.", 25, FG, True)
        take.move_to([0, -3.1, 0])
        self.next_slide()
        self.play(FadeIn(legend), FadeIn(take, shift=UP * 0.2), run_time=0.7)


# ================================================================= 03 lifecycle
class S03(Deck):
    n = 3
    title = "The lifecycle is shifting"
    notes = ("The software development lifecycle (SDLC) is the set of steps every feature goes through: plan, build, "
             "test, review, ship.\n\n"
             "Before agents, a person did every step. Now the agent handles build and test inside its own loop. "
             "That does not remove work, it moves it. Planning (the spec) and review become the main human jobs, "
             "and mistakes there get more expensive because the agent moves fast.\n\n"
             "This is the theme of the rest of the talk: what the agent sees (context), where it gets worse "
             "(dumb zone), how to scale it (multi-agent loops), and how you check it (review).")

    def construct(self):
        self.prep()

        def row(labels, y, special=None):
            items = []
            for i, lab in enumerate(labels):
                if special == i:
                    p = pill(lab, BLUE, BLUE_BG, 3.6, 0.95, size=24, r=0.3)
                    sm = T("the agent loop", 15, "#64D2FF").move_to(p).shift(DOWN * 0.22)
                    p[1].shift(UP * 0.12)
                    p = VGroup(p, sm)
                else:
                    p = pill(lab, GREEN, GREEN_BG, 1.9, 0.8, size=24, r=0.4)
                items.append(p)
            g = VGroup(*items).arrange(RIGHT, buff=0.55).move_to([0.6, y, 0])
            arrows = VGroup(*[Arrow(items[i].get_right(), items[i + 1].get_left(), buff=0.08, stroke_width=3,
                                    color=MUTED, tip_length=0.15, max_tip_length_to_length_ratio=1)
                              for i in range(len(items) - 1)])
            return g, arrows

        tagb = T("BEFORE", 18, MUTED, True).move_to([-6.2, 1.0, 0])
        r1, a1 = row(["Plan", "Build", "Test", "Review", "Ship"], 1.0)
        r1.shift(RIGHT * 0.5)
        a1 = VGroup(*[Arrow(r1[i].get_right(), r1[i + 1].get_left(), buff=0.08, stroke_width=3, color=MUTED,
                            tip_length=0.15, max_tip_length_to_length_ratio=1) for i in range(4)])
        n1 = T("You did every step.", 20, MUTED).next_to(r1, DOWN, buff=0.3).align_to(r1, LEFT)
        tagn = T("NOW", 18, GREEN, True).move_to([-6.2, -1.5, 0])
        r2, a2 = row(["Plan", "Build + Test", "Review", "Ship"], -1.5, special=1)
        r2.shift(RIGHT * 0.5)
        a2 = VGroup(*[Arrow(r2[i].get_right(), r2[i + 1].get_left(), buff=0.08, stroke_width=3, color=MUTED,
                            tip_length=0.15, max_tip_length_to_length_ratio=1) for i in range(3)])
        n2 = T("The agent does the middle.", 20, MUTED).next_to(r2, DOWN, buff=0.35).align_to(r2, LEFT)
        take = T("Your time moves to planning and reviewing.", 28, FG, True).to_edge(DOWN, buff=0.6)

        self.reveal(tagb, *r1, run_time=1.0, lag=0.15)
        self.play(Create(a1), FadeIn(n1), run_time=0.8)
        self.next_slide()
        self.reveal(tagn, *r2, run_time=1.0, lag=0.15)
        self.play(Create(a2), FadeIn(n2), run_time=0.8)
        # fade the "Before" row so the shift reads clearly
        self.play(*[m.animate.set_opacity(0.3) for m in (tagb, r1, a1, n1)], run_time=0.6)
        self.next_slide()
        self.play(FadeIn(take, shift=UP * 0.2), run_time=0.6)


# ================================================================= 04 context window
class S04(Deck):
    n = 4
    title = "What is in the context window"
    notes = ("The context window is the model's working memory: everything it can see right now. It is measured in "
             "tokens (roughly word pieces; 1 token is about three quarters of a word).\n\n"
             "Everything here competes for the same space. System prompt and config files load at the start. "
             "Skills load when relevant. Every file it reads and every command output gets added. So does every "
             "message in the chat.\n\n"
             "If something is not in the window, the agent does not know it. It cannot see your head, your Slack, "
             "or last week's chat. That is why writing things down (specs, config files) works so well.")

    def construct(self):
        self.prep()
        c1 = card("Instructions", "System prompt, rules file (CLAUDE.md), skills", BLUE, 3.95, 3.0, 22, 30, 23)
        c2 = card("What it read", "Files and tool output", BLUE, 3.95, 3.0, 22, 30, 23)
        c3 = card("The conversation", "Everything you and the agent said", BLUE, 3.95, 3.0, 22, 30, 23)
        g = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.35).shift(UP * 0.1)
        self.reveal(*g, run_time=1.2, lag=0.25)
        q = T("The agent only knows what is in its context.", 32, FG, True)
        bar = Line(UP * 0.3, DOWN * 0.3, stroke_color=BLUE, stroke_width=6)
        qq = VGroup(bar, q).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1.0)
        self.next_slide()
        self.play(FadeIn(qq, shift=UP * 0.2), run_time=0.7)


# ================================================================= 05 dumb zone
class S05(Deck):
    n = 5
    title = "The dumb zone"
    notes = ("Term from Dex Horthy of HumanLayer. Models advertise huge windows, but in practice answers get worse "
             "once the window is filled with a lot of material, often starting around 40%.\n\n"
             "Why: more noise to sort through, important instructions get buried, and old wrong turns keep "
             "influencing new answers.\n\n"
             "Watch the bar fill. Green is the smart zone, yellow is slipping, red is the dumb zone. The dashed "
             "lines are roughly 40% and 70%. Treat these as rules of thumb, not exact numbers. They vary by model "
             "and task.")

    def construct(self):
        self.prep()
        W, H, x0, y0 = 11.0, 0.7, -5.5, 0.9
        N = 80

        def col(f):
            if f < 0.38:
                return GREEN
            if f < 0.55:
                return interpolate_color(ManimColor(GREEN), ManimColor(YELLOW), (f - 0.38) / 0.17)
            if f < 0.8:
                return interpolate_color(ManimColor(YELLOW), ManimColor(RED), (f - 0.55) / 0.25)
            return RED

        track = RoundedRectangle(corner_radius=0.35, width=W, height=H, stroke_color=HAIR, stroke_width=2,
                                 fill_color="#17171A", fill_opacity=1).move_to([0, y0, 0])
        segs = VGroup(*[Rectangle(width=W / N + 0.01, height=H - 0.08, stroke_width=0, fill_color=col(i / N),
                                  fill_opacity=1).move_to([x0 + (i + 0.5) * W / N, y0, 0]) for i in range(N)])
        m40 = DashedLine([x0 + 0.4 * W, y0 + 0.55, 0], [x0 + 0.4 * W, y0 - 0.55, 0], color=FG, stroke_width=3, dash_length=0.1)
        m70 = DashedLine([x0 + 0.7 * W, y0 + 0.55, 0], [x0 + 0.7 * W, y0 - 0.55, 0], color=FG, stroke_width=3, dash_length=0.1)
        names = VGroup(
            T("Smart zone", 26, GREEN, True).move_to([x0 + 0.2 * W, y0 - 0.95, 0]),
            T("Slipping", 26, YELLOW, True).move_to([x0 + 0.55 * W, y0 - 0.95, 0]),
            T("Dumb zone", 26, RED, True).move_to([x0 + 0.85 * W, y0 - 0.95, 0]),
        )
        ticks = VGroup(*[T(t, 19, MUTED).move_to([x0 + f * W, y0 - 1.5, 0]) for t, f in
                         (("0%", 0.0), ("40%", 0.4), ("70%", 0.7), ("100%", 1.0))])
        ticks[0].shift(RIGHT * 0.2)
        ticks[3].shift(LEFT * 0.25)
        take = T("Quality starts to slip around 40% full and falls off fast past 70%.", 28, FG).to_edge(DOWN, buff=1.4)

        self.play(FadeIn(track), run_time=0.5)
        self.play(FadeIn(ticks), run_time=0.4)
        self.next_slide()
        self.play(LaggedStart(*[FadeIn(s) for s in segs], lag_ratio=0.05), run_time=5.5, rate_func=linear)
        self.play(Create(m40), Create(m70), run_time=0.5)
        self.play(FadeIn(names, shift=UP * 0.15), run_time=0.6)
        self.next_slide()
        self.play(FadeIn(take, shift=UP * 0.2), run_time=0.6)


# ================================================================= 06 session timeline
class S06(Deck):
    n = 6
    title = "How a session grows and shrinks"
    notes = ("This is one working session, left to right. The line is how full the context window is.\n\n"
             "Click through each step. Growth is the blue line. The green dotted line is a drop.\n\n"
             "Terms: /compact is a command that asks the agent to summarize the conversation so far and replace the "
             "long history with that summary. It frees space but loses detail, and you do not choose what is "
             "dropped. /clear empties the window completely. On its own that loses everything, so first have the "
             "agent write a plan or handoff file, then start the new session from that file. That is the cleanest "
             "way back to the green zone.\n\n"
             "The dashed lines at 40% and 70% are rules of thumb, not exact limits.")

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
        xl, xr, y0, y1 = -5.2, 5.2, -1.45, 1.55
        Y = lambda p: y0 + (y1 - y0) * p / 100
        X = lambda i: xl + (xr - xl) * i / (len(pts) - 1)
        zc = lambda p: GREEN if p < 40 else (YELLOW if p < 70 else RED)
        bands = VGroup(
            Rectangle(width=11.2, height=Y(40) - Y(0), stroke_width=0, fill_color=GREEN, fill_opacity=0.08).move_to([0, (Y(0) + Y(40)) / 2, 0]),
            Rectangle(width=11.2, height=Y(70) - Y(40), stroke_width=0, fill_color=YELLOW, fill_opacity=0.08).move_to([0, (Y(40) + Y(70)) / 2, 0]),
            Rectangle(width=11.2, height=Y(100) - Y(70), stroke_width=0, fill_color=RED, fill_opacity=0.08).move_to([0, (Y(70) + Y(100)) / 2, 0]),
        )
        guides = VGroup(*[DashedLine([-5.6, Y(v), 0], [5.6, Y(v), 0], stroke_width=1.5, color=HAIR, dash_length=0.12) for v in (40, 70)])
        ylabs = VGroup(*[T(f"{v}%", 16, MUTED).move_to([-6.15, Y(v), 0]) for v in (0, 40, 70, 100)])
        zl = VGroup(T("Smart zone", 17, GREEN, True).move_to([-4.6, Y(32), 0]),
                    T("Slipping", 17, YELLOW, True).move_to([-4.75, Y(55), 0]),
                    T("Dumb zone", 17, RED, True).move_to([-4.6, Y(85), 0]))
        zl.set_opacity(0.8)
        cap_title = None
        cap_body = None

        self.play(FadeIn(bands), FadeIn(guides), FadeIn(ylabs), FadeIn(zl), run_time=0.8)

        def caption(i):
            _, _, ct, cb, _ = pts[i]
            box = RoundedRectangle(corner_radius=0.2, width=11.4, height=1.35, stroke_color=HAIR, stroke_width=1.5,
                                   fill_color=CARD, fill_opacity=1).move_to([0, -2.95, 0])
            a = T(ct, 24, FG, True).move_to(box.get_top() + DOWN * 0.38).align_to(box, LEFT).shift(RIGHT * 0.3)
            b = T(textwrap.fill(cb, 95), 18, MUTED).next_to(a, DOWN, buff=0.14).align_to(a, LEFT)
            return VGroup(box, a, b)

        prev_dot, cap = None, None
        for i, (p, lab, ct, cb, drop) in enumerate(pts):
            d = Dot([X(i), Y(p), 0], radius=0.12, color=zc(p))
            lb = T(lab, 17, FG if i == 0 else MUTED, drop, font=MONO if drop else FONT).move_to([X(i), y0 - 0.45, 0])
            c = caption(i)
            anims = []
            if prev_dot is not None:
                seg = DashedLine(prev_dot.get_center(), d.get_center(), color=GREEN, stroke_width=4, dash_length=0.1) if drop \
                    else Line(prev_dot.get_center(), d.get_center(), color=BLUE, stroke_width=5)
                anims.append(Create(seg))
            anims += [GrowFromCenter(d), FadeIn(lb)]
            if cap is None:
                self.play(*anims, FadeIn(c), run_time=0.8)
            else:
                self.next_slide()
                self.play(*anims, FadeOut(cap), FadeIn(c), run_time=0.9)
            if drop:
                self.play(Flash(d, color=GREEN, flash_radius=0.4, line_length=0.15), run_time=0.5)
            cap, prev_dot = c, d


# ================================================================= 07 smart zone
class S07(Deck):
    n = 7
    title = "Staying in the smart zone"
    notes = ("Fresh sessions: do not let one chat run all day. Old context is a cost, not an asset.\n\n"
             "Compact on purpose: compaction means summarizing the conversation to free space. Automatic compaction "
             "is lossy and you do not control it. Do it on purpose instead: ask the agent to write a plan or "
             "handoff file with the goal, what is done, what is next, and key file paths. Then start a clean "
             "session that reads only that file.\n\n"
             "Sub-agents: a sub-agent is a second agent with its own clean window. We cover them properly later. "
             "For now: they let you read a lot without filling your main window.")

    def construct(self):
        self.prep()
        cs = [card("Fresh sessions", "New task, new session. Clear the old one.", GREEN, 3.95, 3.0, 22, 30, 23),
              card("Compact on purpose", "Summarize the work into a plan file, then restart from it.", GREEN, 3.95, 3.0, 22, 30, 23),
              card("Sub-agents", "Push heavy exploration to a separate window.", GREEN, 3.95, 3.0, 22, 30, 23)]
        g = VGroup(*cs).arrange(RIGHT, buff=0.35).shift(DOWN * 0.1)
        self.play(FadeIn(cs[0], shift=UP * 0.25), run_time=0.7)
        self.next_slide()
        self.play(FadeIn(cs[1], shift=UP * 0.25), run_time=0.7)
        self.next_slide()
        self.play(FadeIn(cs[2], shift=UP * 0.25), run_time=0.7)


# ================================================================= 08 skill
class S08(Deck):
    n = 8
    title = "What is a skill"
    notes = ("A skill is a Markdown file, usually named SKILL.md, that holds instructions for one kind of task. "
             "Markdown is just plain text with light formatting.\n\n"
             "The top block between the dashes is frontmatter: metadata. The name and description are all the agent "
             "keeps in context all the time. That is a few dozen tokens.\n\n"
             "When your request matches the description (or you call the skill by name), the agent loads the full "
             "body. So you can install many skills without filling the window. That is why skills add expertise "
             "cheaply.\n\n"
             "This example is simplified for the slide. Real skills can also include extra files and scripts.")

    def construct(self):
        self.prep()
        lines = [("---", DIM), ("name: grill-me", FG),
                 ("description: Interview me about a plan until every branch is resolved.", FG),
                 ("---", DIM), ("# Grill me", BLUE), ("1. Ask one question at a time.", MUTED),
                 ("2. Offer your recommended answer.", MUTED), ("3. Stop when no open branches remain.", MUTED)]
        ts = VGroup(*[T(s, 23, c, font=MONO) for s, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel = RoundedRectangle(corner_radius=0.3, width=ts.width + 1.0, height=ts.height + 0.8, stroke_color=HAIR,
                                 stroke_width=1.5, fill_color="#0C0C0E", fill_opacity=1)
        code = VGroup(panel, ts).move_to([0, 0.15, 0])
        ts.move_to(panel)
        file_lbl = T("SKILL.md", 17, MUTED, font=MONO).next_to(panel, UP, buff=0.12).align_to(panel, LEFT)
        hl = RoundedRectangle(corner_radius=0.1, width=ts.width + 0.3, height=0.45, stroke_color=GREEN, stroke_width=2.5,
                              fill_color=GREEN, fill_opacity=0.12).move_to(ts[2])
        fm_tag = T("always in context", 18, GREEN, True).next_to(hl, RIGHT, buff=0.0).shift(RIGHT * 0.0)
        fm_tag.next_to(panel, RIGHT, buff=0.2).align_to(hl, UP)
        body_tag = T("loads only when needed", 18, BLUE, True).next_to(panel, RIGHT, buff=0.2).align_to(ts[5], UP)
        take = T("Only the short description sits in context. The body loads when needed.", 25, FG).to_edge(DOWN, buff=1.0)

        self.play(FadeIn(panel), FadeIn(file_lbl), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in ts], lag_ratio=0.12), run_time=1.6)
        self.next_slide()
        self.play(Create(hl), *[ts[i].animate.set_opacity(0.35) for i in (0, 1, 3, 4, 5, 6, 7)], run_time=0.7)
        self.next_slide()
        self.play(FadeOut(hl), *[ts[i].animate.set_opacity(1) for i in (0, 1, 3, 4, 5, 6, 7)], run_time=0.5)
        self.play(*[ts[i].animate.set_opacity(0.3) for i in (0, 1, 3)], ts[2].animate.set_opacity(1), run_time=0.01)
        self.play(*[ts[i].animate.set_opacity(0.55) for i in (0, 1, 2, 3)], FadeIn(take, shift=UP * 0.2), run_time=0.6)


# ================================================================= 09 Matt Pocock skills
class S09(Deck):
    n = 9
    title = "Matt Pocock's skills"
    credit = "github.com/mattpocock/skills"
    notes = ("After installing, run /setup-matt-pocock-skills once in each repo you want to use them in.\n\n"
             "Matt Pocock publishes an open source set of skills. The install command and skill names here were "
             "checked against the live repo. Other agents (like Codex) use different install commands, listed in "
             "the repo README.\n\n"
             "grill-me: the agent interviews you about your plan until every branch of the design is settled. Great "
             "for turning a vague idea into a clear spec.\n"
             "to-spec: turns that conversation into a written spec. (Older name: to-prd, a product requirements "
             "document.)\n"
             "to-tickets: splits the spec into small tasks. (Older name: to-issues.)\n"
             "tdd: test-driven development. The agent writes a failing test first, then code to pass it. Tests "
             "become an automatic gate.\n"
             "diagnosing-bugs: a disciplined loop for hard bugs. (Older name: diagnose.)\n"
             "code-review: reviews the diff against your standards and the spec.\n\n"
             "Guardrails are covered with hooks on the guardrails slide.")

    def construct(self):
        self.prep()
        cmd = mono_pill("claude plugin install mattpocock-skills@claude-plugins-official", 22).shift(UP * 1.45)
        rows = [("grill-me   to-spec   to-tickets", "Spec, into the Prompt arrow", GREEN),
                ("tdd   diagnosing-bugs", "The Guardrails box", GREEN),
                ("code-review", "The Review step", GREEN)]
        out = []
        for i, (skills, where, c) in enumerate(rows):
            box = RoundedRectangle(corner_radius=0.22, width=11.2, height=0.95, stroke_color=HAIR, stroke_width=1.5,
                                   fill_color=CARD, fill_opacity=1)
            s = T(skills, 23, FG, True, font=MONO).move_to(box.get_left() + RIGHT * 0.4, aligned_edge=LEFT)
            w = T("→  " + where, 23, c, True).move_to(box.get_right() + LEFT * 0.4, aligned_edge=RIGHT)
            out.append(VGroup(box, s, w))
        tbl = VGroup(*out).arrange(DOWN, buff=0.22).shift(DOWN * 0.95)
        self.play(FadeIn(cmd, shift=DOWN * 0.15), run_time=0.7)
        for r in out:
            self.next_slide()
            self.play(FadeIn(r, shift=UP * 0.2), run_time=0.6)


# ================================================================= 10 demo
class S10(Deck):
    n = 10
    notes = ("Placeholder for the live demo (about 8 to 10 minutes).\n\n"
             "Plan: ask for one project idea from the audience. Run grill-me on it. Show the agent asking one "
             "question at a time and recommending answers. End by running to-spec to show the output as a written "
             "spec.\n\n"
             "Point out during the demo: this is the left side of the loop. We are improving what goes IN before any "
             "code is written.\n\n"
             "Backup plan if the network fails: have a recorded run or a pre-made transcript ready.")

    def construct(self):
        self.prep()
        d = T("DEMO", 130, FG, True).shift(UP * 0.4)
        s = T("Live: grill-me on a project idea", 34, MUTED).next_to(d, DOWN, buff=0.5)
        dot = Dot(color=RED, radius=0.14).next_to(d, UP, buff=0.5)
        self.play(FadeIn(d, scale=0.9), run_time=0.8)
        self.play(FadeIn(s, shift=UP * 0.2), FadeIn(dot), run_time=0.6)
        self.play(dot.animate.scale(1.5), rate_func=there_and_back, run_time=0.8)
        self.play(dot.animate.scale(1.5), rate_func=there_and_back, run_time=0.8)


# ================================================================= 11 environments
class S11(Deck):
    n = 11
    title = "Environments and sandboxes"
    notes = ("The environment is everything the agent can reach: your files, a shell where it runs commands, the "
             "internet, and extra tools (like a database or browser).\n\n"
             "Rule of thumb: the more you let it do on its own, the more you should fence it in.\n\n"
             "Git worktree: a second checkout of your repo in another folder, so the agent works on its own branch "
             "without touching yours.\n"
             "Container: a disposable mini computer on your machine. If the agent breaks it, you delete it.\n"
             "Cloud sandbox: the same idea, running on someone else's machine, so a mistake cannot reach your "
             "laptop at all.")

    def construct(self):
        self.prep()
        left = card("What it can touch", "", BLUE, 5.4, 3.7)
        items = ["Files", "A shell (runs commands)", "The network and tools"]
        li = VGroup(*[T(s, 25, FG) for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        li.next_to(left[2], DOWN, buff=0.4).align_to(left[2], LEFT)
        L = VGroup(left, li)
        right = card("More permission, more isolation", "", GREEN, 6.4, 3.7, title_size=25)
        steps = [("Git worktree", "its own branch folder"), ("Container", "a disposable mini computer"),
                 ("Cloud sandbox", "someone else's machine")]
        ri = VGroup(*[VGroup(T(a, 24, FG, True), T(b, 19, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
                      for a, b in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ri.next_to(right[2], DOWN, buff=0.3).align_to(right[2], LEFT)
        R = VGroup(right, ri)
        VGroup(L, R).arrange(RIGHT, buff=0.4).shift(DOWN * 0.1)
        self.play(FadeIn(L, shift=UP * 0.2), run_time=0.8)
        self.next_slide()
        self.play(FadeIn(R, shift=UP * 0.2), run_time=0.8)
        arrow = Arrow(R.get_bottom() + LEFT * 2.3 + DOWN * 0.3, R.get_bottom() + RIGHT * 2.3 + DOWN * 0.3, buff=0,
                      stroke_width=4, color=GREEN, tip_length=0.2, max_tip_length_to_length_ratio=1)
        lab = T("safer", 18, GREEN, True).next_to(arrow, DOWN, buff=0.1)
        self.play(Create(arrow), FadeIn(lab), run_time=0.6)


# ================================================================= 12 guardrails
class S12(Deck):
    n = 12
    title = "Guardrails"
    notes = ("Guardrails are checks that run whether or not the agent wants them.\n\n"
             "Permission prompts: the agent asks before risky actions. Fine for learning, tiring over time.\n"
             "Allow and deny lists: pre-approve safe commands (run tests) and block dangerous ones.\n"
             "Hooks: small scripts that run before or after a tool call. A hook can refuse a command like rm -rf "
             "(delete everything) or git push --force (overwrite shared history). This is stronger than telling the "
             "agent please do not in a prompt, because it is enforced by code.\n"
             "Tests and linters (a linter is a tool that flags style and likely bugs): the agent runs them after "
             "every change, and failures send it back to fix things before you ever look.\n\n"
             "Colors: yellow means it still depends on a person paying attention. Green means it is enforced by "
             "code, no matter what.")

    def construct(self):
        self.prep()
        cs = [card("Permission prompts", "The agent asks before risky actions.", YELLOW, 5.6, 2.2, 30),
              card("Allow and deny lists", "Pre-approve safe commands, block the rest.", YELLOW, 5.6, 2.2, 30),
              card("Hooks", "Scripts that block commands like rm -rf or a force push.", GREEN, 5.6, 2.2, 30),
              card("Tests and linters", "Automatic gates. A linter is a code checker.", GREEN, 5.6, 2.2, 30)]
        VGroup(*cs).arrange_in_grid(rows=2, cols=2, buff=0.35).shift(DOWN * 0.35)
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.6)
        for c in cs[1:]:
            self.next_slide()
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)


# ================================================================= 13 lock files
class S13(Deck):
    n = 13
    title = "Lock files"
    notes = ("A dependency is code written by someone else that your project uses. A lock file (package-lock.json, "
             "pnpm-lock.yaml, uv.lock) records the exact version of every dependency.\n\n"
             "Why it matters with agents: models sometimes invent package names that sound real. Attackers register "
             "those names with malicious code (called slopsquatting). An agent that runs install on a made-up name "
             "can pull it into your project.\n\n"
             "Defense: commit the lock file, and treat any lock file diff as suspicious. Read it line by line. Ask: "
             "do I recognize every new package? Is the name spelled correctly? Does it have real users?\n\n"
             "The snippet is a simplified diff for illustration. Real lock files are thousands of lines, which is "
             "exactly why you read the diff, not the file.")

    def construct(self):
        self.prep()
        rows = [("  \"dependencies\": {", MUTED, None), ("    \"express\": \"4.19.2\",", MUTED, None),
                ("+   \"leftpad-utils\": \"0.0.1\"", GREEN, GREEN), ("  }", MUTED, None)]
        ts = VGroup(*[T(s, 26, c, font=MONO) for s, c, _ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        panel = RoundedRectangle(corner_radius=0.3, width=ts.width + 1.2, height=ts.height + 0.9, stroke_color=HAIR,
                                 stroke_width=1.5, fill_color="#0C0C0E", fill_opacity=1).move_to([0, 0.3, 0])
        ts.move_to(panel)
        band = Rectangle(width=panel.width - 0.04, height=0.58, stroke_width=0, fill_color=GREEN,
                         fill_opacity=0.14).move_to(ts[2]).align_to(panel, LEFT).shift(RIGHT * 0.02)
        q = T("Never heard of it?", 24, YELLOW, True).next_to(panel, RIGHT, buff=-3.2).align_to(ts[2], DOWN).shift(UP * 0.0)
        q.next_to(band, DOWN, buff=0.12).align_to(ts[2], RIGHT).shift(LEFT * 0.0)
        take = T("Pinned versions mean agents cannot silently add or upgrade packages.", 25, FG).to_edge(DOWN, buff=1.5)
        take2 = T("Read every new line in the diff. Never heard of it? Stop and check.", 25, MUTED).next_to(take, DOWN, buff=0.2)
        self.play(FadeIn(panel), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in ts], lag_ratio=0.2), run_time=1.4)
        self.next_slide()
        self.play(FadeIn(band), Indicate(ts[2], color=GREEN, scale_factor=1.04), run_time=0.9)
        self.play(FadeIn(take, shift=UP * 0.2), FadeIn(take2, shift=UP * 0.2), run_time=0.6)


# ================================================================= 14 sub-agents
class S14(Deck):
    n = 14
    title = "Sub-agents are about context"
    notes = ("Sub-agents are not job titles like designer or tester. They are a way to manage context.\n\n"
             "Click 1: the main agent hands out tasks. Each sub-agent starts with a clean window and does the heavy "
             "reading (hundreds of files, long logs). Watch the small bars: that is how full each window gets.\n"
             "Click 2: only a short summary comes back. Your main agent stays in the smart zone because the noise "
             "never entered its window.\n\n"
             "Good uses: exploring an unfamiliar codebase, searching many files, reading long logs.\n"
             "Weak use: giving a sub-agent a vague task and trusting the summary blindly. The summary is only as "
             "good as what the sub-agent looked at.")

    def construct(self):
        self.prep()

        def mini_bar(w, frac, color, y):
            track = RoundedRectangle(corner_radius=0.08, width=w, height=0.16, stroke_width=0, fill_color="#2A2A2D",
                                     fill_opacity=1)
            fill = RoundedRectangle(corner_radius=0.08, width=max(w * frac, 0.05), height=0.16, stroke_width=0,
                                    fill_color=color, fill_opacity=1).align_to(track, LEFT).align_to(track, UP)
            return track, fill

        main_box = pill("Main agent", GREEN, GREEN_BG, 3.8, 0.9, size=26, r=0.28).move_to([0, 1.5, 0])
        main_sub = T("clean window", 17, MUTED).next_to(main_box, DOWN, buff=0.12)
        mt, mf = mini_bar(2.4, 0.15, GREEN, 0)
        mt.next_to(main_sub, DOWN, buff=0.12)
        mf.move_to(mt.get_left(), aligned_edge=LEFT)
        subs = []
        names = [("Sub-agent A", "reads the auth code"), ("Sub-agent B", "reads the database code"),
                 ("Sub-agent C", "reads the tests")]
        xs = [-4.1, 0, 4.1]
        sub_tracks, sub_fills = [], []
        for (a, b), x in zip(names, xs):
            bx = RoundedRectangle(corner_radius=0.22, width=3.5, height=1.1, stroke_color="#5A5A5E", stroke_width=2,
                                  fill_color=CARD, fill_opacity=1).move_to([x, -1.55, 0])
            ta = T(a, 23, FG, True).move_to(bx).shift(UP * 0.2)
            tb = T(b, 17, MUTED).move_to(bx).shift(DOWN * 0.22)
            t, f = mini_bar(2.4, 0.05, YELLOW, 0)
            t.next_to(bx, DOWN, buff=0.18)
            f.move_to(t.get_left(), aligned_edge=LEFT)
            subs.append(VGroup(bx, ta, tb))
            sub_tracks.append(t)
            sub_fills.append(f)
        down = [Arrow([x, 0.45, 0], [x, -0.95, 0], buff=0, stroke_width=3, color=MUTED, tip_length=0.18,
                      max_tip_length_to_length_ratio=1) for x in xs]
        dlab = [T("task", 17, MUTED).move_to([x + 0.5, -0.25, 0]) for x in xs]
        up = [Arrow([x - 0.7, -0.95, 0], [x - 0.7, 0.45, 0], buff=0, stroke_width=3, color=GREEN, tip_length=0.18,
                    max_tip_length_to_length_ratio=1) for x in xs]
        ulab = [T("summary", 17, GREEN, True).move_to([x - 1.5, -0.25, 0]) for x in xs]
        take = T("Each one reads a lot. Only a short result comes back.", 27, FG, True).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(main_box), FadeIn(main_sub), FadeIn(mt), FadeIn(mf), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(s) for s in subs], lag_ratio=0.2), *[FadeIn(t) for t in sub_tracks],
                  *[FadeIn(f) for f in sub_fills], run_time=1.0)
        self.next_slide()
        self.play(*[Create(a) for a in down], *[FadeIn(l) for l in dlab], run_time=0.6)
        grow = []
        for t, f in zip(sub_tracks, sub_fills):
            nf = RoundedRectangle(corner_radius=0.08, width=2.4 * 0.88, height=0.16, stroke_width=0, fill_color=RED,
                                  fill_opacity=1).move_to(t.get_left(), aligned_edge=LEFT)
            grow.append(Transform(f, nf))
        self.play(*grow, run_time=2.0, rate_func=linear)
        self.next_slide()
        self.play(*[Create(a) for a in up], *[FadeIn(l) for l in ulab], run_time=0.7)
        nmf = RoundedRectangle(corner_radius=0.08, width=2.4 * 0.22, height=0.16, stroke_width=0, fill_color=GREEN,
                               fill_opacity=1).move_to(mt.get_left(), aligned_edge=LEFT)
        small = [Transform(f, RoundedRectangle(corner_radius=0.08, width=2.4 * 0.05, height=0.16, stroke_width=0,
                                               fill_color=GREEN, fill_opacity=1).move_to(t.get_left(), aligned_edge=LEFT))
                 for t, f in zip(sub_tracks, sub_fills)]
        self.play(Transform(mf, nmf), *small, FadeIn(take, shift=UP * 0.2), run_time=1.2)


# ================================================================= 15 multi-agent
class S15(Deck):
    n = 15
    title = "Multi-agent loops"
    notes = ("Three common patterns.\n\n"
             "Fan-out: several agents investigate different questions at once and report back. Fast, good for "
             "research.\n"
             "Pipeline: one agent plans, one writes code, one reviews. Each step has a clear handoff document.\n"
             "Until it passes: the agent runs the tests, reads failures, fixes, and repeats until green. Set a cap "
             "on attempts so it cannot loop forever and burn money.\n\n"
             "The caveat in yellow is the important part. Every agent produces output, and all of it lands on a "
             "human eventually. Do not add agents just because you can.")

    def construct(self):
        self.prep()
        cs = [card("Fan-out", "Many agents research in parallel.", BLUE, 3.95, 3.0, 22, 30, 23),
              card("Pipeline", "Planner, then implementer, then reviewer.", BLUE, 3.95, 3.0, 22, 30, 23),
              card("Until it passes", "Loop until tests go green.", BLUE, 3.95, 3.0, 22, 30, 23)]
        VGroup(*cs).arrange(RIGHT, buff=0.35).shift(UP * 0.1)
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.6)
        self.next_slide()
        self.play(FadeIn(cs[1], shift=UP * 0.2), run_time=0.6)
        self.next_slide()
        self.play(FadeIn(cs[2], shift=UP * 0.2), run_time=0.6)
        warn = T("More agents means more output for you to review.", 29, YELLOW, True).to_edge(DOWN, buff=1.1)
        self.next_slide()
        self.play(FadeIn(warn, shift=UP * 0.2), run_time=0.6)


# ================================================================= 16 review
class S16(Deck):
    n = 16
    title = "Review is the bottleneck"
    notes = ("Agents make writing code cheap. Reading code is still slow, so review becomes the limit on how fast "
             "you can safely go.\n\n"
             "Read the diff: the agent's summary tells you what it intended, not what it did. Check the actual "
             "changes.\n"
             "Run it: tests only check what someone thought to test. Click through the feature yourself.\n"
             "Keep PRs small: ask the agent to work in small slices (this is what to-tickets and tdd help with). A "
             "2,000 line PR gets skimmed, and skimming is how bugs and bad dependencies ship.\n\n"
             "Multi-agent loops make this worse, not better, because more agents produce more to review. A reviewer "
             "agent can help as a first pass, but a human still signs off.")

    def construct(self):
        self.prep()
        cs = [card("Read the diff", "Every changed line, not just the summary.", GREEN, 3.95, 3.0, 22, 30, 23),
              card("Run it", "Do not trust tests pass alone.", GREEN, 3.95, 3.0, 22, 30, 23),
              card("Keep PRs small", "Big agent PRs get rubber stamped.", GREEN, 3.95, 3.0, 22, 30, 23)]
        VGroup(*cs).arrange(RIGHT, buff=0.35).shift(DOWN * 0.1)
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.6)
        for c in cs[1:]:
            self.next_slide()
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)


# ================================================================= 17 human at the end
class S17(Deck):
    n = 17
    title = "The human at the end"
    credit = AIRBNB
    notes = ("Back to the loop with the review path lit up. Look at the arrow from Review to PR. That arrow is "
             "yours.\n\n"
             "You must understand 100% of the code you merge. Not it passed the tests. Not the agent said it works. "
             "Tests only check what someone thought to test.\n\n"
             "Practical habits: read the diff, run it yourself, ask the agent to explain any line you do not follow. "
             "If you still cannot explain it, rewrite it or cut it.\n\n"
             "This is also why the whole SDLC shifts: planning and review become your main jobs, and both need real "
             "understanding.")

    def construct(self):
        self.prep()
        L = Loop(shift=UP * 0.12, scale=0.86)
        self.play(FadeIn(L.all(), lag_ratio=0.03), run_time=1.2)
        self.next_slide()
        self.play(*L.focus({"review", "pr", "e_pr", "e_cc", "l_cc", "prompt", "e_out", "l_out", "dev_region"}),
                  run_time=0.8)
        a = T("The agent opens the PR. A human merges it.", 24, FG, True).move_to([0, -2.75, 0])
        b = T("If you cannot explain a line, it does not ship.", 24, RED, True).move_to([0, -3.15, 0])
        self.play(FadeIn(a, shift=UP * 0.2), run_time=0.6)
        self.next_slide()
        self.play(FadeIn(b, shift=UP * 0.2), Indicate(L.m["pr"], color=FG, scale_factor=1.15), run_time=0.8)


# ================================================================= 18 questions
class S18(Deck):
    n = 18
    notes = ("Open the floor. Resources are listed on the slide.\n\n"
             "The HumanLayer repo is Dex Horthy's material on context engineering for coding agents.\n\n"
             "Closing thought: agents are good at the middle of the loop. You are responsible for the two ends.")

    def construct(self):
        self.prep()
        q = T("Questions?", 100, FG, True).shift(UP * 1.0)
        l1 = T("github.com/mattpocock/skills", 26, MUTED, font=MONO)
        l2 = T("github.com/humanlayer/advanced-context-engineering-for-coding-agents", 22, MUTED, font=MONO)
        l3 = T("Dex Horthy, HumanLayer", 18, DIM)
        links = VGroup(l1, l2, l3).arrange(DOWN, buff=0.28).next_to(q, DOWN, buff=0.9)
        self.play(FadeIn(q, shift=UP * 0.3), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in links], lag_ratio=0.25), run_time=1.2)
