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

# ── 연락 요소 (2026-09-05 추가)
#   ⚠ 전화 링크 하나뿐이면 PC 로 보는 손님은 연락할 방법이 없다. 문자·번호복사를 같이 낸다.
def trust(region=None):
    """첫 화면 신뢰 3줄. 3번째는 그 페이지에 맞는 출장 범위."""
    where = ("%s 인근까지 출장" % region["name"]) if region \
            else "서울 · 인천 · 경기 전역, 충청 전 시군 출장"
    return '<div class="trust">%s</div>' % "".join(
        '<div><i>✓</i><span>%s</span></div>' % html.escape(t)
        for t in list(SITE["trust"]) + [where])

def ctabtns():
    """전화 + 문자 두 버튼. sms: 는 본문 없이 번호만 넣어야 안드로이드·아이폰 둘 다 열린다."""
    return ('<div class="btns">'
            '<a class="btn call" href="tel:%s">📞 전화 걸기</a>'
            '<a class="btn sms" href="sms:%s">💬 사진 문자 보내기</a></div>'
            % (SITE["phone_raw"], SITE["phone_raw"]))

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
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
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

# ── 내부 링크 (2026-09-05 추가, 27째방)
#   "서비스 격리" 는 서비스끼리의 얘기다. 같은 서비스 안에서는 이어도 된다.
#   - 우수관: 지역 페이지 → 메인 "/" 만. 지역끼리는 잇지 않는다 (지역 격리).
#             메인 → 지역도 잇지 않는다 (메인에 타 지역명 노출 금지).
#   - 트렌치: /trench/ ↔ musoeum·gongsa·parking 서로.
#   - 보도블록·카스토퍼: 혼자인 페이지라 링크 없음.
#   ⚠ 서비스 간 링크는 여전히 절대 금지.
def home_of(svc, region=None):
    """이 페이지의 '첫 페이지' 서비스. 자기 자신이 첫 페이지면 None."""
    if region:
        return svc
    return svc.get("parent")

def crumb(svc, region=None):
    home = home_of(svc, region)
    if not home:
        return ""
    here = region["name"] if region else svc["label"]
    return ('<div class="crumb"><div class="wrap"><a href="%s">%s</a><span>&rsaquo;</span>%s</div></div>\n'
            % (url_of(home), home["home_label"], here))

def _link(svc):
    return '<a href="%s">%s<i>&rsaquo;</i></a>' % (url_of(svc), svc["label"])

def navlinks(svc, region=None):
    home = home_of(svc, region)
    kids = svc.get("children")
    if region:
        # 지역 페이지 — 우수관 첫 페이지 하나만
        return ('<section class="nav"><div class="wrap">\n'
                '  <h2>우수관 교체 안내 전체 보기</h2>\n'
                '  <div class="links"><a href="%s">%s<i>&rsaquo;</i></a></div>\n'
                '</div></section>\n' % (url_of(home), home["home_label"]))
    if kids:
        # 첫 페이지 — 하위 페이지 목록
        return ('<section class="nav"><div class="wrap">\n'
                '  <h2>%s 자세히 보기</h2><p>상황별 안내 페이지로 이동합니다.</p>\n'
                '  <div class="links">%s</div>\n'
                '</div></section>\n' % (svc["nav_title"], "".join(_link(k) for k in kids)))
    if home:
        # 하위 페이지 — 형제 + 첫 페이지 (지금 페이지는 검게)
        rows = ""
        for k in home["children"]:
            if k is svc:
                rows += '<a class="me" aria-current="page">%s<i>지금 보는 페이지</i></a>' % k["label"]
            else:
                rows += _link(k)
        rows += '<a href="%s">%s<i>&rsaquo;</i></a>' % (url_of(home), home["home_label"])
        return ('<section class="nav"><div class="wrap">\n'
                '  <h2>다른 %s 안내</h2>\n'
                '  <div class="links">%s</div>\n'
                '</div></section>\n' % (home["nav_title"], rows))
    return ""

def header(svc=None, region=None):
    home = home_of(svc, region) if svc else None
    if home:
        logo = '<a class="logo" href="%s">%s</a>' % (url_of(home), SITE["name"])
    else:
        logo = '<div class="logo">%s</div>' % SITE["name"]
    h = """<header><div class="wrap">%s<a class="hcall" href="tel:%s">%s</a></div></header>
""" % (logo, SITE["phone_raw"], SITE["phone"])
    # ⚠ 서비스 격리 원칙 — 서비스 간 링크를 절대 넣지 않는다.
    #   우수관 문제로 들어온 사람에게 트렌치를, 트렌치 문제로 들어온 사람에게 외벽 작업을
    #   보여주면 이탈만 늘어난다. 각 서비스 페이지는 그 서비스만 보이는 독립 사이트처럼 동작한다.
    #   서비스 간 이동 경로는 만들지 않는다. 유입은 검색 + 사이트맵 + 블로그 링크로만 받는다.
    #   (같은 서비스 안의 링크는 허용 — 로고·crumb·navlinks·푸터. 2026-09-05)
    return h + (crumb(svc, region) if svc else "")

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
%s%s
    <div class="tri">%s</div>
  </div></div>
</div>
""" % (imgtag(src, alt, lazy=False), top, svc["h1_top"], svc["h1_bottom"], svc["h1_tail"],
       svc["sub"], trust(region), ctabtns(), tri)

def gallery(svc, region=None):
    slug = region["slug"] if region else None
    # ⚠ 사진과 문구를 반드시 같이 본다.
    #   지역 페이지는 지역 사진(usugwan-N-{slug}.jpg)을 쓰므로
    #   문구도 그 지역 전용 문구(gallery_by_region)를 써야 어긋나지 않는다.
    rows = svc["gallery"]
    if slug:
        rows = svc.get("gallery_by_region", {}).get(slug, rows)
    items = []
    for i, row in enumerate(rows, start=1):
        lb, title, desc = row[0], row[1], row[2]
        loc = row[3] if len(row) > 3 else None      # 촬영지역 (지역 격리를 안 쓰는 서비스만)
        src = pick("%s-%d" % (svc["key"], i), slug)
        loctag = ('<span class="loc">%s</span>' % html.escape(loc)) if loc else ""
        items.append(
            '<div class="item">%s<span class="lb">%s</span>'
            '<div class="cp">%s%s<span>%s</span></div></div>'
            % (imgtag(src, (loc + " " + title) if loc else title), lb, title, loctag, desc))
    # 서비스가 자기 문구를 갖고 있으면 그걸 쓴다 (없으면 기본 문구)
    if svc.get("gal_h2"):
        h2, p = svc["gal_h2"], svc["gal_p"]
    else:
        where = (region["name"] + " ") if region else ""
        h2 = "다녀온 현장 <em>%d곳</em>에서 고른 사진입니다" % SITE["sites_done"]
        p = "업체 고르실 때 결국 사진 보시잖아요. %s저희가 시공한 현장 그대로 올렸습니다." % where
    return """<section><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>%s</h2>
  <p>%s</p></div>
  <div class="gal">%s</div>
  <div class="more"><a href="tel:%s">전화 주시면 현장 사진 더 보내드립니다</a></div>
</div></section>
""" % (h2, p, "".join(items), SITE["phone_raw"])


def area(svc, region=None):
    """출장 지역 섹션.
    - 지역 페이지: region 자체에 "area" 가 있으면 그 권역만 보여준다 (지역 격리 유지)
    - 메인/서비스 페이지: svc["area"] 를 쓴다 (트렌치처럼 격리 안 쓰는 서비스)
    """
    a = region.get("area") if region is not None else svc.get("area")
    if not a:
        return ""
    rows = "".join('<div class="ar"><b>%s</b><span>%s</span></div>' % (t, v)
                   for t, v in a["groups"])
    return """<section class="area"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>%s</h2>
  <p>%s</p></div>
  <div class="arlist">%s</div>
  <p class="artail">%s</p>
</div></section>
""" % (a["h2"], a["sub"], rows, a["tail"])

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
        # ⚠ 2026-09-03 수정 — 사진이 없을 때 imgtag 가 빈 회색 박스를 내보내
        #    새 서비스 페이지에 정체불명의 빈 칸이 그대로 배포된 사고가 있었다.
        #    사진이 없으면 이미지 자리를 아예 만들지 않고 글자 카드만 낸다.
        img = imgtag(src, "견적 사진 예시 " + t) if src else ""
        cells.append('<div class="cell">%s<div class="t"><b>%s</b><span>%s</span></div></div>'
                     % (img, t, d))
    return """<section class="q"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>견적 문의</h2></div>
  <div class="warn"><b>사진을 꼭 보내주세요</b><span>사진 없이는 정확한 금액을 드릴 수 없습니다. 4장이면 충분합니다.</span></div>
  <div class="qg">%s</div>
  <div class="qcta">
    <span class="n">%s</span>
    %s
    <button class="copy" type="button" data-num="%s">%s<span>PC 에서 쓰는 버튼</span></button>
    <p class="qnote">문자로 사진 4장만 보내주시면 확인 후 금액 회신드립니다.</p>
  </div>
</div></section>
""" % ("".join(cells), SITE["phone"], ctabtns(), SITE["phone"], "번호 복사")

# ── 네이버 검색광고 전환추적 (2026-08-26 자가설치 · 2026-08-28 전환이벤트 추가)
#
#   [1] 공통 스크립트 — 네이버 설치안내메일의 "2. 공통 스크립트" 원문 그대로. 임의로 고치지 말 것.
#   [2] 전환 스크립트 — 전화 링크 클릭을 "신청완료(lead)" 전환으로 보낸다.
#
#   ★ 전환유형을 lead 로 고른 근거 (naver.github.io/conversion-tracking 공식 가이드)
#     - 우리 사이트는 가이드의 "2. 비커머스"(병원·제품소개·창업문의 사이트) 유형이다.
#     - 신청완료의 코드명이 lead 다. 한글명을 넣으면 안 되고 반드시 코드명을 넣어야 한다.
#     - 구매·장바구니·회원가입은 우리 사이트에 존재하지 않으므로 쓰면 안 된다.
#   ★ 구 방식(wcs.cnv 숫자코드)과 신 방식(wcs.trans)을 섞지 말 것.
#     같은 유형이 두 방식으로 들어오면 구 방식 전환이 영구 필터링된다. 우리는 trans 만 쓴다.
#   ★ value(금액)는 lead 에서 선택항목이다. 견적 금액을 모르므로 넣지 않는다.
#   ★ 한 페이지에서 여러 번 눌러도 전환은 1회만 보낸다 (중복 집계 방지).
#   ★ 전화 링크는 헤더 전화번호·갤러리 하단·견적문의 버튼·하단 고정버튼 4곳 모두 잡힌다.
#   ⚠ 인증키는 data.py SITE["naver_wa"] 한 곳에서만 관리한다.
#   ⚠ 설치 후 네이버에 "데이터 검수요청"(전환유형 = 신청 완료)을 해야 수집이 시작된다.
NAVER_WCS = """<script type="text/javascript" src="//wcs.naver.net/wcslog.js"></script>
<script type="text/javascript">
if(!wcs_add) var wcs_add={};
wcs_add["wa"] = "%s";
if(!_nasa) var _nasa={};
if(window.wcs){
wcs.inflow();
wcs_do();
}
(function(){
  var sent = false;
  document.addEventListener("click", function(e){
    if (sent) return;
    var n = e.target;
    while (n && n.nodeType === 1) {
      if (n.tagName === "A" && /^(tel:|sms:)/.test(n.getAttribute("href") || "")) break;
      if (n.tagName === "BUTTON" && n.className.indexOf("copy") >= 0) break;
      n = n.parentNode;
    }
    if (!n || n.nodeType !== 1) return;
    sent = true;
    try {
      if (window.wcs && wcs.trans) {
        var _conv = {};
        _conv.type = "lead";
        wcs.trans(_conv);
      }
    } catch (err) {}
  }, true);
})();
</script>
""" % SITE["naver_wa"]

# 번호 복사 버튼 — PC 손님이 전화번호를 옮겨 적을 수 있게 한다.
# https 사이트라 clipboard API 가 되지만, 안 되는 브라우저를 위해 옛 방식도 남겨둔다.
COPY_JS = """<script>
document.addEventListener("click", function (e) {
  var b = e.target;
  while (b && b.nodeType === 1 && !(b.tagName === "BUTTON" && b.className.indexOf("copy") >= 0)) b = b.parentNode;
  if (!b || b.nodeType !== 1) return;
  var num = b.getAttribute("data-num");
  function done() { b.className = "copy done"; b.firstChild.nodeValue = "복사했습니다 " + num; }
  function old() {
    var t = document.createElement("textarea");
    t.value = num; t.style.position = "fixed"; t.style.opacity = "0";
    document.body.appendChild(t); t.select();
    try { document.execCommand("copy"); done(); } catch (x) {}
    document.body.removeChild(t);
  }
  if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(num).then(done, old);
  else old();
});
</script>
"""

def footer(svc, region=None):
    line = svc["foot"]
    if region:
        line = "%s %s" % (region["name"], line)
    home = home_of(svc, region)
    homeln = ('<br><a class="fhome" href="%s">%s</a>' % (url_of(home), home["home_label"])) if home else ""
    return """<footer>%s · %s<br>%s%s
<span class="biz">상호 %s &middot; 대표 %s &middot; 사업자등록번호 %s<br>%s</span></footer>
<div class="fixed"><a class="f-call" href="tel:%s">📞 전화 걸기</a><a class="f-sms" href="sms:%s">💬 사진 문자</a></div>
%s%s</body></html>""" % (SITE["name"], SITE["phone"], line, homeln,
                     SITE["name"], SITE["biz_owner"], SITE["biz_no"], SITE["biz_addr"],
                     SITE["phone_raw"], SITE["phone_raw"], COPY_JS, NAVER_WCS)

# ────────────────────────────────────────────────────────── JSON-LD
def jsonld(svc, region=None):
    import json
    hero = pick("hero-" + svc["key"], region["slug"] if region else None)
    if region:
        area = [{"@type": "City", "name": c} for c in region["cities"]]
    elif svc.get("cities"):                      # 지역 격리를 안 쓰는 서비스는 자기 목록을 쓴다
        area = [{"@type": "City", "name": c} for c in svc["cities"]]
    else:
        area = [{"@type": "City", "name": c} for r in REGIONS for c in r["cities"]]
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
    # "file" 이 있으면 그 서비스는 /{dir}/{file} 한 장으로 나간다 (하위 페이지).
    if svc.get("file"):
        return "/%s/%s" % (svc["dir"], svc["file"])
    return "/" if svc["at_root"] else "/%s/" % svc["dir"]

def path_of(svc, region=None):
    if region:
        return os.path.join(DIST, svc["dir"], region["slug"] + ".html")
    if svc.get("file"):
        return os.path.join(DIST, svc["dir"], svc["file"])
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
            + area(svc, region) + focus(svc, region) + faq(svc, region)
            + navlinks(svc, region) + quote(svc, region) + footer(svc, region))

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
        # regions=False 인 서비스는 지역 페이지를 만들지 않는다 (한 페이지 + 출장지역 공개 방식)
        if svc.get("regions", True):
            for r in REGIONS:
                write(path_of(svc, r), page(svc, r));  urls.append(url_of(svc, r))

    # 사진 복사
    if os.path.isdir(IMG):
        shutil.copytree(IMG, os.path.join(DIST, "img"))

    # 파비콘 — 없으면 네이버 서치어드바이저가 favicon.ico 를 400 으로 잡아
    # "접근 불가한 페이지(수집제한)" 로 기록한다. (2026-08-28 실제로 1건 발생)
    for f in ("favicon.ico", "apple-touch-icon.png"):
        if os.path.exists(f):
            shutil.copy2(f, os.path.join(DIST, f))

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