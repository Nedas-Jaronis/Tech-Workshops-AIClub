# One-time setup for the Manim deck on a new Windows laptop.
# Makes a virtual environment, installs ..\requirements.txt into it, then renders all slides at 1080p.
#   .\setup.ps1              full setup (the render takes several minutes)
#   .\setup.ps1 -SkipRender  install only, render later with .\render.ps1
param([switch]$SkipRender)
Set-Location $PSScriptRoot

function Need($cmd, $help) {
  if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
    Write-Host "Missing: $cmd. $help" -ForegroundColor Red
    exit 1
  }
}
Need python 'Install Python 3.11 to 3.13 from python.org and tick "Add python.exe to PATH".'
Need ffmpeg 'Install FFmpeg, for example: winget install Gyan.FFmpeg  (then open a new terminal).'

if (-not (Test-Path .venv)) {
  Write-Host "Creating virtual environment..."
  python -m venv .venv
  if ($LASTEXITCODE -ne 0) { Write-Host "Could not create the virtual environment." -ForegroundColor Red; exit 1 }
}

Write-Host "Installing packages (a few minutes, PySide6 is large)..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r ..\requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Host "Package install failed." -ForegroundColor Red; exit 1 }

if (-not $SkipRender) {
  Write-Host "Rendering all slides at 1080p (several minutes)..."
  .\render.ps1 -Quality hd
}
Write-Host ""
Write-Host "Done. Present with present.bat (or .\present.ps1)." -ForegroundColor Green
