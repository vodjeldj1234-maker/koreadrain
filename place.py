# -*- coding: utf-8 -*-
"""장소별 안내 /place/{장소}.html 30장 + 목록 /place/ (49째방, 2026-10-17) — 주인님 「모든건 팔도처럼」.
   팔도의 /apartment · /school · /hospital … 자리. 한 장소에서 생기는 문제와 저희가 하는 공사를 종목별로 묶는다.
   + 종목×장소 페이지(예: /trench/apartment.html 「아파트 트렌치 시공·교체 업체」)는 bld.pages 가 여기 combo_pages 를 받아 같이 만든다.

   ★ 글 = place_data.json (49째방 글 조수가 facts49.txt 사실표만 근거로 씀). 그 장소에서 공사했다고 쓰지 않는다.
   ★ 「실제로 공사한 현장」 카드는 아래 REAL 에 적은 실제 사례만 (사례 제목에 그 장소가 적힌 것). 없으면 종목 공통 사진에
     「같은 공사를 한 다른 현장 사진」이라고 붙인다.
   ★ 지역 이름 없음 (출장 범위 한 줄 = 첫 페이지와 같은 문구). slug 는 바꾸지 않는다."""
import os, io, json, html
import cases as CS

DIR = "place"
_HERE = os.path.dirname(os.path.abspath(__file__))
_P = os.path.join(_HERE, "place_data.json")
DATA = json.load(io.open(_P, encoding="utf-8")) if os.path.exists(_P) else []
FOOT = {"foot": "우수관 · 트렌치 · 보도블록 · 카스토퍼 · 에어컨 배관 · 렉산 캐노피 시공"}

SVC_NAME = {"usugwan": "우수관·홈통·빗물받이", "trench": "트렌치·배수로", "block": "보도블록·점자블록·경계석",
            "carstop": "카스토퍼·과속방지턱", "aircon": "에어컨 배관 보온재", "lexan": "렉산·캐노피"}
SVC_SHORT = {"usugwan": "우수관", "trench": "트렌치", "block": "보도블록", "carstop": "카스토퍼",
             "aircon": "에어컨 배관", "lexan": "캐노피"}

# 장소 → 실제 사례 slug (사례 제목에 그 장소가 적힌 것만 · 49째방에 사례 제목을 보고 골랐다)
REAL = {
    "apartment": ["apt-entrance-canopy-lexan-one-row",
                  "apt-walkway-canopy-lexan-full-replace", "apt-office-front-canopy-lexan-replace", "apt-pergola-skylight-lexan-replace",
                  "apt-bike-shelter-lexan-partial-replace", "apt-parking-ramp-roof-silicone", "apt-recycling-shed-roof-silicone",
                  "apt-park-round-pergola-lexan-strips", "apt-recycling-shed-lexan-roof-repair"],
    "villa": ["tile-eave-gutter-to-rooftop", "top-floor-terrace-embedded-leak-100", "dryvit-villa-loose-downpipe-refix",
              "villa-crushed-zinc-bottom-one-pipe"],
    "house": ["house-zinc-gutter-new", "brick-house-zinc-gutter-lines", "brick-house-gutter-square-downpipes", "entrance-roof-gutter-new",
              "brick-house-old-pvc-pipe-replace", "house-drain-outlet-pvc-downpipe", "rooftop-balcony-drain-channel-rebuild",
              "house-wall-canopy-lexan-replace", "house-deck-canopy-lexan-roof", "house-eaves-bracket-canopy-install"],
    "mixed": ["rooftop-drain-new-hole-stainless-75", "leaking-zinc-header-to-pvc", "embedded-leak-rope-pvc-offset-eave",
              "embedded-leak-rope-pvc-four-storey"],
    "shop": ["shop-building-gutter-two-downpipes", "shop-building-gutter-bridge", "commercial-building-stainless-pipe-new-hole",
             "shop-row-zinc-downpipe-full-replace", "alley-rope-stainless-75-redesign", "rooftop-parapet-core-pvc-pipe-add",
             "fallen-pipe-pvc-rope-jump-over", "rooftop-parking-drain-slope-new-pipe", "shop-tile-floor-trench", "parking-ramp-noiseless",
             "shop-entrance-braille-new", "block-floor-parking-line-paint", "shop-entrance-arch-canopy-replace",
             "shop-front-arch-canopy-lexan-replace"],
    "factory": ["factory-gutter-new-brackets", "factory-gutter-new-stainless-100", "factory-roof-water-stainless-100-new",
                "factory-fallen-stainless-125-refix", "factory-wall-drain", "factory-basement-trench"],
    "warehouse": ["warehouse-door-canopy-install"],
    "restaurant": ["restaurant-courtyard-extra-downpipe"],
    "car-wash": ["carwash-indoor-trench"],
    "car-center": ["detailing-shop-grid-trench", "garage-rooftop-small-drain-core-100"],
    "parking": ["parking-ramp-noiseless", "underground-parking-grating", "parking-entrance-grating-repair", "indoor-ramp-speed-bump",
                "indoor-aisle-long-speed-bump", "piloti-lot-carstop-row", "outdoor-lot-carstop-set", "wide-outdoor-lot-carstop",
                "apt-parking-ramp-roof-silicone", "driveway-arch-canopy-lexan-replace"],
    "public-office": ["parking-entrance-grating-repair"],
    "gym": ["pool-tile-trench-extend"],
}


def url(p=None):
    return "/%s/%s.html" % (DIR, p["slug"]) if p else "/%s/" % DIR


def _case_index(b):
    """slug → (사례, 그 종목 case_cfg)"""
    out = {}
    for s in b.SERVICES:
        for c in (s.get("cases") or []):
            out.setdefault(c["slug"], (c, s["case_cfg"]))
    return out


def combo_pages(key):
    """bld.pages 가 부른다 — 이 종목의 종목×장소 페이지 (실제 사례 없는 유형 · 글은 place_data.json combos)."""
    out = []
    for p in DATA:
        cb = (p.get("combos") or {}).get(key)
        if not cb:
            continue
        out.append(dict(kind="bld", combo=True, slug=p["slug"], name=p["name"], head=cb["title"],
                        desc_t=cb["desc"].rstrip() + " {phone}", cases=[], story=(cb["story_title"], cb["paras"]),
                        faq_r=[tuple(x) for x in cb.get("faq", [])], place=p["slug"]))
    return out


def _svc_url(b, p, key):
    """장소 페이지의 종목 카드가 갈 곳 — 종목×장소 페이지가 있으면 그것, 없으면 종목 첫 페이지."""
    svc = next(s for s in b.SERVICES if s["key"] == key)
    if key in (p.get("combos") or {}):
        return "/%s/%s.html" % (svc["dir"], p["slug"])
    import bld
    for slug, *_ in bld.B.get(key, []):
        if slug == p["slug"]:
            return "/%s/%s.html" % (svc["dir"], slug)
    return b.url_of(svc)


def _photos(b, p):
    idx = _case_index(b)
    real = [idx[s] for s in REAL.get(p["slug"], []) if s in idx]
    if real:
        cards = "".join('<a class="ccard" href="%s">%s<b>%s</b><span>사진 %d장</span></a>'
                        % (CS.url(cfg, c), b.imgtag(CS.img(c, c["cover"]), c["title"]), html.escape(c["title"]), len(c["photos"]))
                        for c, cfg in real[:6])
        return """<section class="cases"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>실제로 공사한 <em>%s 현장</em></h2>
  <p>현장 하나를 처음부터 끝까지 사진 순서대로 정리했습니다.</p></div>
  <div class="cgrid">%s</div>
</div></section>
<style>%s</style>
""" % (html.escape(p["name"]), cards, CS.CSS)
    items = []
    for key in p["svcs"][:2]:
        svc = next(s for s in b.SERVICES if s["key"] == key)
        for i, row in enumerate(svc["gallery"][:3], start=1):
            src = b.pick("%s-%d" % (key, i))
            items.append('<div class="item">%s<span class="lb">%s</span><div class="cp">%s<span>%s</span></div></div>'
                         % (b.imgtag(src, row[1]), row[0], row[1], row[2]))
    return """<section><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>같은 공사를 한 <em>다른 현장</em> 사진</h2>
  <p>%s 현장 사진은 시공하는 대로 올립니다. 아래는 같은 공사를 한 다른 현장 사진입니다.</p></div>
  <div class="gal">%s</div>
</div></section>
""" % (html.escape(p["name"]), "".join(items))


def _others(p=None):
    rows = "".join('<a href="%s">%s<i>&rsaquo;</i></a>' % (url(o), html.escape(o["name"])) for o in DATA if not p or o["slug"] != p["slug"])
    return ('<section class="nav"><div class="wrap">\n  <h2>장소별 안내</h2><p>건물·시설마다 손보는 자리가 다릅니다.</p>\n'
            '  <div class="links">%s</div>\n</div></section>\n' % rows)


def page(b, p):
    S = b.SITE
    top = "·".join(SVC_SHORT[k] for k in p["svcs"][:3])
    title = "%s %s 시공 업체 | %s" % (p["name"], top, S["name"])
    desc = p["desc"].rstrip() + " " + S["phone"]
    canonical = S["domain"] + url(p)
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": canonical,
                     "description": desc, "inLanguage": "ko",
                     "publisher": {"@type": "Organization", "name": S["name"], "telephone": S["phone"]}}, ensure_ascii=False)
    cells = "".join('<div class="cell"><div class="t"><b><a href="%s" style="color:inherit;text-decoration:none">%s %s &rsaquo;</a></b>'
                    '<span>%s %s</span></div></div>'
                    % (_svc_url(b, p, s["key"]), html.escape(p["name"]), html.escape(SVC_NAME[s["key"]]),
                       html.escape(s["why"]), html.escape(s["do"])) for s in p["svc_text"])
    intro = "".join("<p>%s</p>" % html.escape(x) for x in p["intro"])
    fq = "".join('<div class="fq"><b><i>Q</i>%s</b><p>%s</p></div>' % (html.escape(q), html.escape(a)) for q, a in p["faq"])
    body = """<div class="crumb"><div class="wrap"><a href="%s">장소별 안내</a><span>&rsaquo;</span>%s</div></div>
<section class="hero"><div class="wrap">
<h1>%s 시설 공사</h1>
<p class="sub">%s</p>
%s
%s
</div></section>
<section class="story"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>%s에서 손보는 자리</h2></div>
  <div class="stext">%s</div>
</div></section>
<section class="q"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>%s에서 하는 공사</h2><p>공사 종류를 누르면 자세한 안내로 갑니다.</p></div>
  <div class="qg">%s</div>
</div></section>
%s<section class="faq"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>%s 공사 <em>자주 묻는 질문</em></h2></div>
  <div class="fqlist">%s</div>
  <div class="links" style="margin-top:18px"><a href="/contact.html">견적 문의 · 사진 보내는 법<i>&rsaquo;</i></a><a href="/area/">출장 지역<i>&rsaquo;</i></a></div>
</div></section>
%s""" % (url(), html.escape(p["name"]), html.escape(p["name"]), html.escape(p["sub"]), b.trust(), b.ctabtns(),
         html.escape(p["name"]), intro, html.escape(p["name"]), cells, _photos(b, p), html.escape(p["name"]), fq, _others(p))
    return b.head(title, desc, canonical, ld, False, None) + b.header(None) + body + b.footer(FOOT)


def index(b):
    S = b.SITE
    title = "장소별 안내 — 아파트·상가·공장·학교·병원 시설 공사 | %s" % S["name"]
    desc = ("아파트·빌라·상가·공장·학교·병원·주차장 등 장소마다 손보는 자리가 다릅니다. 우수관·트렌치·보도블록·카스토퍼·에어컨 배관·렉산 캐노피. "
            "사진 보내주시면 당일 견적 회신. %s" % S["phone"])
    canonical = S["domain"] + url()
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": canonical,
                     "description": desc, "inLanguage": "ko"}, ensure_ascii=False)
    body = """<section class="hero"><div class="wrap">
<h1>장소별 안내</h1>
<p class="sub">건물과 시설마다 물이 고이고 깨지는 자리가 다릅니다. 장소를 누르면 그곳에서 하는 공사를 모아 보여 드립니다.</p>
%s
</div></section>
%s""" % (b.ctabtns(), _others())
    return b.head(title, desc, canonical, ld, False, None) + b.header(None) + body + b.footer(FOOT)


def build(b):
    out = []
    if not DATA:
        return out
    os.makedirs(os.path.join(b.DIST, DIR), exist_ok=True)
    b.write(os.path.join(b.DIST, DIR, "index.html"), index(b)); out.append(url())
    for p in DATA:
        b.write(os.path.join(b.DIST, DIR, p["slug"] + ".html"), page(b, p)); out.append(url(p))
    print("장소별 안내 %d장 + 목록 → /%s/" % (len(out) - 1, DIR))
    return out
