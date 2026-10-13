# A Mapperatorinator notebook indítása az uv környezetből.
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

uv run jupyter lab "mapperatorinator_inference.ipynb"
