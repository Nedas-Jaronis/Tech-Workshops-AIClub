# Runs manim-slides, but makes the slides fit any screen.
# manim-slides 5.7 pins the player to the render size (1920x1080), so on a small or high-DPI laptop
# (for example 3200x2000 at 250% scaling, which Qt sees as 1280x800) the slides overflow the screen.
# Used by present.ps1:  python present.py present --full-screen S01 S02 ...
import sys

from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap

import manim_slides.present.player as player_module
from manim_slides.__main__ import cli

_players = []


class FitPixmap(QPixmap):
    # Still slides are drawn as a pixmap scaled to the render width. Scale to the window instead.
    def scaledToWidth(self, *args, **kwargs):
        if not _players:
            return super().scaledToWidth(*args, **kwargs)
        p = _players[-1]
        size = p.centralWidget().size() if p.isVisible() else p.screen().size()
        dpr = p.devicePixelRatioF()
        out = self.scaled(size * dpr, Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        out.setDevicePixelRatio(dpr)
        return out


_init = player_module.Player.__init__


def _fit_init(self, *args, **kwargs):
    _players.append(self)
    _init(self, *args, **kwargs)
    # Let the window shrink to the screen instead of staying at least 1920x1080.
    self.image_label.setMinimumSize(1, 1)
    self.media_stack.setMinimumSize(1, 1)


player_module.QPixmap = FitPixmap
player_module.Player.__init__ = _fit_init

if __name__ == "__main__":
    sys.argv[0] = "manim-slides"
    cli()
