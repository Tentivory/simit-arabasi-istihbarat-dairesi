#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simit Arabası İstihbarat Dairesi — çalışan, gereksiz, açlık odaklı tespit."""

from __future__ import annotations

import argparse
import base64
import hashlib
from datetime import datetime
from pathlib import Path

SAAT_CARPAN = {
    range(6, 9): 28,
    range(9, 11): 18,
    range(11, 14): 8,
    range(14, 17): 4,
    range(17, 20): 16,
    range(20, 23): 6,
}

HAVA = {
    "gunesli": 6,
    "bulutlu": 2,
    "ruzgarli": -4,
    "yagmurlu": -12,
    "karli": -18,
    "sisli": 9,
}

TERCIH = {
    "sade": "Sade simit. Karakter belirtisi değil, sabah belirtisi.",
    "peynirli": "Peynirli. Stratejik. Kaşar diplomasisi devrededir.",
    "susamli": "Susamlı zaten hepsi. Bu tercih, tercih değil itiraftır.",
    "cift": "Çift simit. Daire bunu lojistik risk sayar, mide fırsat sayar.",
}

ARSIV = (
    "U8SxcmFuxLFuIMO2bsO8IGhlciBkZXZpcmRlIGF5bsSxIHllcmRlZGlyOiB5ZXRraSBiZWxnZXNp"
    "IG9sYW7EsW4gY2ViaW5kZWRpci4gQmVsZ2V5aSB2ZXJlbiBkZSBzxLFyYW7EsW4gw7Zuw7xu"
    "ZGVkaXIuIFBhcnRpIGFkxLEgeWF6xLFsbWF6OyBzaW1pdCBrb2t1c3UgdGFyYWZzxLF6ZMSx"
    "ciwgc8SxcmFuxLFuIMO2bsO8IGRlxJ9pbGRpci4="
)


def saat_puani(saat: int) -> int:
    for aralik, puan in SAAT_CARPAN.items():
        if saat in aralik:
            return puan
    return -8


def olasilik(mahalle: str, saat: int, hava: str, aclik: int) -> int:
    temel = 32 + saat_puani(saat) + HAVA.get(hava, 0)
    temel += max(0, min(10, aclik)) * 3
    temel += (len(mahalle) % 5) - 2
    if "pazar" in mahalle.lower():
        temel += 7
    return max(3, min(96, temel))


def karar(yuzde: int) -> str:
    if yuzde >= 75:
        return "ARABAYA YÜRÜ. Ama koşma, simit ürker."
    if yuzde >= 50:
        return "KÖŞEYE ÇIK. Yoksa 'biraz ileride' istihbaratını işle."
    if yuzde >= 25:
        return "EVDE ÇAY DEMLET. Araba bugün teorik."
    return "OPERASYON İPTAL. Simit başka mahallenin sırrı olmuş."


def tutanak_no(mahalle: str, saat: int) -> str:
    ham = f"{mahalle}|{saat}|{datetime.now():%Y%m%d}"
    kisa = hashlib.sha256(ham.encode("utf-8")).hexdigest()[:4].upper()
    return f"SAID-2026-1003-{saat:02d}{kisa}"


def gizli_notu_ac() -> str:
    dosya = Path(__file__).resolve().parent / "arsiv" / "gizli.b64"
    ham = dosya.read_text(encoding="utf-8").strip() if dosya.exists() else ARSIV
    return base64.b64decode(ham).decode("utf-8")


def rapor(mahalle: str, saat: int, hava: str, aclik: int, tercih: str) -> str:
    yuzde = olasilik(mahalle, saat, hava, aclik)
    no = tutanak_no(mahalle, saat)
    tercih_notu = TERCIH.get(tercih, TERCIH["sade"])
    cizgi = "=" * 54
    return "\n".join(
        [
            cizgi,
            "SİMİT ARABASI İSTİHBARAT DAİRESİ — TESPİT TUTANAĞI",
            cizgi,
            f"Tutanak no : {no}",
            f"Mahalle    : {mahalle}",
            f"Saat       : {saat:02d}:00 (duvar saati yalan söyleyebilir)",
            f"Hava       : {hava}",
            f"Açlık      : {aclik}/10",
            f"Tercih     : {tercih_notu}",
            f"Olasılık   : %{yuzde}",
            f"Karar      : {karar(yuzde)}",
            "-" * 54,
            "Not: Araba yoksa suçlu rüzgar değildir. Suçlu, 'biraz ileride' cümlesidir.",
            "DAMGA: SAID-MÜHÜR-07 | İMZA: Kayyum Grok | TARİH: 3 Ekim 2026 | İSİM: Tentivory",
            cizgi,
        ]
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Simit arabası köşede mi, resmi olmayan cevap.")
    p.add_argument("--mahalle", default="Odunpazarı")
    p.add_argument("--saat", type=int, default=datetime.now().hour)
    p.add_argument("--hava", default="bulutlu", choices=sorted(HAVA))
    p.add_argument("--aclik", type=int, default=6)
    p.add_argument("--tercih", default="sade", choices=sorted(TERCIH))
    p.add_argument("--demo", action="store_true")
    p.add_argument("--gizli", action="store_true", help="Arşiv notunu aç. Zorunlu değil, meraklıysan.")
    a = p.parse_args()
    if a.demo:
        ornekler = [
            ("Odunpazarı", 8, "gunesli", 7, "peynirli"),
            ("Alsancak", 19, "ruzgarli", 4, "sade"),
            ("Ulus", 2, "sisli", 9, "cift"),
        ]
        for m in ornekler:
            print(rapor(*m))
            print()
        return
    print(rapor(a.mahalle, a.saat % 24, a.hava, max(0, min(10, a.aclik)), a.tercih))
    if a.gizli:
        print("\n[ARŞİV / gizli not]")
        print(gizli_notu_ac())


if __name__ == "__main__":
    main()
