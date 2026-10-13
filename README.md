# osu-ai-mapper

Helyi jegyzet az [OliBomby Mapperatorinator](https://github.com/OliBomby/Mapperatorinator) modellhez. osu! beatmapet készít mind a négy játékmódra. A környezet uv-val van kezelve, a számítás NVIDIA GPU-n fut (RTX 3090 és 4090 is).

Az angol leírás a `README.en.md` fájlban van. A magyar jegyzet a `mapperatorinator_inference.ipynb`, az angol a `mapperatorinator_inference_en.ipynb`.

A mesterséges intelligencia használatát a beatmapben mindig jelezd.

## Telepítés

Kell hozzá a [Git](https://git-scm.com/) és az [uv](https://docs.astral.sh/uv/), plusz egy NVIDIA-driver, ami a CUDA 12.8-at kezeli.

Dupla kattintás: `scripts\install.bat`

PowerShellből, a projekt mappájából:

```powershell
.\scripts\install.ps1
```

Ez felteszi a 64 bites Python 3.12-t, a CUDA-s PyTorchot és a többi Python-csomagot, letölti a git-függőségeket, az FFmpeg 7.1 shared buildet, és regisztrálja a Jupyter-kernelt.

## Indítás

Streamlit: `start.bat` vagy `.\start.ps1`

Angol Streamlit: `scripts\start-en.bat` vagy `.\scripts\start-en.ps1`

Jegyzet (ipynb): `scripts\start-ipynb.bat` vagy `.\scripts\start-ipynb.ps1`

A Streamlitben a folyamat a gomb alatti naplóban látszik. Az első generálás a modellt a Hugging Face-ről tölti le, ez több gigabájt.

## Git-függőségek

A `slider` Python-könyvtár uv git-függőség, commitra rögzítve a `pyproject.toml`-ban. A `uv sync` tölti le.

A Mapperatorinator nem telepíthető csomag, ezért git almodul a `Mapperatorinator` mappában, egy rögzített commiton. Friss klón után az `install.ps1` a `git submodule update --init` paranccsal hozza le.

## Mi nincs a repóban

A virtuális környezet, az FFmpeg, a legenerált beatmapek, a `beallitasok.json` és a Hugging Face-ről letöltött modellek nincsenek verziókezelve. Ezeket a telepítő vagy az első generálás hozza létre.
