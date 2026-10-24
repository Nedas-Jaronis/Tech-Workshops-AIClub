# Present the rendered deck fullscreen. Arrow keys / space to advance, q to quit.
# The slides scale to fit whatever screen they are on (see present.py).
#   .\present.ps1              present on the main screen (or a duplicated HDMI screen)
#   .\present.ps1 -Screen 1    slides on the second screen (HDMI in "Extend" mode), notes on the laptop
# Add -Web to export a self-contained HTML file instead (open it in any browser).
param([switch]$Web, [int]$Screen = -1)
Set-Location $PSScriptRoot
$slides = 1..21 | ForEach-Object { "S{0:D2}" -f $_ }
if ($Web) {
  & .\.venv\Scripts\manim-slides.exe convert --to html @slides agents101.html
  Write-Host "Wrote agents101.html"
} else {
  $extra = if ($Screen -ge 0) { @("--screen", $Screen) } else { @() }
  & .\.venv\Scripts\python.exe present.py present --full-screen @extra @slides
}
