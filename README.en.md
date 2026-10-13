# osu-ai-mapper

Local notebook for [OliBomby's Mapperatorinator](https://github.com/OliBomby/Mapperatorinator). It generates osu! beatmaps for all four gamemodes. The environment is managed with uv and runs on an NVIDIA GPU (RTX 3090 and 4090).

The Hungarian readme is `README.md`. The Hungarian notebook is `mapperatorinator_inference.ipynb`, and the English notebook is `mapperatorinator_inference_en.ipynb`.

Always disclose the use of AI in your beatmaps.

## Install

You need [Git](https://git-scm.com/), [uv](https://docs.astral.sh/uv/), and an NVIDIA driver that supports CUDA 12.8.

Double-click `scripts\install.bat`, or from PowerShell in the project folder:

```powershell
.\scripts\install.ps1
```

This installs 64-bit Python 3.12, the CUDA build of PyTorch and the other Python packages, fetches the git dependencies, downloads the FFmpeg 7.1 shared build, and registers the Jupyter kernel.

## Start

Streamlit: `start.bat` or `.\start.ps1`

English Streamlit: `scripts\start-en.bat` or `.\scripts\start-en.ps1`

Notebook (ipynb): `scripts\start-ipynb.bat` or `.\scripts\start-ipynb.ps1`

In Streamlit, progress appears in the log under the button. The first generation downloads the model from Hugging Face, which is several gigabytes.

## Git dependencies

`slider` is a uv git dependency, pinned to a commit in `pyproject.toml`. `uv sync` downloads it.

Mapperatorinator is not an installable package, so it is a git submodule in the `Mapperatorinator` folder, pinned to a commit. On a fresh clone, `install.ps1` fetches it with `git submodule update --init`.

## Not in the repository

The virtual environment, FFmpeg, generated beatmaps, `beallitasok.json`, and the Hugging Face models are not versioned. The installer or the first generation creates them.
