# -*- coding: utf-8 -*-
"""
koreadrain.kr 정적 사이트 빌더
사용법: 이 폴더에서  python build.py   →  dist/ 폴더 생성 → Netlify 에 드래그&드롭

지역 격리 원칙:
  어떤 페이지에서도 다른 지역 이름이 고객 눈에 보이지 않는다.
  지역명은 JSON-LD(검색엔진용)와 해당 지역 페이지 본문에만 존재한다.

서비스 격리 원칙:
  우수관 페이지와 트렌치 페이지는 서로를 노출하지 않는다.
  서비스 간 링크도, 타 서비스 문구도 넣지 않는다. 각 서비스는 독립 사이트처럼 동작한다.
"""
import os, shutil, html
from data import SITE, REGIONS, SERVICES
from style import CSS

DIST = "dist"
IMG  = "img"

# ─────────────────────────────────────────────────────────── 사진 헬퍼
def pick(basename, slug=None):
    """지역 전용 사진이 있으면 그걸, 없으면 공통 사진을 쓴다."""
    if slug:
        cand = "%s-%s.jpg" % (basename, slug)
        if os.path.exists(os.path.join(IMG, cand)):
            return "/img/" + cand
    common = basename + ".jpg"
    if os.path.exists(os.path.join(IMG, common)):
        return "/img/" + common
    return None

def imgtag(src, alt, cls="ph", lazy=True):
    if not src:
        return '<div class="%s" aria-hidden="true"></div>' % cls
    # 첫 화면(히어로) 사진만 즉시 로딩, 나머지는 스크롤해서 보일 때 로딩한다.
    # → 방문자 대부분이 아래까지 안 내려가므로 Netlify 대역폭(크레딧)이 크게 절약된다.
    extra = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    return '<img class="%s" src="%s" alt="%s"%s>' % (cls, src, html.escape(alt), extra)

# ─────────────────────────────────────────────────────────── 페이지 조각
def head(title, desc, canonical, jsonld, is_index, og_img=None):
    verify = ""
    if is_index:
        verify = ('<meta name="naver-site-verification" content="%s">\n'
                  '<meta name="google-site-verification" content="%s">\n'
                  % (SITE["naver_verify"], SITE["google_verify"]))
    og = ""
    if og_img:
        abs_img = SITE["domain"] + og_img
        og = ('<meta property="og:image" content="%s">\n'
              '<meta name="twitter:card" content="summary_large_image">\n'
              '<meta name="twitter:image" content="%s">\n' % (abs_img, abs_img))
    return """<!DOCTYPE html><html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
%s<meta property="og:type" content="website">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:site_name" content="%s">
%s<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=IBM+Plex+Mono:wght@600&display=swap" rel="stylesheet">
<style>%s</style>
<script type="application/ld+json">%s</script>
</head><body>
""" % (html.escape(title), html.escape(desc), canonical, verify,
       html.escape(title), html.escape(desc), canonical, SITE["name"], og, CSS, jsonld)

def header(svc=None, region=None):
    h = """<header><div class="wrap"><div class="logo">%s</div><a class="hcall" href="tel:%s">%s</a></div></header>
""" % (SITE["name"], SITE["phone_raw"], SITE["phone"])
    # ⚠ 서비스 격리 원칙 — 서비스 간 링크를 절대 넣지 않는다.
    #   우수관 문제로 들어온 사람에게 트렌치를, 트렌치 문제로 들어온 사람에게 외벽 작업을
    #   보여주면 이탈만 늘어난다. 각 서비스 페이지는 그 서비스만 보이는 독립 사이트처럼 동작한다.
    #   서비스 간 이동 경로는 만들지 않는다. 유입은 검색 + 사이트맵 + 블로그 링크로만 받는다.
    return h

def hero(svc, region=None):
    slug = region["slug"] if region else None
    src  = pick("hero-" + svc["key"], slug)
    top  = (region["name"] + " ") if region else ""
    alt  = "%s%s 시공 현장" % (top, svc["label"])
    tri  = "".join('<div><b>%s</b><span>%s</span></div>' % (a, b) for a, b in svc["tri"])
    return """<div class="hero">
%s
  <div class="cap"><div class="wrap">
    <h1>%s%s<br><em>%s</em> %s</h1>
    <p>%s</p>
    <div class="tri">%s</div>
  </div></div>
</div>
""" % (imgtag(src, alt, lazy=False), top, svc["h1_top"], svc["h1_bottom"], svc["h1_tail"], svc["sub"], tri)

def gallery(svc, region=None):
    slug = region["slug"] if region else None
    items = []
    for i, (lb, title, desc) in enumerate(svc["gallery"], start=1):
        src = pick("%s-%d" % (svc["key"], i), slug)
        items.append(
            '<div class="item">%s<span class="lb">%s</span>'
            '<div class="cp">%s<span>%s</span></div></div>'
            % (imgtag(src, title), lb, title, desc))
    where = (region["name"] + " ") if region else ""
    return """<section><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>직접 한 <em>시공 사진</em>입니다</h2>
  <p>업체 고르실 때 결국 사진 보시잖아요. %s저희가 시공한 현장 그대로 올렸습니다.</p></div>
  <div class="gal">%s</div>
  <div class="more"><a href="tel:%s">더 많은 시공 사진 보기</a></div>
</div></section>
""" % (where, "".join(items), SITE["phone_raw"])

def focus(svc, region=None):
    slug = region["slug"] if region else None
    f = svc["focus"]
    shots = "".join(imgtag(pick("%s-%d" % (f["img"], i), slug),
                           "%s %d" % (f["alt"], i)) for i in (1, 2))
    rows = "".join('<div><div class="ck">✓</div><div><b>%s</b><span>%s</span></div></div>' % (a, b)
                   for a, b in f["items"])
    return """<section class="sil"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>%s</h2>
  <p>%s</p></div>
  <div class="silbig">%s</div>
  <div class="silrow">%s</div>
</div></section>
""" % (f["h2"], f["sub"], shots, rows)

def faq_items(svc, region=None):
    """이 페이지에 나갈 FAQ 목록을 (질문, 답변) 으로 돌려준다.
       지역 격리 — {region} 은 그 페이지 지역명으로만 치환된다."""
    out = []
    for scope, q, a in svc.get("faq", []):
        if scope == "region" and region is None:
            continue
        if scope == "main" and region is not None:
            continue
        name = region["name"] if region else ""
        out.append((q.format(region=name), a.format(region=name)))
    return out

def faq(svc, region=None):
    items = faq_items(svc, region)
    if not items:
        return ""
    rows = "".join(
        '<div class="fq"><b><i>Q</i>%s</b><p>%s</p></div>'
        % (html.escape(q), html.escape(a)) for q, a in items)
    return """<section class="faq"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>자주 묻는 <em>질문</em></h2>
  <p>전화 주시기 전에 궁금하신 것들, 먼저 정리해뒀습니다.</p></div>
  <div class="fqlist">%s</div>
</div></section>
""" % rows

def quote(svc, region=None):
    slug = region["slug"] if region else None
    cells = []
    for i, (t, d) in enumerate(svc["guide"], start=1):
        src = pick("%s-%d" % (svc["guide_img"], i), slug)
        cells.append('<div class="cell">%s<div class="t"><b>%s</b><span>%s</span></div></div>'
                     % (imgtag(src, "견적 사진 예시 " + t), t, d))
    return """<section class="q"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>견적 문의</h2></div>
  <div class="warn"><b>사진을 꼭 보내주세요</b><span>사진 없이는 정확한 금액을 드릴 수 없습니다. 4장이면 충분합니다.</span></div>
  <div class="qg">%s</div>
  <div class="qcta">
    <p style="color:#b7c3cd">문자 · 카톡으로 사진 전송해주시면 확인 후 바로 금액 회신드립니다.</p>
    <span class="n">%s</span>
    <a href="tel:%s">📞 전화 / 사진 전송</a>
  </div>
</div></section>
""" % ("".join(cells), SITE["phone"], SITE["phone_raw"])

def footer(svc, region=None):
    line = svc["foot"]
    if region:
        line = "%s %s" % (region["name"], line)
    return """<footer>%s · %s<br>%s</footer>
<a class="fixed" href="tel:%s">📞 사진 보내고 견적 받기</a>
</body></html>""" % (SITE["name"], SITE["phone"], line, SITE["phone_raw"])

# ────────────────────────────────────────────────────────── JSON-LD
def jsonld(svc, region=None):
    import json
    hero = pick("hero-" + svc["key"], region["slug"] if region else None)
    area = ([{"@type": "City", "name": c} for c in region["cities"]] if region
            else [{"@type": "City", "name": c} for r in REGIONS for c in r["cities"]])
    name = SITE["name"] + ((" " + region["name"]) if region else "")
    d = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": name,
        "telephone": SITE["phone"],
        "url": SITE["domain"] + url_of(svc, region),
        "areaServed": area,
        "image": ([SITE["domain"] + hero] if hero else []),
        "makesOffer": [{"@type": "Offer", "itemOffered": {
            "@type": "Service", "name": svc["offer"]}}],
    }
    graph = [d]
    # FAQPage — AI 검색·구글 스니펫이 질문-답변 쌍을 그대로 가져간다.
    # 화면에 안 보이는 질문을 넣으면 규정 위반이므로, 반드시 faq() 가 출력하는 것과 같은 목록을 쓴다.
    qas = faq_items(svc, region)
    if qas:
        graph.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            } for q, a in qas],
        })
    return json.dumps(graph, ensure_ascii=False)

# ─────────────────────────────────────────────────────────── URL / 출력
def url_of(svc, region=None):
    if region:
        return "/%s/%s.html" % (svc["dir"], region["slug"])
    return "/" if svc["at_root"] else "/%s/" % svc["dir"]

def path_of(svc, region=None):
    if region:
        return os.path.join(DIST, svc["dir"], region["slug"] + ".html")
    return os.path.join(DIST, "index.html") if svc["at_root"] \
        else os.path.join(DIST, svc["dir"], "index.html")

def page(svc, region=None):
    if region:
        title = svc["title_r"].format(region=region["name"], site=SITE["name"])
        desc  = svc["desc_r"].format(region=region["name"], phone=SITE["phone"])
    else:
        title = svc["title_m"].format(site=SITE["name"])
        desc  = svc["desc_m"].format(phone=SITE["phone"])
    canonical = SITE["domain"] + url_of(svc, region)
    og_img = pick("hero-" + svc["key"], region["slug"] if region else None)
    return (head(title, desc, canonical, jsonld(svc, region), region is None, og_img)
            + header(svc, region) + hero(svc, region) + gallery(svc, region)
            + focus(svc, region) + faq(svc, region)
            + quote(svc, region) + footer(svc, region))

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

# ─────────────────────────────────────────────────────────── IndexNow (자동 색인 요청)
# 네이버·Bing 등에 "이 주소들 바뀌었다"고 사이트가 직접 알린다.
# 사람이 검색엔진에 들어가서 주소를 하나씩 넣던 일을 대신한다.
# 구글은 IndexNow 에 참여하지 않는다. 구글은 sitemap.xml 이 담당한다.
INDEXNOW_KEY = "23b09e70317a160a2a7caeaf1d88ae66"

def indexnow(urls):
    """Netlify 실서비스 배포일 때만 보낸다. 실패해도 배포는 절대 안 깨진다."""
    # Netlify 는 CONTEXT, Cloudflare Pages 는 CF_PAGES 로 실서비스 배포인지 알려준다.
    # 둘 다 알아듣게 해두면 호스팅을 옮겨도 이 부분을 다시 고칠 필요가 없다.
    on_netlify = os.environ.get("CONTEXT") == "production"
    on_cloudflare = (os.environ.get("CF_PAGES") == "1"
                     and os.environ.get("CF_PAGES_BRANCH") == "main")
    on_github = (os.environ.get("GITHUB_ACTIONS") == "true"
                 and os.environ.get("GITHUB_REF_NAME") == "main")
    if not (on_netlify or on_cloudflare or on_github):
        print("IndexNow 건너뜀 (실서비스 배포가 아님)")
        return
    import json, urllib.request
    body = json.dumps({
        "host": SITE["domain"].split("//", 1)[1],
        "key": INDEXNOW_KEY,
        "keyLocation": "%s/%s.txt" % (SITE["domain"], INDEXNOW_KEY),
        "urlList": [SITE["domain"] + u for u in urls],
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=body, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print("IndexNow 제출 완료 - 주소 %d개 (응답코드 %d)" % (len(urls), r.status))
    except Exception as e:
        print("IndexNow 제출 실패 - 무시하고 배포는 계속한다: %s" % e)

# ─────────────────────────────────────────────────────────── 빌드
def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    urls = []
    for svc in SERVICES:
        write(path_of(svc), page(svc));            urls.append(url_of(svc))
        for r in REGIONS:
            write(path_of(svc, r), page(svc, r));  urls.append(url_of(svc, r))

    # 사진 복사
    if os.path.isdir(IMG):
        shutil.copytree(IMG, os.path.join(DIST, "img"))

    # sitemap.xml  — lastmod 를 넣어야 검색엔진이 "바뀌었다"를 스스로 알다
    import datetime
    today = datetime.date.today().isoformat()
    items = "".join('<url><loc>%s%s</loc><lastmod>%s</lastmod>'
                    '<changefreq>monthly</changefreq></url>'
                    % (SITE["domain"], u, today) for u in urls)
    write(os.path.join(DIST, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % items)

    # robots.txt
    write(os.path.join(DIST, "robots.txt"),
          "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["domain"])

    # _redirects — extra/_redirects 파일이 있으면 그 내용을 그대로 사용
    extra = os.path.join("extra", "_redirects")
    rules = open(extra, encoding="utf-8").read() if os.path.exists(extra) else ""
    rules += "\nhttp://koreadrain.kr/*   https://koreadrain.kr/:splat   301!\n"
    write(os.path.join(DIST, "_redirects"), rules)

    # IndexNow 인증키 파일 - 사이트 루트에 있어야 검색엔진이 우리를 믿는다
    write(os.path.join(DIST, INDEXNOW_KEY + ".txt"), INDEXNOW_KEY)

    # GitHub Pages 용
    #  CNAME    : 이게 없으면 배포할 때마다 koreadrain.kr 연결이 풀린다
    #  .nojekyll: GitHub 이 밑줄(_)로 시작하는 파일을 지워버리는 걸 막는다
    write(os.path.join(DIST, "CNAME"), SITE["domain"].split("//", 1)[1] + "\n")
    write(os.path.join(DIST, ".nojekyll"), "")

    print("빌드 완료 → %s/  (%d 페이지)" % (DIST, len(urls)))
    for u in urls:
        print("   ", u)

    indexnow(urls)

if __name__ == "__main__":
    main()