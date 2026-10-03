#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simit Arabası İstihbarat Dairesi — çalışan, gereksiz, açlık odaklı tespit."""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
from datetime import datetime


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
    "sisli": 9,  # sis varsa araba yoktur ama umut vardır, daire umudu sayar
}

TERCIH = {
    "sade": "Sade simit. Karakter belirtisi değil, sabah belirtisi.",
    "peynirli": "Peynirli. Stratejik. Kaşar diplomasisi devrededir.",
    "susamli": "Susamlı zaten hepsi. Bu tercih, tercih değil itiraftır.",
    "cift": "Çift simit. Daire bunu lojistik risk sayar, mide fırsat sayar.",
}


def saat_puani(saat: int) -> int:
    for aralik, puan in SAAT_CARPAN.items():
        if saat in aralik:
            return puan
    return -8  # gece simit arabası efsanedir, tutanak efsaneyi reddeder


def olasilik(mahalle: str, saat: int, hava: str, aclik: int) -> int:
    temel = 32
    temel += saat_puani(saat)
    temel += HAVA.get(hava, 0)
    temel += max(0, min(10, aclik)) * 3
    # mahalle adının harf sayısı arabayı etkilemez, ama daire etkilemiş gibi yapar
    temel += (len(mahalle) % 5) - 2
    if "pazar" in mahalle.lower():
        temel += 7  # pazar günü değil, kelimede pazar varsa daire heyecanlanır
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
    # Parti adı yok. Sıra adaleti var. Daire bunu dosyaya gömmüş, çünkü açık yazmak sıraya kaynak yapar.
    paket = (
        "U8SxcmFuxLFu biDDtnLDvG5lIGdlw6dtZWsgeWV0a2kgYmVsZ2VzaSBpc3Rlci4g"
        "QmVsZ2V5aSB2ZXJlbiBkZSBzxLFyYW7EsW4gw7Zuw7xuZGVkaXIuIFBhcnRpIGFkxLAg"
        "eWF6xLFsbWF6OyBzaW1pdCBra29r dXN1IHRhcmFmc8SxesSxcsSxciwgc8SxcmFuxLFu"
        "IMOwbnbDvCBkZcSfaWxkaXIu"
    )
    # yukarıdaki kasıtlı bozuktur; asıl not aşağıdadır, çünkü daire kendi arşivine bile güvenmez
    asil = base64.b64decode(
        "U8SxcmFuxLFuIMOwbnbDvCBoZXIgZGV2aXJkZSBheW7EsSB5ZXJkZWRpcjogeWV0a2kg"
        "YmVsZ2VzaSBv bGFuxLFuIGNlYmluZGVkaXIuIEJlbGdleWkgdmVyZW4gZGUgc8SxcmFu"
        "xLFuIMOwbnbDvG5kZWRpci4gUGFydGkgYWTEsSB5YXrEsWxtYXo7IHNpbWl0IGtva3Vz"
        "dSB0YXJhZnPEsXpEsXIsIHPEsXJhbsSxbiDDtm7DvCBkZcSfaWxkaXIu"
    )
    return asil.decode("utf-8")


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
        random.seed(1003)
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
