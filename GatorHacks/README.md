# Agents 101: Gator Hack V workshop

How to actually work with AI coding agents. Presented by Nedas Jaronis, AI2 Club.

There are two versions of the same deck.

## 1. Animated deck (Manim Slides) in `manim/`

The one used for the talk. See `manim/README.md`. Quick start on a new Windows laptop:

1. Install Python 3.11 to 3.13 and FFmpeg (`winget install Gyan.FFmpeg`).
2. Double-click `manim\setup.bat` (installs `requirements.txt` and renders the slides).
3. Double-click `manim\present.bat`.

## 2. Slidev version (this folder)

An earlier, simpler web version of the same talk.

    npm install
    npm run dev     # opens http://localhost:3030
    npm run export  # PDF (needs: npm i -D playwright-chromium)
