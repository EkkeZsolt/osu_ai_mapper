# Telepíti a 64 bites Python-t, a CUDA-s függőségeket, a Mapperatorinatort és az FFmpeget.
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$gyoker = Split-Path -Parent $PSScriptRoot
Set-Location $gyoker

function Kell-Parancs([string]$nev, [string]$hiba) {
    if (-not (Get-Command $nev -ErrorAction SilentlyContinue)) {
        throw $hiba
    }
}

Kell-Parancs "uv" "Az uv nincs a PATH-on. Telepítés: https://docs.astral.sh/uv/"
Kell-Parancs "git" "A git nincs a PATH-on."

Write-Host "64 bites Python 3.12 telepítése..."
uv python install "cpython-3.12.14-windows-x86_64-none"

Write-Host "Python-függőségek telepítése (uv sync)..."
uv sync

$repo = Join-Path $gyoker "Mapperatorinator"
if (-not (Test-Path (Join-Path $repo "inference.py"))) {
    Write-Host "Mapperatorinator almodul letöltése..."
    git submodule update --init --depth 1
}

$ffmpegExe = Join-Path $gyoker "eszkozok\ffmpeg\bin\ffmpeg.exe"
$ffprobeExe = Join-Path $gyoker "eszkozok\ffmpeg\bin\ffprobe.exe"
if (-not ((Test-Path $ffmpegExe) -and (Test-Path $ffprobeExe))) {
    Write-Host "FFmpeg 7.1 letöltése..."
    $eszkozok = Join-Path $gyoker "eszkozok"
    New-Item -ItemType Directory -Force -Path $eszkozok | Out-Null
    $zip = Join-Path $eszkozok "ffmpeg.zip"
    $url = "https://github.com/GyanD/codexffmpeg/releases/download/7.1.1/ffmpeg-7.1.1-full_build-shared.zip"
    curl.exe -L --fail -o $zip $url
    if ($LASTEXITCODE -ne 0) {
        throw "Az FFmpeg letöltése sikertelen."
    }
    Expand-Archive -Path $zip -DestinationPath $eszkozok -Force
    $kibontott = Get-ChildItem $eszkozok -Directory | Where-Object { $_.Name -like "ffmpeg-*" } | Select-Object -First 1
    if (-not $kibontott) {
        throw "Az FFmpeg csomag kibontása nem hozott létre mappát."
    }
    $cel = Join-Path $eszkozok "ffmpeg"
    if (Test-Path $cel) {
        Remove-Item $cel -Recurse -Force
    }
    Rename-Item $kibontott.FullName "ffmpeg"
    Remove-Item $zip -Force
}

Write-Host "Jupyter-kernel regisztrálása..."
uv run python -m ipykernel install --user --name "osu-ai-mapper" --display-name "osu-ai-mapper (uv)"

Write-Host "A telepítés kész. Indítás: .\scripts\start.ps1"
