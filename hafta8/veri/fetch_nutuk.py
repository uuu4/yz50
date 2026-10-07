import json, urllib.request, urllib.parse, time
base = "https://tr.wikisource.org/w/api.php"
UA = {"User-Agent": "yz50-dataset/1.0 (egitim amacli; lalifmind@gmail.com)"}
titles = [t for l, t in json.load(open("pages.json")) if t.startswith("Nutuk")]
raw = {}
for i in range(0, len(titles), 40):
    chunk = titles[i:i+40]
    p = {"action":"query","prop":"revisions","rvprop":"content","rvslots":"main","titles":"|".join(chunk),"format":"json"}
    req = urllib.request.Request(base, data=urllib.parse.urlencode(p).encode(), headers=UA)
    d = json.load(urllib.request.urlopen(req, timeout=60))
    for pg in d["query"]["pages"].values():
        if "revisions" in pg:
            raw[pg["title"]] = pg["revisions"][0]["slots"]["main"]["*"]
    time.sleep(0.5)
json.dump(raw, open("nutuk_raw.json", "w"), ensure_ascii=False)
print(len(titles), len(raw), sum(len(v) for v in raw.values()))
