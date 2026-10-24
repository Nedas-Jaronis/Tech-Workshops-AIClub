# Agents 101 (Manim Slides)

Animated deck for Gator Hack V. One scene per slide in `deck.py` (S01 to S21). Speaker notes are embedded
(`notes.json`). Windows only.

## New laptop: set it up and run it

1. Install **Python 3.11 to 3.13** from python.org (tick "Add python.exe to PATH").
2. Install **FFmpeg**: `winget install Gyan.FFmpeg`, then open a new terminal.
3. Get the repo and open the `GatorHacks\manim` folder.
4. Double-click **`setup.bat`**. It makes a virtual environment, installs `..\requirements.txt` into it and
   renders all 21 slides at 1080p. Allow 15 to 30 minutes, most of it the render.
5. Double-click **`present.bat`**.

While presenting: space or right arrow = next, left arrow = back, `q` = quit.

Slides scale to fit any screen size (`present.py` patches the player, which otherwise assumes a 1920x1080 screen).
On a projector over HDMI: in Windows "Duplicate" mode use `present.bat`; in "Extend" mode use **`present-hdmi.bat`**
(slides on the projector, speaker notes on the laptop).

## Everyday commands

    .\render.ps1 -Quality hd        # 1080p (use this for the talk)
    .\render.ps1 -Quality preview   # fast 480p draft
    .\render.ps1 -Slides S06,S14    # re-render only some slides
    .\present.ps1                   # fullscreen presenter (same as present.bat)
    .\present.ps1 -Web              # export agents101.html for any browser (same as present-web.bat)

## Notes

- The rendered videos (`media/`, `slides/`) and the virtual environment (`.venv/`) are not in git. Run
  `setup.bat` or `render.ps1` to rebuild them.
- Packages are pinned in `..\requirements.txt`: Manim below 0.20 (manim-slides 5.7 does not work with newer
  Manim) and Pillow below 11.3 (otherwise Manim cannot draw the logo).
- Colors, fonts and layout live at the top of `deck.py`. Fonts are in `fonts/` (Nunito is used, Jost is kept
  to switch back).
- The older Slidev version of the deck is in the parent folder (`npm install`, then `npm run dev`).
