# osu-ai-mapper

Helyi, magyar jegyzet az [OliBomby Mapperatorinator](https://github.com/OliBomby/Mapperatorinator) modellhez. osu! beatmapet készít mind a négy játékmódra. A környezet uv-val van kezelve, a számítás NVIDIA GPU-n fut (RTX 3090 és 4090 is).

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

Dupla kattintás: `scripts\start.bat`

```powershell
.\scripts\start.ps1
```

A notebookban a cellákat fentről lefelé futtasd. Az első generálás a modellt a Hugging Face-ről tölti le, ez több gigabájt.

## Git-függőségek

A `slider` Python-könyvtár uv git-függőség, commitra rögzítve a `pyproject.toml`-ban. A `uv sync` tölti le.

A Mapperatorinator nem telepíthető csomag, ezért git almodul a `Mapperatorinator` mappában, egy rögzített commiton. Friss klón után az `install.ps1` a `git submodule update --init` paranccsal hozza le.

## Mi nincs a repóban

A virtuális környezet, az FFmpeg, a legenerált beatmapek, a `beallitasok.json` és a Hugging Face-ről letöltött modellek nincsenek verziókezelve. Ezeket a telepítő vagy az első generálás hozza létre.
