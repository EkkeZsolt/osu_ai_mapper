# A Mapperatorinator Streamlit felületének indítása.
param(
    [ValidateSet("hu", "en", "de", "ru")]
    [string]$Nyelv = "hu"
)

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

$env:OSU_AI_LANG = $Nyelv
uv run streamlit run src/app.py --browser.gatherUsageStats false
