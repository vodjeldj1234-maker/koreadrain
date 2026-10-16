# -*- coding: utf-8 -*-
"""도시 안내 페이지 /area/{도시}.html 98장 + 출장 지역 목록 /area/ (49째방, 2026-10-17) — 주인님 「모든건 팔도처럼」.
   팔도의 /area/cheonan 자리: 한 도시에서 하는 공사 여섯 가지를 한 장에 모아 그 도시의 종목별 도시 페이지로 잇는다.

   ★ 지역 격리는 지킨다 — 도시 안내 페이지에는 그 도시와 그 도시의 구·동만. 다른 도시로 가는 링크 없음
     (팔도는 「다른 지역 보기」를 다는데 우리는 안 단다). 출장 지역 목록 /area/ 만 98곳 전체를 보여 준다.
   ★ 없는 사실 금지 — 종목 설명은 cities.SVC desc(= 각 종목 첫 페이지에 있는 말)만 줄였다. 그 도시 사례가 있다고 쓰지 않는다.
   slug = 도시 slug (city_data.json) 그대로. 바꾸지 않는다."""
import html, json
import cities

DIR = "area"
# 종목 카드 한 줄 — cities.SVC desc 에서 지역 말을 뺀 것
LINE = {
    "usugwan": "새는 우수관·선홈통 교체. 벽 속 매립 우수관은 막고 외벽으로 새로 냅니다.",
    "trench": "내려앉은 그레이팅·부식된 앵글 교체, 무소음 덮개, 배수로 신설.",
    "block": "내려앉은 보도블록 재시공, 깨진 점자블록·경계석 교체.",
    "carstop": "카스토퍼 설치·교체, 과속방지턱 시공, 주차장 코너보호대, 주차선 도색.",
    "aircon": "삭아서 벗겨진 보온재를 새로 씌우고 테이프를 다시 감아 케이블타이로 마감합니다.",
    "lexan": "깨지고 비 새는 렉산 지붕 부분 교체·전체 교체, 캐노픽스·현관 캐노피 설치.",
}
FOOT = {"foot": "우수관 · 트렌치 · 보도블록 · 카스토퍼 · 에어컨 배관 · 렉산 캐노피 시공"}


def url(c=None):
    return "/%s/%s.html" % (DIR, c["slug"]) if c else "/%s/" % DIR


def _cards(b, c):
    out = []
    for key in cities.KEYS:
        svc = next(s for s in b.SERVICES if s["key"] == key)
        u = cities.url_for(svc, c, b.REGIONS, b.SITE)
        if not u:
            continue
        out.append('<div class="cell"><div class="t"><b><a href="%s" style="color:inherit;text-decoration:none">%s &rsaquo;</a></b>'
                   '<span>%s</span></div></div>'
                   % (u, html.escape(cities.SVC[key]["link"].format(short=c["short"])), html.escape(LINE[key])))
    return "".join(out)


def page(b, c):
    S = b.SITE
    title = "%s 우수관·트렌치·보도블록 시공 업체 | %s" % (c["name"], S["name"])
    desc = ("%s 출장 시공 업체. 우수관·트렌치·보도블록·카스토퍼·에어컨 배관 보온재·렉산 캐노피. "
            "%s 전 지역 출장. 사진 보내주시면 당일 견적 회신. %s" % (c["official"], c["official"], S["phone"]))
    canonical = S["domain"] + url(c)
    base = cities._page_dict({"key": "usugwan"}, c, c["slug"], S)          # 구·동 목록과 동네 질문은 도시 페이지와 같은 틀
    ds = cities._dongs(c)
    faq = []
    if ds:
        d = ds[(len(ds) // 2) % len(ds)]
        faq.append(("%s인데 와 주시나요?" % d,
                    "갑니다. %s 안이면 동네를 가리지 않습니다. 현장 사진과 주소를 문자로 보내주시면 당일 견적 회신드립니다." % c["official"]))
    faq.append(("여러 가지 공사를 한 번에 맡길 수 있나요?",
                "됩니다. 우수관·트렌치·보도블록·카스토퍼·에어컨 배관·렉산 캐노피를 같은 업체가 직접 와서 합니다. 사진을 같이 보내 주시면 한 번에 견적 드립니다."))
    faq.append(("견적을 받으려면 무엇을 보내야 하나요?",
                "전체가 보이는 사진, 문제 부위 가까이 찍은 사진, 그리고 주소(동네까지)면 됩니다. 종목별로 보내 주실 사진은 견적 문의 안내에 정리해 두었습니다."))
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": canonical,
                     "description": desc, "inLanguage": "ko",
                     "about": {"@type": "City", "name": c["official"]},
                     "publisher": {"@type": "Organization", "name": S["name"], "telephone": S["phone"]}}, ensure_ascii=False)
    region = {"kind": "city", "name": c["name"]}
    fq = "".join('<div class="fq"><b><i>Q</i>%s</b><p>%s</p></div>' % (html.escape(q), html.escape(a)) for q, a in faq)
    body = """<div class="crumb"><div class="wrap"><a href="%s">출장 지역</a><span>&rsaquo;</span>%s</div></div>
<section class="hero"><div class="wrap">
<h1>%s 출장 시공</h1>
<p class="sub">우수관 · 트렌치 · 보도블록 · 카스토퍼 · 에어컨 배관 · 렉산 캐노피 — %s 어디든 같은 업체가 직접 와서 합니다.</p>
%s
%s
</div></section>
<section class="q"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>%s에서 하는 일</h2>
  <p>공사 종류를 누르면 %s 안내로 갑니다.</p></div>
  <div class="qg">%s</div>
</div></section>
%s<section class="faq"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>%s 시공 <em>자주 묻는 질문</em></h2></div>
  <div class="fqlist">%s</div>
  <div class="links" style="margin-top:18px"><a href="/contact.html">견적 문의 · 사진 보내는 법<i>&rsaquo;</i></a></div>
</div></section>
""" % (url(), html.escape(c["short"]), html.escape(c["short"]), html.escape(c["official"]),
       b.trust(region), b.ctabtns(), html.escape(c["short"]), html.escape(c["short"]), _cards(b, c),
       b.area(None, base), html.escape(c["short"]), fq)
    return b.head(title, desc, canonical, ld, False, None) + b.header(None) + body + b.footer(FOOT)


def index(b):
    S = b.SITE
    title = "출장 지역 — 서울·인천·경기·충청 | %s" % S["name"]
    desc = "서울·인천·경기 전역, 충청 전 시군 출장. 사는 곳을 누르면 그 도시에서 하는 공사 안내로 갑니다. 사진 보내주시면 당일 견적 회신. %s" % S["phone"]
    canonical = S["domain"] + url()
    blocks = []
    for g in cities.GROUPS:
        rows = "".join('<a href="%s">%s</a>' % (url(c), html.escape(c["short"])) for c in cities.CITIES if c["group"] == g)
        if rows:
            blocks.append('<div class="cg"><b>%s</b><div>%s</div></div>' % (g, rows))
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": canonical,
                     "description": desc, "inLanguage": "ko"}, ensure_ascii=False)
    body = """<section class="hero"><div class="wrap">
<h1>출장 지역</h1>
<p class="sub">서울 · 인천 · 경기 전역, 충청 전 시군에 갑니다. 사는 곳을 누르면 그 도시에서 하는 공사 안내로 갑니다.</p>
%s
</div></section>
<section class="cdir"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>도시별 <em>안내</em></h2>
  <p>목록에 없는 곳도 연락 주시면 갈 수 있는지 바로 알려 드립니다.</p></div>
  %s
</div></section>
""" % (b.ctabtns(), "".join(blocks))
    return b.head(title, desc, canonical, ld, False, None) + b.header(None) + body + b.footer(FOOT)


def build(b):
    import os
    out = []
    os.makedirs(os.path.join(b.DIST, DIR), exist_ok=True)
    b.write(os.path.join(b.DIST, DIR, "index.html"), index(b)); out.append(url())
    for c in cities.CITIES:
        b.write(os.path.join(b.DIST, DIR, c["slug"] + ".html"), page(b, c)); out.append(url(c))
    print("도시 안내 %d장 + 목록 → /%s/" % (len(out) - 1, DIR))
    return out
