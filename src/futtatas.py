"""Mapperatorinator-generálás a Streamlit felület és a tesztek számára."""

from __future__ import annotations

import os
import sys
import time
import traceback
from pathlib import Path

PROJEKT = Path(__file__).resolve().parent.parent
REPO = PROJEKT / "Mapperatorinator"
FFMPEG_BIN = PROJEKT / "eszkozok" / "ffmpeg" / "bin"
KIMENET = PROJEKT / "kimenet"
TESZT = PROJEKT / "teszt"

HANG_KITERJESZTES = {".mp3", ".ogg", ".wav", ".flac", ".m4a"}


def teszt_hang() -> Path | None:
    if not TESZT.is_dir():
        return None
    fajlok = [ut for ut in TESZT.iterdir() if ut.suffix.lower() in HANG_KITERJESZTES]
    return sorted(fajlok, key=lambda ut: ut.name.casefold())[0] if fajlok else None


def normalizal_kimenet(modell: str, kimenet: list[str]) -> tuple[list[str], bool]:
    """A V32 sablonja timing+map+sv, külön kiai kimenet nélkül."""
    if modell in ("v32", "v32-mini") and "kiai" in kimenet:
        tisztitott = [elem for elem in kimenet if elem != "kiai"] or ["timing", "map", "sv"]
        return tisztitott, True
    return kimenet, False


def _szoveg(ertek: str | None) -> str | None:
    ertek = (ertek or "").strip()
    return ertek or None


def _szam(ertek, egesz: bool = False):
    if ertek is None or ertek == -1:
        return None
    return int(ertek) if egesz else float(ertek)


def _kontextus(szoveg: str):
    from osuT5.osuT5.event import ContextType

    belso = szoveg.strip()[1:-1]
    if not belso or belso.upper() == "NONE":
        return [ContextType.NONE]
    return [ContextType[resz.strip().upper()] for resz in belso.split(",") if resz.strip()]


class _Naplo:
    encoding = "utf-8"

    def __init__(self, eredeti, frissit):
        self.eredeti = eredeti
        self.frissit = frissit
        self._darab = ""
        self._sorok: list[str] = []
        self._utolso = 0.0

    def write(self, szoveg):
        if not szoveg:
            return
        try:
            sys.__stdout__.write(szoveg)
        except Exception:
            pass
        self._darab += szoveg
        if "\r" not in self._darab and "\n" not in self._darab:
            return
        darabok = self._darab.replace("\r", "\n").split("\n")
        self._darab = darabok[-1]
        most = time.monotonic()
        valtozott = False
        for sor in darabok[:-1]:
            sor = sor.strip()
            if not sor:
                continue
            folyamat = "%" in sor or "it/s" in sor or "MB/s" in sor
            if folyamat and most - self._utolso < 1.0:
                continue
            if folyamat:
                self._utolso = most
            self._sorok.append(sor)
            valtozott = True
        if valtozott and self.frissit is not None:
            try:
                self.frissit("\n".join(self._sorok[-40:]))
            except Exception:
                pass

    def flush(self):
        if self._darab.strip():
            self._sorok.append(self._darab.strip())
            self._darab = ""
            if self.frissit is not None:
                try:
                    self.frissit("\n".join(self._sorok[-40:]))
                except Exception:
                    pass
        try:
            sys.__stdout__.flush()
        except Exception:
            pass

    def isatty(self):
        return True

    def writable(self):
        return True

    def __getattr__(self, nev):
        return getattr(self.eredeti, nev)


def elokeszit():
    os.environ.setdefault("WANDB_MODE", "disabled")
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    if not (REPO / "inference.py").exists():
        raise RuntimeError("Hiányzik a Mapperatorinator almodul. Futtasd: .\\scripts\\install.ps1")
    if not (FFMPEG_BIN / "ffmpeg.exe").exists():
        raise RuntimeError("Hiányzik az FFmpeg. Futtasd: .\\scripts\\install.ps1")
    if str(FFMPEG_BIN) not in os.environ.get("PATH", ""):
        os.environ["PATH"] = str(FFMPEG_BIN) + os.pathsep + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(str(FFMPEG_BIN))
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        from pydub import AudioSegment

        AudioSegment.converter = str(FFMPEG_BIN / "ffmpeg.exe")
        AudioSegment.ffprobe = str(FFMPEG_BIN / "ffprobe.exe")
    import inference  # noqa: F401


def futtat(beallitas: dict, frissit=None, megnyit: bool = True) -> Path:
    if not beallitas.get("elfogadva"):
        raise RuntimeError("A generálás előtt fogadd el a szabályt.")

    hang = _szoveg(beallitas.get("hang"))
    beatmap = _szoveg(beallitas.get("beatmap"))
    kimenet = _szoveg(beallitas.get("kimenet")) or str(KIMENET)
    if not hang and not beatmap:
        raise RuntimeError("Adj meg egy hangfájlt, vagy egy .osu-t, ami mellett ott a dal.")
    if hang and not Path(hang).is_file():
        raise RuntimeError(f"A hangfájl nem található: {hang}")
    if beatmap and (not Path(beatmap).is_file() or Path(beatmap).suffix.lower() != ".osu"):
        raise RuntimeError("A referenciának létező .osu fájlnak kell lennie.")
    if hang and Path(hang).suffix.lower() not in HANG_KITERJESZTES:
        raise RuntimeError("A hang legyen mp3, ogg, wav, flac vagy m4a.")

    kezdet = _szam(beallitas.get("kezdet"), egesz=True)
    veg = _szam(beallitas.get("veg"), egesz=True)
    if kezdet is not None and veg is not None and kezdet >= veg:
        raise RuntimeError("A szakasz vége később legyen, mint a kezdete.")

    modell = beallitas.get("modell", "v32")
    elokeszit()
    from hydra import compose, initialize_config_dir
    from hydra.core.global_hydra import GlobalHydra
    from osuT5.osuT5.event import ContextType

    import inference

    kimenet_nevek = [elem.value for elem in _kontextus(beallitas.get("kimenet_tipus", "[TIMING,MAP,SV]"))]
    kimenet_nevek, kiai_kimaradt = normalizal_kimenet(modell, kimenet_nevek)
    kontextus = _kontextus(beallitas.get("kontextus", "[NONE]"))
    kimenet_tipus = [ContextType(nev) for nev in kimenet_nevek]

    cimkek = [cimke for cimke in beallitas.get("cimkek") or [] if cimke] or None
    negativ = [cimke for cimke in beallitas.get("negativ") or [] if cimke] or None
    if modell == "v30":
        if int(beallitas.get("jatekmod", 0)) != 0:
            raise RuntimeError("A V30 csak osu!standard mapot tud.")
        kimenet_tipus = [ContextType.MAP]
        cimkek = None
        negativ = None

    kell_referencia = bool(beallitas.get("hozzaad")) or any(
        elem in kontextus
        for elem in (
            ContextType.TIMING,
            ContextType.KIAI,
            ContextType.MAP,
            ContextType.SV,
            ContextType.GD,
            ContextType.NO_HS,
        )
    )
    if kell_referencia and not beatmap:
        raise RuntimeError("Ehhez a beállításhoz kell egy referencia .osu.")
    if beallitas.get("felulir") and not beatmap:
        raise RuntimeError("Felülíráshoz kell a referencia .osu.")

    Path(kimenet).mkdir(parents=True, exist_ok=True)
    if GlobalHydra.instance().is_initialized():
        GlobalHydra.instance().clear()
    config_dir = (REPO / "configs" / "inference").resolve().as_posix()
    with initialize_config_dir(version_base="1.1", config_dir=config_dir):
        conf = compose(config_name=modell)

    conf.audio_path = hang or ""
    conf.output_path = kimenet
    conf.beatmap_path = beatmap or ""
    conf.gamemode = int(beallitas.get("jatekmod", 0))
    conf.difficulty = _szam(beallitas.get("nehezseg", 5))
    conf.mapper_id = _szam(beallitas.get("mapper_id", -1), egesz=True)
    conf.year = _szam(beallitas.get("ev", 2023), egesz=True)
    conf.lora_path = _szoveg(beallitas.get("lora"))
    conf.hitsounded = bool(beallitas.get("hitsounded", True))
    conf.hp_drain_rate = _szam(beallitas.get("hp", 5))
    conf.circle_size = _szam(beallitas.get("cs", 4))
    conf.overall_difficulty = _szam(beallitas.get("od", 9))
    conf.approach_rate = _szam(beallitas.get("ar", 8))
    conf.slider_multiplier = _szam(beallitas.get("sv", 1.4))
    conf.slider_tick_rate = _szam(beallitas.get("slider_tick", 1))
    conf.keycount = int(beallitas.get("billentyu", 4))
    conf.hold_note_ratio = _szam(beallitas.get("hold", -1))
    conf.scroll_speed_ratio = _szam(beallitas.get("scroll", -1))
    conf.descriptors = cimkek
    conf.negative_descriptors = negativ
    conf.export_osz = bool(beallitas.get("osz", True))
    conf.add_to_beatmap = bool(beallitas.get("hozzaad", False))
    conf.overwrite_reference_beatmap = bool(beallitas.get("felulir", False))
    conf.start_time = kezdet
    conf.end_time = veg
    conf.in_context = kontextus
    conf.output_type = kimenet_tipus
    conf.cfg_scale = float(beallitas.get("cfg", 1))
    conf.temperature = float(beallitas.get("homerseklet", 0.9))
    conf.seed = _szam(beallitas.get("seed", -1), egesz=True)
    conf.timing_leniency = int(beallitas.get("timing_tures", 20))
    conf.super_timing = bool(beallitas.get("super_timing", False))
    conf.timer_num_beams = int(beallitas.get("sugarak", 2))
    conf.timer_iterations = int(beallitas.get("iteraciok", 20))
    conf.timer_bpm_threshold = float(beallitas.get("bpm_kuszob", 0.1))
    conf.use_server = False
    conf.title = _szoveg(beallitas.get("cim"))
    conf.artist = _szoveg(beallitas.get("eloado"))
    conf.creator = _szoveg(beallitas.get("keszito")) or "Mapperatorinator"
    conf.version = _szoveg(beallitas.get("verzio")) or "AI"
    conf.source = _szoveg(beallitas.get("forras"))
    conf.background = _szoveg(beallitas.get("hatter"))

    if kiai_kimaradt and frissit is not None:
        frissit("A V32 nem generál külön kiai sávot. A kimenet timing, objektumok és SV.\n")

    eredeti_konyvtar = os.getcwd()
    eredeti_ki, eredeti_be = sys.stdout, sys.stderr
    sys.stdout = _Naplo(eredeti_ki, frissit)
    sys.stderr = _Naplo(eredeti_be, frissit)
    os.chdir(REPO)
    try:
        eredmeny = inference.main(conf)
    except Exception:
        if frissit is not None:
            frissit(traceback.format_exc())
        raise
    finally:
        sys.stdout = eredeti_ki
        sys.stderr = eredeti_be
        os.chdir(eredeti_konyvtar)

    if not isinstance(eredmeny, tuple) or len(eredmeny) != 2:
        raise RuntimeError(f"A generálás nem adott vissza fájlt: {eredmeny!r}")
    utvonal = Path(eredmeny[1])
    if megnyit:
        try:
            os.startfile(utvonal.parent)
        except OSError:
            pass
    return utvonal
