# Render the deck. Usage:  .\render.ps1 [-Quality preview|hd|4k] [-Slides S01,S02]
# preview = fast 480p, check = 720p for proofing, hd = 1080p (use this for the workshop), 4k = 3840x2160
param(
  [ValidateSet("preview", "check", "hd", "4k")][string]$Quality = "hd",
  [string[]]$Slides = (1..20 | ForEach-Object { "S{0:D2}" -f $_ })
)
Set-Location $PSScriptRoot
$flags = switch ($Quality) {
  "preview" { @("-r", "854,480", "--fps", "15") }
  "check"   { @("-r", "1280,720", "--fps", "15") }
  "hd"      { @("-r", "1920,1080", "--fps", "30") }
  "4k"      { @("-r", "3840,2160", "--fps", "30") }
}
& .\.venv\Scripts\manim-slides.exe render @flags deck.py @Slides
