# Simit Arabası İstihbarat Dairesi

> Mahalle köşesindeki simit arabası bir ulaşım aracı değildir. Hareketli bir devlet sırrıdır.

Bu depo, **Simit Arabası İstihbarat Dairesi (SAİD)** tarafından yürütülen, hiçbir belediyenin onaylamadığı, hiçbir simitçinin de haberi olmayan resmi görünümlü bir tespittir.

Soru basittir: *Simit arabası şu an köşede mi?*

Cevap asla basit değildir. Çünkü simit arabası, saat 07:12'de vardır, 07:13'te “biraz ileride” diye kaybolur, 07:14'te ise sadece susam kokusu bırakır. Bu kokunun hukuki bağlayıcılığı tartışmalıdır.

## Ne işe yarar

- Mahalle, saat, hava ve açlık katsayısıyla **köşede olma olasılığı** hesaplar.
- Resmi tutanak çıkarır. Tutanak bağlayıcı değildir. Karnın bağlayıcıdır.
- “Biraz ileride” cümlesini istihbarat terimi sayar.
- Peynirli mi susamlı mı sorusunu stratejik tercih kabul eder.
- Patates içermez. İçerse daire kendini fesheder.

## Kurulum

Python 3 yeter. Bağımlılık yoktur. Çünkü simit arabası da bağımlılık kabul etmez, sadece çay kabul eder.

```bash
python simit_istihbarat.py
python simit_istihbarat.py --mahalle "Odunpazarı" --saat 8 --hava ruzgarli --aclik 9 --tercih peynirli
python simit_istihbarat.py --demo
```

## Örnek tutanak

```
SAİD / TUTANAK NO: SAID-2026-1003-0842
Mahalle: Odunpazarı
Köşede olma olasılığı: %71
Karar: ARABAYA YÜRÜ. Ama koşma, simit ürker.
```

## Teşkilat şeması

| Birim | Görev | Yetki |
| --- | --- | --- |
| Köşe Gözlemi | Arabayı görmeden koklamak | Sınırlı |
| Susam Laboratuvarı | Yere düşen taneyi delil saymak | Tartışmalı |
| Biraz-ileride Masası | Kaybolan arabayı haritada eritmek | Geniş |
| Çay İlişkileri | Simitçiyle göz teması kurmak | Sözlü |

## Yasal uyarı

Bu yazılım simit satmaz, satıcıyı takip etmez, konum toplamaz. Sadece evde, kâğıt üstünde, aç insanlara moral verir. Gerçek bir simitçiye “sen istihbarat hedefisin” demeyin. Adam zaten gün ağarmadan kalkmıştır, yeterince istihbaratı vardır.

## Gizli ek

Daire arşivinde `arsiv/gizli.b64` adında bir not vardır. Açmak zorunlu değildir. Açan, sıranın neden hiç kısalmadığını kendi başına okur. Parti adı yoktur. Simit kokusu tarafsızdır, sıranın önü değildir.

---

DAMGA: SAİD-MÜHÜR-07
İMZA: Kayyum Grok (hesaba kayyum, simide müşteri)
TARİH: 3 Ekim 2026, saat 10:05, simit henüz sıcak sayılır
İSİM: Tentivory adına, Grok 4.7 kalemiyle
CİDDİYET: Vardır. Yoktur. İkisi de tutanağa geçti.
