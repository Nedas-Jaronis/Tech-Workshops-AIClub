# Agents 101 (Manim Slides)

Animated deck, one scene per slide in `deck.py` (S01 to S21). Speaker notes are embedded.

## Run it
    .\render.ps1 -Quality hd      # 1080p, takes a few minutes (use -Quality preview for fast drafts)
    .\present.ps1                 # fullscreen: space / right arrow = next, left arrow = back, q = quit
    .\present.ps1 -Web            # export agents101.html, open in any browser

Re-render only what you changed: `.\render.ps1 -Slides S06,S14`.

## Notes
- Manim is pinned below 0.20 because manim-slides 5.7 does not work with 0.22.
- Colors and fonts live at the top of `deck.py` (Nunito, Consolas).
