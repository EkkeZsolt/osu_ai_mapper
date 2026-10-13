# Jupyter notebook (ipynb) indítása.
# mapperatorinator_inference.ipynb és mapperatorinator_inference_en.ipynb
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$gyoker = Split-Path -Parent $PSScriptRoot
Set-Location $gyoker

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "Az uv nincs a PATH-on. Telepítés: https://docs.astral.sh/uv/"
}

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Error "Még nincs telepítve a környezet. Futtasd: .\scripts\install.ps1"
}

Write-Host "ipynb: mapperatorinator_inference.ipynb, mapperatorinator_inference_en.ipynb"
uv run jupyter lab --LabApp.extension_manager=readonly "mapperatorinator_inference.ipynb"
