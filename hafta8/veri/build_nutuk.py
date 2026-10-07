import json, re, unicodedata, sys

raw = json.load(open("nutuk_raw.json"))

def links(page, wikitext):
    out = []
    for m in re.finditer(r"\[\[/([^\]|]+)(?:\|[^\]]*)?\]\]", wikitext):
        out.append(page + "/" + m.group(1).strip())
    return out

# okuma sırası: ana sayfa -> bölümler -> her bölümün alt başlıkları
order = []
for ch in links("Nutuk", raw["Nutuk"]):
    if ch not in raw: continue
    order.append(ch)
    for sub in links(ch, raw[ch]):
        if sub in raw and sub not in order: order.append(sub)
missing = [t for t in raw if t not in order]
print("sıralı:", len(order), "sıra dışı:", len(missing))

def strip_templates(s):
    s = re.sub(r"\{\{\s*[Aa]lıntı\s*\|(.*?)\}\}", lambda m: m.group(1), s, flags=re.S)   # alıntının içeriği kalsın
    prev = None
    while prev != s:                      # iç içe şablonları içten dışa sil
        prev = s
        s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    return s

def clean(t):
    t = strip_templates(t)
    t = re.sub(r"\{\|.*?\|\}", "", t, flags=re.S)                  # tablolar
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)                  # <br> satır sonu olsun, kelimeleri yapıştırmasın
    t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
    t = re.sub(r"<ref[^>]*/>", "", t)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)                                  # html etiketleri
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)             # [[a|b]] -> b
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", t)
    t = re.sub(r"'{2,}", "", t)                                    # kalın/italik
    t = re.sub(r"^=+\s*(.*?)\s*=+\s*$", r"\1", t, flags=re.M)      # başlıklar
    t = re.sub(r"^[*#:;]+\s*", "", t, flags=re.M)
    return t

def normalize(t):
    t = unicodedata.normalize("NFC", t)
    t = t.replace("'", "’")                                          # düz kesme işaretini Nutuk’un genel ’ biçimine eşitle
    t = t.replace(" ", " ").replace("​", "").replace("﻿", "").replace("‎", "").replace("‏", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

parts, skipped = [], []
for title in order:
    if "esika" in title:                    # Vesika sayfaları: belge/telgraf, anlatı değil
        skipped.append(title); continue
    body = normalize(clean(raw[title]))
    if len(body) < 200:                     # boş/içindekiler sayfaları
        skipped.append(title); continue
    parts.append(body)

text = "\n\n".join(parts) + "\n"
open("nutuk_full.txt", "w", encoding="utf-8").write(text)
TARGET = 1_115_394                       # Tiny Shakespeare ile aynı karakter sayısı
cut = text.rfind("\n\n", 0, TARGET)    # paragraf sınırında kes
open("input_tr.txt", "w", encoding="utf-8").write(text[:cut] + "\n")
print("kesilen metin:", cut)
print("parça:", len(parts), "atlanan:", len(skipped), "toplam karakter:", len(text))
