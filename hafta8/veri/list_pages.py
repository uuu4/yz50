import json, urllib.request, urllib.parse
base = "https://tr.wikisource.org/w/api.php"
UA = {"User-Agent": "yz50-dataset/1.0 (egitim amacli; lalifmind@gmail.com)"}
params = {"action":"query","generator":"allpages","gaplimit":"500","gapnamespace":"0","prop":"info","format":"json"}
pages = []
while True:
    req = urllib.request.Request(base + "?" + urllib.parse.urlencode(params), headers=UA)
    d = json.load(urllib.request.urlopen(req, timeout=30))
    pages += [(p["length"], p["title"]) for p in d.get("query", {}).get("pages", {}).values()]
    if "continue" not in d: break
    params.update(d["continue"])
pages.sort(reverse=True)
json.dump(pages, open("pages.json", "w"), ensure_ascii=False)
print(len(pages), sum(l for l, _ in pages) / 1e6, "MB toplam (wikitext)")
for l, t in pages[:70]: print(l, t)
