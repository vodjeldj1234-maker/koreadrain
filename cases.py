# -*- coding: utf-8 -*-
"""
시공 사례 빌더 — /trench/case/{slug}.html + 목록 /trench/case/  (2026-09-17, 홈페이지제작 31째방)

■ 현장 1곳 = 사례 1편. 데이터는 data.py 의 TRENCH_CASES (TRENCH["cases"]).
■ ⚠ 지역 격리 — 사례에는 지역명을 쓰지 않는다. 사례 카드가 트렌치 첫 페이지와 지역 페이지 24곳 전부에 똑같이 붙기 때문이다.
     (주인님 결정 2026-09-17: "수원 페이지로 들어왔을 때 다른 지역 시공사례가 안 보이면 안 된다" → 지역명 없는 사례를 어디서나 보여준다)
■ ⚠ 서비스 격리 — 링크는 트렌치 안에서만 (/trench/ · /trench/case/).
■ 사진: img/case/{slug}-{NN}.jpg (960×960). 캡션은 사진에 찍힌 것만. 요약은 사진과 현장 폴더 이름에 있는 것만.
■ 새 현장이 생기면 TRENCH_CASES 에 1편 추가 → 모든 트렌치 페이지에 자동으로 뜬다.
"""
import os, html, json

DIR    = "trench/case"
CARD_N = 6          # 지역 페이지에 보이는 카드 수 (나머지는 "전체 보기")

CSS = r"""
.cases .cgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.cases a.ccard{display:block;text-decoration:none;color:#16202a;background:#fff;border:1px solid #e3e6e9;border-radius:10px;overflow:hidden}
.cases a.ccard img{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;display:block}
.cases a.ccard b{display:block;padding:10px 12px 2px;font-size:15px;line-height:1.45;letter-spacing:-.5px}
.cases a.ccard span{display:block;padding:0 12px 12px;color:#6b7885;font-size:13px}
.post .shots{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:6px 0 10px}
.post .shots figure{margin:0}
.post .shots figcaption b{display:block;color:#E0521A;font-size:13px;margin-top:6px}
.post .shots figcaption span{display:block;color:#16202a;font-size:14.5px;font-weight:700;line-height:1.45}
.post .shots figcaption i{display:block;color:#6b7885;font-size:13px;font-style:normal}
@media(max-width:760px){.cases .cgrid{grid-template-columns:repeat(2,1fr);gap:10px}.post .shots{grid-template-columns:1fr}}
"""

def url(c=None):
    return "/%s/%s.html" % (DIR, c["slug"]) if c else "/%s/" % DIR

def img(c, n):
    return "/img/case/%s-%02d.jpg" % (c["slug"], n)

def section(b, cases, offset=0):
    """트렌치 첫 페이지 · 지역 페이지에 붙는 사례 카드. offset 으로 지역마다 앞에 오는 사례를 돌려 쓴다."""
    if not cases:
        return ""
    k = len(cases)
    pick = [cases[(offset + i) % k] for i in range(min(CARD_N, k))]
    cards = "".join('<a class="ccard" href="%s">%s<b>%s</b><span>사진 %d장</span></a>'
                    % (url(c), b.imgtag(img(c, c["cover"]), c["title"]), html.escape(c["title"]), len(c["photos"]))
                    for c in pick)
    return """<section class="cases"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>트렌치 <em>시공 사례</em></h2>
  <p>현장 하나를 처음부터 끝까지 사진 순서대로 정리했습니다.</p></div>
  <div class="cgrid">%s</div>
  <div class="more"><a href="%s">시공 사례 전체 %d곳 보기</a></div>
</div></section>
<style>%s</style>
""" % (cards, url(), k, CSS)

def build(b, cases):
    """b = build 모듈. 만든 URL 목록을 돌려준다."""
    import info
    SITE = b.SITE
    urls = []
    if not cases:
        return urls
    cfg = info.SERVICES["트렌치"]
    crumb = '<div class="icrumb"><div class="wrap"><a href="/trench/">%s</a><span>›</span><a href="%s">시공 사례</a>%s</div></div>\n'

    def shell(title, desc, canonical, ld, body, og=None, tail=""):
        h = b.head(title, desc, canonical, ld, False, og)
        h = h.replace("</style>", info.EXTRA_CSS + CSS + "</style>", 1)
        return h + b.header(None) + crumb % (SITE["name"], url(), tail) + body + info._footer(b, cfg)

    def ym(c):
        y, m = c["date"].split("-")
        return "%s년 %d월" % (y, int(m))

    for c in cases:
        canonical = SITE["domain"] + url(c)
        shots = "".join(
            '<figure>%s<figcaption><b>%02d · %s</b><span>%s</span>%s</figcaption></figure>'
            % (b.imgtag(img(c, n), t), n, html.escape(lb), html.escape(t), ("<i>%s</i>" % html.escape(d)) if d else "")
            for n, (lb, t, d) in enumerate(c["photos"], 1))
        others = "".join('<a href="%s">%s<span>%s · 사진 %d장</span></a>'
                         % (url(o), html.escape(o["title"]), ym(o), len(o["photos"])) for o in cases if o is not c)
        body = """<section class="post"><div class="wrap">
<h1>%s</h1>
<div class="meta">%s 시공 · %s · 사진 %d장</div>
<p class="lead">%s</p>
<div class="shots">%s</div>
<div class="cta"><b>사진 4장 보내주시면 당일 견적 회신</b><p>%s</p>%s
<a class="home" href="/trench/">%s</a></div>
<div class="rel"><h2>다른 시공 사례</h2>%s</div>
</div></section>
""" % (html.escape(c["title"]), ym(c), SITE["name"], len(c["photos"]), html.escape(c["summary"]), shots,
       cfg["cta_sub"], b.ctabtns(), cfg["cta_link"] % SITE["name"], others)
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Article", "headline": c["title"], "description": c["summary"], "inLanguage": "ko",
             "mainEntityOfPage": canonical,
             "author": {"@type": "Organization", "name": SITE["name"]},
             "publisher": {"@type": "Organization", "name": SITE["name"], "url": SITE["domain"]},
             "image": [SITE["domain"] + img(c, n) for n in range(1, len(c["photos"]) + 1)]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "트렌치 보수", "item": SITE["domain"] + "/trench/"},
                {"@type": "ListItem", "position": 2, "name": "시공 사례", "item": SITE["domain"] + url()},
                {"@type": "ListItem", "position": 3, "name": c["title"], "item": canonical}]}]}
        page = shell(c["title"] + " | 트렌치 시공 사례 | " + SITE["name"], c["summary"][:150], canonical,
                     json.dumps(ld, ensure_ascii=False), body, img(c, c["cover"]),
                     '<span>›</span><span>%s</span>' % html.escape(c["title"][:22] + ("…" if len(c["title"]) > 22 else "")))
        b.write(os.path.join(b.DIST, DIR, c["slug"] + ".html"), page)
        urls.append(url(c))

    # 목록
    cards = "".join('<a class="ccard" href="%s">%s<b>%s</b><span>%s 시공 · 사진 %d장</span></a>'
                    % (url(c), b.imgtag(img(c, c["cover"]), c["title"]), html.escape(c["title"]), ym(c), len(c["photos"]))
                    for c in cases)
    title = "트렌치 시공 사례 %d곳 | %s" % (len(cases), SITE["name"])
    desc = "트렌치 · 배수로 신설, 앵글 교체, 무소음 덮개 교체, 측구 보수, 배수로 청소 — 현장마다 시공 전부터 완료까지 사진 순서대로 정리했습니다."
    canonical = SITE["domain"] + url()
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "url": canonical,
          "isPartOf": {"@type": "WebSite", "name": SITE["name"], "url": SITE["domain"]}}
    body = """<section class="plist cases"><div class="wrap">
<h1>트렌치 시공 사례</h1>
<p class="intro">현장 하나를 처음부터 끝까지 사진 순서대로 정리했습니다. %d곳.</p>
<div class="cgrid">%s</div>
</div></section>
""" % (len(cases), cards)
    b.write(os.path.join(b.DIST, DIR, "index.html"), shell(title, desc, canonical, json.dumps(ld, ensure_ascii=False), body))
    urls.append(url())
    print("시공 사례(트렌치) %d곳 → /%s/" % (len(cases), DIR))
    return urls
