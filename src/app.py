"""Helyi Mapperatorinator felület. Magyar és angol."""

from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st

import futtatas

PROJEKT = Path(__file__).resolve().parent.parent
CIMKEK = PROJEKT / "temp" / "cimkek_hu.json"
TAGEK = PROJEKT / "Mapperatorinator" / "datasets" / "tags_2026.json"

SZOVEG = {
    "hu": {
        "cim": "Beatmap generálása",
        "szabaly": "A mesterséges intelligencia használatát a beatmapben mindig jelzem.",
        "elfogadom": "Elfogadom",
        "nyelv": "Nyelv",
        "feladat": "Feladat",
        "hang": "Hang",
        "hang_sugo": "Üresen maradhat, ha a dal a .osu mellett van. A teszt mappa dala az alapértelmezett.",
        "feltoltes": "Vagy tölts fel egy hangfájlt",
        "beatmap": "Referencia .osu",
        "beatmap_sugo": "In-contexthez és szakasz újraíráshoz kell. Stable: File → Open Song Folder. Lazer: File → Edit Externally.",
        "kimenet": "Kimeneti mappa",
        "modell": "Modell",
        "modell_sugo": "A V32 a legjobb. A V30 csak osu!standardot tud, címke és in-context nélkül.",
        "mod": "Játékmód",
        "nehezseg": "Csillagérték",
        "nehezseg_sugo": "−1: ismeretlen. A végeredmény eltérhet.",
        "mapper": "Mapper azonosító",
        "ev": "Év",
        "lora": "LoRA",
        "cimkek": "Címkék",
        "cimkek_sugo": "Üresen a modell dönt, vagy a referencia címkéi maradnak.",
        "negativ": "Negatív címkék",
        "negativ_sugo": "Csak cfg > 1 mellett hatnak.",
        "minden": "Minden játékmód címkéje",
        "nehezseg_panel": "Nehézségi számok",
        "generalas_panel": "Generálás",
        "meta": "Metaadatok",
        "kontextus": "Kontextus",
        "kimenet_tipus": "Kimenet",
        "hozzaad": "Hozzáírás a referencia maphoz",
        "osz": ".osz csomag",
        "felulir": "Az eredeti .osu felülírása",
        "kezdet": "Kezdet (ms), −1 = eleje",
        "veg": "Vége (ms), −1 = vége",
        "cfg": "Cfg",
        "homerseklet": "Hőmérséklet",
        "seed": "Seed, −1 = véletlen",
        "timing": "Timing tűrés (ms)",
        "super": "Szuper timing",
        "sugarak": "Szuper timing sugarak",
        "iteraciok": "Szuper timing ismétlések",
        "bpm": "BPM-váltás küszöbe",
        "hp": "HP",
        "cs": "CS",
        "od": "OD",
        "ar": "AR",
        "sv": "SV",
        "tick": "Slider tick",
        "kulcs": "Mania kulcsok",
        "hold": "Hold arány, −1 = automatikus",
        "scroll": "Scroll arány, −1 = automatikus",
        "hitsound": "Hitsound",
        "dalcim": "Cím",
        "eloado": "Előadó",
        "keszito": "Készítő",
        "verzio": "Nehézség neve",
        "forras": "Forrás",
        "gomb": "Beatmap generálása",
        "folyamat": "Generálás",
        "kesz": "Kész",
        "hiba": "Hiba",
        "nincs": "nincs",
    },
    "en": {
        "cim": "Generate a beatmap",
        "szabaly": "I will disclose the use of AI in the beatmap.",
        "elfogadom": "I accept",
        "nyelv": "Language",
        "feladat": "Task",
        "hang": "Audio",
        "hang_sugo": "Leave empty if the audio sits next to the .osu. The file in teszt/ is the default.",
        "feltoltes": "Or upload an audio file",
        "beatmap": "Reference .osu",
        "beatmap_sugo": "Required for in-context options and for remapping a section.",
        "kimenet": "Output folder",
        "modell": "Model",
        "modell_sugo": "V32 is the best model. V30 is osu!standard only, without descriptors or in-context.",
        "mod": "Game mode",
        "nehezseg": "Star rating",
        "nehezseg_sugo": "-1 leaves it unknown. The result can deviate.",
        "mapper": "Mapper ID",
        "ev": "Year",
        "lora": "LoRA",
        "cimkek": "Descriptors",
        "cimkek_sugo": "Leave empty and the model decides, or the reference tags stay.",
        "negativ": "Negative descriptors",
        "negativ_sugo": "Only applied when cfg is greater than 1.",
        "minden": "Tags for every mode",
        "nehezseg_panel": "Difficulty",
        "generalas_panel": "Generation",
        "meta": "Metadata",
        "kontextus": "In context",
        "kimenet_tipus": "Output",
        "hozzaad": "Add to the reference map",
        "osz": ".osz package",
        "felulir": "Overwrite the original .osu",
        "kezdet": "Start (ms), -1 = beginning",
        "veg": "End (ms), -1 = end of the song",
        "cfg": "Cfg",
        "homerseklet": "Temperature",
        "seed": "Seed, -1 = random",
        "timing": "Timing leniency (ms)",
        "super": "Super timing",
        "sugarak": "Super timing beams",
        "iteraciok": "Super timing iterations",
        "bpm": "BPM-change threshold",
        "hp": "HP",
        "cs": "CS",
        "od": "OD",
        "ar": "AR",
        "sv": "SV",
        "tick": "Slider tick",
        "kulcs": "Mania key count",
        "hold": "Hold note ratio, -1 = automatic",
        "scroll": "Scroll speed ratio, -1 = automatic",
        "hitsound": "Hitsounds",
        "dalcim": "Title",
        "eloado": "Artist",
        "keszito": "Creator",
        "verzio": "Version",
        "forras": "Source",
        "gomb": "Generate beatmap",
        "folyamat": "Generating",
        "kesz": "Done",
        "hiba": "Error",
        "nincs": "none",
    },
}

FELADATOK = {
    "uj": {
        "hu": "Új beatmap",
        "en": "New beatmap",
        "leiras_hu": "Timing, kiai nélkül: objektumok és slider velocity. A V32 ezt a hármat tudja. Elég a hang.",
        "leiras_en": "Timing, hit objects, and slider velocity. V32 has no separate kiai output. Audio is enough.",
        "kontextus": "[NONE]",
        "kimenet": "[TIMING,MAP,SV]",
        "hozzaad": False,
        "osz": True,
        "super": False,
    },
    "timing": {
        "hu": "Csak timing",
        "en": "Timing only",
        "leiras_hu": "Lassabb, pontosabb szuper timing. Változó BPM-hez.",
        "leiras_en": "Slower, more accurate super timing. Use this for variable BPM.",
        "kontextus": "[NONE]",
        "kimenet": "[TIMING]",
        "hozzaad": False,
        "osz": False,
        "super": True,
    },
    "vendeg": {
        "hu": "Vendég nehézség",
        "en": "Guest difficulty",
        "leiras_hu": "A V31 tudja igazán. Kell egy .osu ugyanabból a szettből.",
        "leiras_en": "Works properly on V31. Needs a .osu from the same mapset.",
        "kontextus": "[GD,TIMING]",
        "kimenet": "[MAP]",
        "hozzaad": False,
        "osz": False,
        "super": False,
    },
    "hitsound": {
        "hu": "Hitsound",
        "en": "Hitsounds",
        "leiras_hu": "A V31 a kész objektumokra hitsoundot tesz. Kell a .osu.",
        "leiras_en": "V31 adds hitsounds onto the existing objects. The .osu is required.",
        "kontextus": "[NO_HS,TIMING]",
        "kimenet": "[MAP]",
        "hozzaad": False,
        "osz": False,
        "super": False,
    },
    "szakasz": {
        "hu": "Szakasz",
        "en": "Section",
        "leiras_hu": "Egy időintervallum újragenerálása. Kell a .osu, a kezdet és a vég.",
        "leiras_en": "Regenerate a time range. Needs the .osu, plus start and end.",
        "kontextus": "[TIMING]",
        "kimenet": "[MAP]",
        "hozzaad": True,
        "osz": False,
        "super": False,
    },
    "egyeni": {
        "hu": "Egyéni",
        "en": "Custom",
        "leiras_hu": "Minden kapcsoló szerkeszthető. A −1 ismeretlent jelent.",
        "leiras_en": "Every control is editable. -1 means unknown.",
        "kontextus": "[NONE]",
        "kimenet": "[TIMING,MAP,SV]",
        "hozzaad": False,
        "osz": True,
        "super": False,
    },
}

KONTEXTUSOK = ["[NONE]", "[TIMING]", "[TIMING,KIAI]", "[TIMING,KIAI,MAP]", "[GD,TIMING]", "[NO_HS,TIMING]"]
KIMENETEK = {
    "v32": ["[TIMING,MAP,SV]", "[MAP]", "[TIMING]"],
    "v31": ["[TIMING,KIAI,MAP,SV]", "[MAP]", "[TIMING]"],
}


def t(kulcs: str) -> str:
    return SZOVEG[st.session_state.nyelv][kulcs]


def cimke_lista(jatekmod: int, mind: bool) -> list[str]:
    if not TAGEK.exists():
        return []
    tagok = json.loads(TAGEK.read_text(encoding="utf-8"))["tags"]
    magyar = json.loads(CIMKEK.read_text(encoding="utf-8")) if CIMKEK.exists() else {}
    lathato = []
    mar = set()
    for tag in tagok:
        nev = tag["name"]
        if nev in mar:
            continue
        szabaly = tag.get("ruleset_id")
        if not mind and szabaly not in (None, jatekmod):
            continue
        mar.add(nev)
        felirat = magyar.get(nev, nev) if st.session_state.nyelv == "hu" else nev
        lathato.append((felirat, nev))
    lathato.sort(key=lambda par: par[0].casefold())
    return [""] + [f"{felirat} — {nev}" if felirat != nev else nev for felirat, nev in lathato]


def cimke_nev(szoveg: str) -> str:
    szoveg = (szoveg or "").strip()
    if " — " in szoveg:
        return szoveg.split(" — ", 1)[1].strip()
    return szoveg


def alapok():
    hang = futtatas.teszt_hang()
    st.session_state.setdefault("nyelv", os.environ.get("OSU_AI_LANG", "hu"))
    st.session_state.setdefault("feladat", "uj")
    st.session_state.setdefault("elfogadom", False)
    st.session_state.setdefault("hang", str(hang) if hang else "")
    st.session_state.setdefault("beatmap", "")
    st.session_state.setdefault("kimenet", str(futtatas.KIMENET))
    st.session_state.setdefault("modell", "v32")
    st.session_state.setdefault("jatekmod", 0)
    st.session_state.setdefault("kontextus", "[NONE]")
    st.session_state.setdefault("kimenet_tipus", "[TIMING,MAP,SV]")
    st.session_state.setdefault("hozzaad", False)
    st.session_state.setdefault("osz", True)
    st.session_state.setdefault("super_timing", False)
    st.session_state.setdefault("nehezseg", 5.0)
    st.session_state.setdefault("mapper_id", -1)
    st.session_state.setdefault("ev", 2023)
    st.session_state.setdefault("hp", 5.0)
    st.session_state.setdefault("cs", 4.0)
    st.session_state.setdefault("od", 9.0)
    st.session_state.setdefault("ar", 8.0)
    st.session_state.setdefault("sv", 1.4)
    st.session_state.setdefault("slider_tick", 1.0)
    st.session_state.setdefault("billentyu", 4)
    st.session_state.setdefault("hitsounded", True)
    st.session_state.setdefault("hold", -1.0)
    st.session_state.setdefault("scroll", -1.0)
    st.session_state.setdefault("felulir", False)
    st.session_state.setdefault("kezdet", -1)
    st.session_state.setdefault("veg", -1)
    st.session_state.setdefault("cfg", 1.0)
    st.session_state.setdefault("homerseklet", 0.9)
    st.session_state.setdefault("seed", -1)
    st.session_state.setdefault("timing_tures", 20)
    st.session_state.setdefault("sugarak", 2)
    st.session_state.setdefault("iteraciok", 20)
    st.session_state.setdefault("bpm_kuszob", 0.1)
    st.session_state.setdefault("keszito", "Mapperatorinator")
    st.session_state.setdefault("diff_verzio", "AI")


def feladat_valtozott():
    if st.session_state.feladat == "egyeni":
        return
    adat = FELADATOK[st.session_state.feladat]
    st.session_state.kontextus = adat["kontextus"]
    st.session_state.kimenet_tipus = adat["kimenet"]
    st.session_state.hozzaad = adat["hozzaad"]
    st.session_state.osz = adat["osz"]
    st.session_state.super_timing = adat["super"]


def feltoltott_hang(fajl) -> str:
    cel = PROJEKT / "bemenet"
    cel.mkdir(exist_ok=True)
    ut = cel / fajl.name
    ut.write_bytes(fajl.getbuffer())
    return str(ut)


def main():
    st.set_page_config(page_title="Mapperatorinator", layout="wide")
    alapok()
    nyelv = st.sidebar.radio(t("nyelv"), ["hu", "en"], format_func=lambda kod: "Magyar" if kod == "hu" else "English", key="nyelv")
    st.title(t("cim"))
    st.checkbox(t("szabaly"), key="elfogadom")

    st.selectbox(
        t("feladat"),
        list(FELADATOK),
        format_func=lambda kod: FELADATOK[kod][nyelv],
        key="feladat",
        on_change=feladat_valtozott,
    )
    st.caption(FELADATOK[st.session_state.feladat][f"leiras_{nyelv}"])

    st.text_input(t("hang"), key="hang", help=t("hang_sugo"))
    feltoltve = st.file_uploader(t("feltoltes"), type=["mp3", "ogg", "wav", "flac", "m4a"])
    st.text_input(t("beatmap"), key="beatmap", help=t("beatmap_sugo"))
    st.text_input(t("kimenet"), key="kimenet")

    oszlop = st.columns(3)
    oszlop[0].selectbox(t("modell"), ["v32", "v32-mini", "v31", "v30", "v29"], key="modell", help=t("modell_sugo"))
    oszlop[1].selectbox(t("mod"), [0, 1, 2, 3], format_func=lambda mod: ["osu!standard", "osu!taiko", "osu!catch", "osu!mania"][mod], key="jatekmod")
    oszlop[2].number_input(t("nehezseg"), step=0.1, help=t("nehezseg_sugo"), key="nehezseg")
    meta = st.columns(3)
    meta[0].number_input(t("mapper"), step=1, key="mapper_id")
    meta[1].number_input(t("ev"), step=1, key="ev")
    meta[2].text_input(t("lora"), key="lora")

    mind = st.checkbox(t("minden"), key="minden_cimke")
    opciok = cimke_lista(int(st.session_state.jatekmod), bool(mind))
    st.caption(t("cimkek_sugo"))
    valasztott = []
    for index in range(1, 4):
        kulcs = f"cimke_{index}"
        st.session_state.setdefault(kulcs, "")
        if st.session_state[kulcs] not in opciok:
            st.session_state[kulcs] = ""
        valasztott.append(st.selectbox(f"{index}. {t('cimkek')}", opciok, key=kulcs))
    st.caption(t("negativ_sugo"))
    negativ = []
    for index in range(1, 4):
        kulcs = f"negativ_{index}"
        st.session_state.setdefault(kulcs, "")
        if st.session_state[kulcs] not in opciok:
            st.session_state[kulcs] = ""
        negativ.append(st.selectbox(f"{index}. {t('negativ')}", opciok, key=kulcs))

    with st.expander(t("nehezseg_panel")):
        szamok = st.columns(4)
        szamok[0].number_input(t("hp"), step=0.1, key="hp")
        szamok[1].number_input(t("cs"), step=0.1, key="cs")
        szamok[2].number_input(t("od"), step=0.1, key="od")
        szamok[3].number_input(t("ar"), step=0.1, key="ar")
        tovabb = st.columns(4)
        tovabb[0].number_input(t("sv"), step=0.1, key="sv")
        tovabb[1].number_input(t("tick"), step=0.1, key="slider_tick")
        tovabb[2].slider(t("kulcs"), 1, 18, key="billentyu")
        tovabb[3].checkbox(t("hitsound"), key="hitsounded")
        st.number_input(t("hold"), step=0.1, key="hold")
        st.number_input(t("scroll"), step=0.1, key="scroll")

    with st.expander(t("generalas_panel")):
        lehetseges = KIMENETEK["v31" if st.session_state.modell == "v31" else "v32"]
        if st.session_state.kimenet_tipus not in lehetseges:
            st.session_state.kimenet_tipus = lehetseges[0]
        st.selectbox(t("kontextus"), KONTEXTUSOK, key="kontextus", disabled=st.session_state.feladat != "egyeni")
        st.selectbox(t("kimenet_tipus"), lehetseges, key="kimenet_tipus", disabled=st.session_state.feladat != "egyeni")
        st.checkbox(t("hozzaad"), key="hozzaad", disabled=st.session_state.feladat != "egyeni")
        st.checkbox(t("osz"), key="osz", disabled=st.session_state.feladat != "egyeni")
        st.checkbox(t("felulir"), key="felulir")
        st.number_input(t("kezdet"), step=1000, key="kezdet")
        st.number_input(t("veg"), step=1000, key="veg")
        st.slider(t("cfg"), 1.0, 5.0, step=0.1, key="cfg")
        st.slider(t("homerseklet"), 0.0, 1.0, step=0.01, key="homerseklet")
        st.number_input(t("seed"), step=1, key="seed")
        st.slider(t("timing"), 0, 100, key="timing_tures")
        st.checkbox(t("super"), key="super_timing", disabled=st.session_state.feladat != "egyeni")
        st.slider(t("sugarak"), 1, 4, key="sugarak")
        st.slider(t("iteraciok"), 1, 40, key="iteraciok")
        st.slider(t("bpm"), 0.0, 1.0, step=0.1, key="bpm_kuszob")

    with st.expander(t("meta")):
        st.text_input(t("dalcim"), key="dalcim")
        st.text_input(t("eloado"), key="eloado_nev")
        st.text_input(t("keszito"), key="keszito")
        st.text_input(t("verzio"), key="diff_verzio")
        st.text_input(t("forras"), key="forras")

    naplo = st.empty()
    if st.button(t("gomb"), type="primary"):
        hang = feltoltott_hang(feltoltve) if feltoltve is not None else st.session_state.hang
        beallitas = {
            "elfogadva": st.session_state.elfogadom,
            "modell": st.session_state.modell,
            "jatekmod": int(st.session_state.jatekmod),
            "hang": hang,
            "beatmap": st.session_state.beatmap,
            "kimenet": st.session_state.kimenet,
            "kontextus": st.session_state.kontextus,
            "kimenet_tipus": st.session_state.kimenet_tipus,
            "cimkek": [cimke_nev(ertek) for ertek in valasztott],
            "negativ": [cimke_nev(ertek) for ertek in negativ],
            "nehezseg": st.session_state.nehezseg,
            "mapper_id": st.session_state.mapper_id,
            "ev": st.session_state.ev,
            "lora": st.session_state.get("lora", ""),
            "hp": st.session_state.hp,
            "cs": st.session_state.cs,
            "od": st.session_state.od,
            "ar": st.session_state.ar,
            "sv": st.session_state.sv,
            "slider_tick": st.session_state.slider_tick,
            "billentyu": st.session_state.billentyu,
            "hitsounded": st.session_state.hitsounded,
            "hold": st.session_state.hold,
            "scroll": st.session_state.scroll,
            "hozzaad": st.session_state.hozzaad,
            "osz": st.session_state.osz,
            "felulir": st.session_state.felulir,
            "kezdet": st.session_state.kezdet,
            "veg": st.session_state.veg,
            "cfg": st.session_state.cfg,
            "homerseklet": st.session_state.homerseklet,
            "seed": st.session_state.seed,
            "timing_tures": st.session_state.timing_tures,
            "super_timing": st.session_state.super_timing,
            "sugarak": st.session_state.sugarak,
            "iteraciok": st.session_state.iteraciok,
            "bpm_kuszob": st.session_state.bpm_kuszob,
            "cim": st.session_state.get("dalcim", ""),
            "eloado": st.session_state.get("eloado_nev", ""),
            "keszito": st.session_state.keszito,
            "verzio": st.session_state.diff_verzio,
            "forras": st.session_state.get("forras", ""),
        }
        with st.status(t("folyamat"), expanded=True) as allapot:
            try:
                utvonal = futtatas.futtat(beallitas, frissit=naplo.code)
            except Exception as hiba:
                allapot.update(label=t("hiba"), state="error")
                st.error(str(hiba))
            else:
                allapot.update(label=t("kesz"), state="complete")
                st.success(str(utvonal))


if __name__ == "__main__":
    main()
