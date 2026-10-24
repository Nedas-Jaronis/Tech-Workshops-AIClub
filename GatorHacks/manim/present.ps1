# Present the rendered deck fullscreen. Arrow keys / space to advance, q to quit.
# Add -Web to export a self-contained HTML file instead (open it in any browser).
param([switch]$Web)
Set-Location $PSScriptRoot
$slides = 1..21 | ForEach-Object { "S{0:D2}" -f $_ }
if ($Web) {
  & .\.venv\Scripts\manim-slides.exe convert --to html @slides agents101.html
  Write-Host "Wrote agents101.html"
} else {
  & .\.venv\Scripts\manim-slides.exe present --full-screen @slides
}
