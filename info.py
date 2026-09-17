# -*- coding: utf-8 -*-
"""
정보글 빌더 — koreadrain.kr/info/  (2026-09-16, 워드프레스 2째방에서 추가)

posts/*.txt 를 읽어 /info/{slug}.html 과 목록 /info/ 를 만든다.
build.py main() 에서 `urls += info.build()` 한 줄로 호출된다. 기존 17페이지 코드는 건드리지 않는다.

■ 글 파일 형식 (posts/읽어주세요.txt 에도 있음)
    제목: ...
    슬러그: usugwan-nusu-wonin        ← URL. 한 번 올라가면 바꾸지 않는다
    설명: 검색 결과에 보이는 한두 문장 (150자 안팎)
    키워드: 우수관누수, 우수관교체      ← 관련 글 고를 때 쓴다 (화면엔 안 나옴)
    날짜: 2026-09-16
    ---
    본문 — ## 소제목 / ### 소제목 / - 목록 / | 표 | / [사진 N] / [인용구] 문장 / **강조** / [글자](주소)
    빈 줄 = 문단 구분
    사진 캡션:
    1: 캡션

■ 사진: img/info/{slug}-{N}.jpg  (없으면 [사진 N] 자리는 비운다. 사진에 안 찍힌 걸 캡션에 쓰지 않는다)
■ 원칙: 없는 사실 안 씀 / 금액·연수·건수 지어내지 않음 / "당일 출장·출동·방문" 금지 / 아파트 얘기 안 씀 / 동료 이름 안 씀
■ 링크: 글 끝에 "시공 문의는 포스원" → / (우수관 메인) 한 줄. 트렌치·보도블록 등 다른 서비스로는 잇지 않는다 (서비스 격리)
■ 서비스 (31째방): 머리에 `서비스: 트렌치` 를 쓰면 /trench/info/ 로 나간다. 없으면 우수관 → /info/.
  목록·관련 글·견적 버튼·crumb·푸터 링크가 전부 그 서비스 안에서만 이어진다 (서비스 격리).
"""
import os, re, html, json, glob, datetime

POSTS_DIR = "posts"
INFO_DIR  = "info"
IMG_DIR   = os.path.join("img", "info")
RELATED_N = 3

# 서비스별 설정 (31째방 — 트렌치 정보글 추가)
#   ⚠ 서비스 격리 — 글·목록·관련 글·견적 버튼·crumb·푸터 링크가 전부 자기 서비스 첫 페이지로만 간다.
SERVICES = {
    "우수관": {
        "dir": "info", "home": "/",
        "list_h1": "우수관 · 홈통 · 빗물받이 정보글",
        "list_desc": "우수관 누수 원인, 교체 비용이 정해지는 기준, 막힘과 교체의 구분, 빗물받이·선홈통 시공 순서 — 현장에서 실제로 겪은 것만 정리했습니다.",
        "cta_sub": "새는 자리 · 배관 라인 전체 · 배관 맨 아래 · 건물 외관",
        "cta_link": "시공 문의는 %s 우수관 페이지에서",
        "fhome": "우수관 · 홈통 · 빗물받이 시공 안내",
    },
    "트렌치": {
        "dir": "trench/info", "home": "/trench/",
        "list_h1": "트렌치 · 배수로 정보글",
        "list_desc": "트렌치 · 배수로 보수와 신설에 대해 현장에서 실제로 겪은 것만 정리했습니다.",
        "cta_sub": "배수로 전체 · 물 고이는 자리 · 파손 부위 근접 · 덮개와 앵글 상태",
        "cta_link": "시공 문의는 %s 트렌치 페이지에서",
        "fhome": "트렌치 · 배수로 시공 안내",
    },
    # 32째방 (2026-09-18) — 보도블록 · 카스토퍼 · 에어컨 정보글. 서비스 격리 그대로 (자기 첫 페이지로만)
    "보도블록": {
        "dir": "block/info", "home": "/block/",
        "list_h1": "보도블록 · 경계석 정보글",
        "list_desc": "보도블록이 내려앉는 이유, 경계석 · 점자블록 · 판석 보수까지 현장에서 실제로 겪은 것만 정리했습니다.",
        "cta_sub": "손볼 구간 전체 · 파손 부위 근접 · 옆 바닥과 높이 · 장비 진입로",
        "cta_link": "시공 문의는 %s 보도블록 페이지에서",
        "fhome": "보도블록 · 경계석 시공 안내",
    },
    "카스토퍼": {
        "dir": "carstop/info", "home": "/carstop/",
        "list_h1": "카스토퍼 · 과속방지턱 · 반사경 정보글",
        "list_desc": "카스토퍼 설치 위치와 줄 맞춤, 과속방지턱 · 반사경 · 코너보호대까지 현장에서 실제로 겪은 것만 정리했습니다.",
        "cta_sub": "주차장 전체 · 설치할 자리 · 바닥 근접 · 기존 제품",
        "cta_link": "시공 문의는 %s 카스토퍼 페이지에서",
        "fhome": "카스토퍼 · 과속방지턱 · 반사경 설치 안내",
    },
    "에어컨": {
        "dir": "aircon/info", "home": "/aircon/",
        "list_h1": "에어컨 배관 보온재 · 테이핑 정보글",
        "list_desc": "에어컨 배관 보온재가 삭았을 때 보온재만 교체하는 작업 — 순서, 걸리는 시간, 높은 외벽 작업까지 현장에서 실제로 겪은 것만 정리했습니다.",
        "cta_sub": "배관 전체 · 삭은 부위 근접 · 실외기 쪽 · 건물 외관",
        "cta_link": "시공 문의는 %s 에어컨 배관 페이지에서",
        "fhome": "에어컨 배관 보온재 교체 · 테이핑 안내",
    },
}

EXTRA_CSS = r"""
.post{background:#fff}
.post .wrap{max-width:720px}
.post h1{font-size:30px;line-height:1.4;letter-spacing:-1px;margin-bottom:10px}
.post .meta{color:#6b7885;font-size:13.5px;margin-bottom:26px}
.post .lead{font-size:17px;line-height:1.85;color:#2b3742;background:#FFF3E6;border-left:4px solid #E0521A;padding:14px 16px;border-radius:6px;margin-bottom:26px}
.post h2{font-size:22px;line-height:1.45;margin:38px 0 12px;padding-top:6px;letter-spacing:-.8px}
.post h3{font-size:18px;margin:26px 0 8px;letter-spacing:-.6px}
.post p{font-size:16.5px;line-height:1.9;color:#2b3742;margin-bottom:16px;letter-spacing:-.3px}
.post ul,.post ol{margin:0 0 18px 22px;font-size:16px;line-height:1.85;color:#2b3742}
.post li{margin-bottom:4px}
.post blockquote{background:#f6f7f8;border-left:4px solid #16202a;padding:14px 18px;border-radius:6px;margin:0 0 18px;font-size:16px;line-height:1.8;color:#16202a;font-weight:500}
.post table{width:100%;border-collapse:collapse;font-size:15px;margin:0 0 20px}
.post th,.post td{border:1px solid #e3e6e9;padding:9px 10px;text-align:left;vertical-align:top;line-height:1.6}
.post th{background:#f6f7f8;font-weight:700}
.post figure{margin:0 0 20px}
.post figure img{width:100%;height:auto;display:block;border-radius:8px}
.post figcaption{font-size:13.5px;color:#6b7885;margin-top:6px}
.post .tbl{overflow-x:auto}
.post .cta{background:#16202a;color:#fff;border-radius:12px;padding:26px 20px;text-align:center;margin:40px 0 10px}
.post .cta b{display:block;font-size:20px;letter-spacing:-.7px}
.post .cta p{color:#b7c3cd;font-size:14.5px;margin:8px 0 0}
.post .cta a.home{display:inline-block;margin-top:14px;color:#FFB443;font-weight:700;text-decoration:underline;text-underline-offset:3px}
.post .rel{margin-top:34px;padding-top:22px;border-top:1px solid #e3e6e9}
.post .rel h2{font-size:18px;margin:0 0 10px}
.post .rel a{display:block;padding:10px 0;border-bottom:1px dashed #e3e6e9;color:#16202a;text-decoration:none;font-weight:700;font-size:15.5px}
.post .rel a span{display:block;font-weight:400;color:#6b7885;font-size:13.5px;margin-top:2px}
.plist{background:#fff}
.plist .wrap{max-width:720px}
.plist h1{font-size:28px;line-height:1.4;margin-bottom:8px}
.plist .intro{color:#5d6b78;font-size:15.5px;margin-bottom:24px}
.plist a.card{display:block;padding:18px 0;border-bottom:1px solid #e3e6e9;text-decoration:none;color:#16202a}
.plist a.card b{display:block;font-size:18px;letter-spacing:-.6px;line-height:1.45}
.plist a.card span{display:block;color:#5d6b78;font-size:14.5px;line-height:1.7;margin-top:6px}
.plist a.card small{display:block;color:#98a6b2;font-size:12.5px;margin-top:6px;font-family:'IBM Plex Mono'}
.icrumb{background:#1f2b36;color:#b7c3cd;font-size:13px}
.icrumb .wrap{display:flex;gap:8px;align-items:center;min-height:36px}
.icrumb a{color:#fff;font-weight:700;text-decoration:underline;text-decoration-color:#FFB443;text-underline-offset:3px}
@media(max-width:760px){.post h1{font-size:25px}.post h2{font-size:20px}.post p{font-size:16px}}
"""

# ───────────────────────────────────────────── 글 읽기
def read_post(path):
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n").lstrip("﻿")
    assert "\n---" in text, "%s: 머리와 본문을 나누는 --- 줄이 없다" % path
    head, rest = text.split("\n---", 1)
    rest = rest.lstrip("-").lstrip("\n")
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for k in ("제목", "슬러그", "설명", "날짜"):
        assert meta.get(k), "%s: '%s:' 줄이 없다" % (path, k)
    assert re.fullmatch(r"[a-z0-9-]+", meta["슬러그"]), "%s: 슬러그는 영문 소문자·숫자·- 만" % path
    body, captions = rest, {}
    m = re.search(r"^사진 ?캡션\s*:\s*$", rest, flags=re.M)
    if m:
        body = rest[:m.start()]
        for line in rest[m.end():].splitlines():
            mm = re.match(r"\s*(\d+)\s*[:.]\s*(.+)", line)
            if mm:
                captions[int(mm.group(1))] = mm.group(2).strip()
    meta["서비스"] = meta.get("서비스") or "우수관"
    assert meta["서비스"] in SERVICES, "%s: 서비스는 %s 중 하나" % (path, "/".join(SERVICES))
    meta["키워드목록"] = [t.strip() for t in re.split(r"[,，]", meta.get("키워드", "")) if t.strip()]
    meta["본문"] = body.strip("\n")
    meta["캡션"] = captions
    meta["파일"] = path
    return meta

def load_posts():
    posts = [read_post(p) for p in sorted(glob.glob(os.path.join(POSTS_DIR, "*.txt")))
             if not os.path.basename(p).startswith(("읽어", "_"))]
    slugs = [p["슬러그"] for p in posts]
    assert len(slugs) == len(set(slugs)), "슬러그가 겹친다: %s" % [s for s in slugs if slugs.count(s) > 1]
    posts.sort(key=lambda p: p["날짜"], reverse=True)
    return posts

# ───────────────────────────────────────────── 본문 → HTML
def _inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\((/[^\s)]*|https?://[^\s)]+)\)", r'<a href="\2">\1</a>', s)
    return s

def body_html(post, imgtag):
    """imgtag(src, alt) 는 build.py 의 imgtag (width/height 자동). 사진 없으면 자리 비움."""
    out, para, ul, ol, table = [], [], [], [], []
    slug = post["슬러그"]

    def flush_para():
        if para: out.append("<p>%s</p>" % _inline(" ".join(para))); para.clear()
    def flush_lists():
        if ul: out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % _inline(x) for x in ul)); ul.clear()
        if ol: out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % _inline(x) for x in ol)); ol.clear()
    def flush_table():
        if table:
            rows = [r for r in table if not re.match(r"^\s*\|?\s*:?-{2,}", r)]
            cells = [[_inline(c.strip()) for c in r.strip().strip("|").split("|")] for r in rows]
            thead = "<thead><tr>%s</tr></thead>" % "".join("<th>%s</th>" % c for c in cells[0])
            tbody = "<tbody>%s</tbody>" % "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in cells[1:])
            out.append('<div class="tbl"><table>%s%s</table></div>' % (thead, tbody)); table.clear()
    def flush_all():
        flush_para(); flush_lists(); flush_table()

    for raw in post["본문"].splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_all(); continue
        if line.lstrip().startswith("|"):
            flush_para(); flush_lists(); table.append(line); continue
        flush_table()
        m = re.match(r"^(#{2,3})\s+(.+)", line)
        if m:
            flush_all(); lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, _inline(m.group(2)), lv)); continue
        m = re.match(r"^\[사진\s*(\d+)\]\s*(.*)", line)
        if m:
            flush_all(); n = int(m.group(1))
            cap = post["캡션"].get(n, m.group(2).strip())
            src = "/%s/%s-%d.jpg" % (IMG_DIR.replace(os.sep, "/"), slug, n)
            if os.path.exists(os.path.join(IMG_DIR, "%s-%d.jpg" % (slug, n))):
                fc = "<figcaption>%s</figcaption>" % html.escape(cap) if cap else ""
                out.append("<figure>%s%s</figure>" % (imgtag(src, cap or post["제목"]), fc))
            continue
        m = re.match(r"^\[인용구\]\s*(.+)", line)
        if m:
            flush_all(); out.append("<blockquote>%s</blockquote>" % _inline(m.group(1))); continue
        m = re.match(r"^[-*•]\s+(.+)", line)
        if m:
            flush_para(); ol_flush = ol and flush_lists(); ul.append(m.group(1)); continue
        m = re.match(r"^\d+[.)]\s+(.+)", line)
        if m:
            flush_para(); ul_flush = ul and flush_lists(); ol.append(m.group(1)); continue
        flush_lists(); para.append(line.strip())
    flush_all()
    return "\n".join(out)

def first_image(post):
    for n in sorted(post["캡션"]) or [1]:
        p = os.path.join(IMG_DIR, "%s-%d.jpg" % (post["슬러그"], n))
        if os.path.exists(p):
            return "/" + p.replace(os.sep, "/")
    return None

def related(post, posts):
    """키워드 겹치는 수 → 최신순. 자기 자신 제외. posts 는 같은 서비스 글만 넘어온다."""
    def score(o):
        return len(set(o["키워드목록"]) & set(post["키워드목록"]))
    others = [o for o in posts if o["슬러그"] != post["슬러그"]]
    others.sort(key=lambda o: (score(o), o["날짜"]), reverse=True)
    return others[:RELATED_N]

# ───────────────────────────────────────────── 페이지
def url_of(post=None, svc="우수관"):
    d = SERVICES[post["서비스"] if post else svc]["dir"]
    return "/%s/%s.html" % (d, post["슬러그"]) if post else "/%s/" % d

def build(b):
    """b = build 모듈 (SITE, head, header, ctabtns, imgtag, footer 재료, write, DIST). 만든 URL 목록을 돌려준다."""
    posts_all = load_posts()
    urls = []
    for name, cfg in SERVICES.items():
        posts = [p for p in posts_all if p["서비스"] == name]
        if not posts:
            print("정보글(%s) 없음 → /%s/ 안 만듦" % (name, cfg["dir"])); continue
        urls += _build_service(b, name, cfg, posts)

    # 사진 복사 (서비스 공통 폴더 — 파일 이름이 슬러그라 겹치지 않는다)
    if os.path.isdir(IMG_DIR):
        import shutil
        dst = os.path.join(b.DIST, IMG_DIR)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(IMG_DIR, dst)
    return urls

def _build_service(b, name, cfg, posts):
    SITE = b.SITE
    urls = []
    home = cfg["home"]
    crumb_tpl = '<div class="icrumb"><div class="wrap"><a href="%s">%s</a><span>›</span><a href="%s">정보글</a>%s</div></div>\n'

    def shell(title, desc, canonical, jsonld, body, og_img=None, crumb_tail=""):
        h = b.head(title, desc, canonical, jsonld, False, og_img)
        h = h.replace("</style>", EXTRA_CSS + "</style>", 1)
        return (h + b.header(None) + crumb_tpl % (home, SITE["name"], url_of(svc=name), crumb_tail)
                + body + _footer(b, cfg))

    # 글 페이지
    for p in posts:
        canonical = SITE["domain"] + url_of(p)
        og = first_image(p)
        rel = related(p, posts)
        rel_html = ""
        if rel:
            rel_html = '<div class="rel"><h2>관련 글</h2>%s</div>' % "".join(
                '<a href="%s">%s<span>%s</span></a>' % (url_of(o), html.escape(o["제목"]), html.escape(o["설명"])) for o in rel)
        body = """<section class="post"><div class="wrap">
<h1>%s</h1>
<div class="meta">%s · %s</div>
%s
<div class="cta"><b>사진 4장 보내주시면 당일 견적 회신</b><p>%s</p>%s
<a class="home" href="%s">%s</a></div>
%s
</div></section>
""" % (html.escape(p["제목"]), p["날짜"], SITE["name"], body_html(p, b.imgtag), cfg["cta_sub"], b.ctabtns(),
       home, cfg["cta_link"] % SITE["name"], rel_html)
        ld = {
            "@context": "https://schema.org",
            "@graph": [
                {"@type": "Article", "headline": p["제목"], "description": p["설명"],
                 "datePublished": p["날짜"], "dateModified": p["날짜"], "inLanguage": "ko",
                 "mainEntityOfPage": canonical,
                 "author": {"@type": "Organization", "name": SITE["name"]},
                 "publisher": {"@type": "Organization", "name": SITE["name"], "url": SITE["domain"]},
                 **({"image": SITE["domain"] + og} if og else {})},
                {"@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": SITE["name"], "item": SITE["domain"] + home},
                    {"@type": "ListItem", "position": 2, "name": "정보글", "item": SITE["domain"] + url_of(svc=name)},
                    {"@type": "ListItem", "position": 3, "name": p["제목"], "item": canonical}]},
            ]}
        page = shell(p["제목"] + " | " + SITE["name"], p["설명"], canonical,
                     json.dumps(ld, ensure_ascii=False), body, og,
                     '<span>›</span><span>%s</span>' % html.escape(p["제목"][:22] + ("…" if len(p["제목"]) > 22 else "")))
        b.write(os.path.join(b.DIST, cfg["dir"], p["슬러그"] + ".html"), page)
        urls.append(url_of(p))

    # 목록 페이지
    cards = "".join('<a class="card" href="%s"><b>%s</b><span>%s</span><small>%s</small></a>'
                    % (url_of(p), html.escape(p["제목"]), html.escape(p["설명"]), p["날짜"]) for p in posts)
    title = "%s | %s" % (cfg["list_h1"], SITE["name"])
    desc = cfg["list_desc"]
    canonical = SITE["domain"] + url_of(svc=name)
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "url": canonical,
          "isPartOf": {"@type": "WebSite", "name": SITE["name"], "url": SITE["domain"]}}
    body = """<section class="plist"><div class="wrap">
<h1>%s</h1>
<p class="intro">현장에서 실제로 겪은 것만 씁니다. 글 %d편.</p>
%s
</div></section>
""" % (cfg["list_h1"], len(posts), cards)
    b.write(os.path.join(b.DIST, cfg["dir"], "index.html"), shell(title, desc, canonical, json.dumps(ld, ensure_ascii=False), body))
    urls.append(url_of(svc=name))
    print("정보글(%s) %d편 → /%s/" % (name, len(posts), cfg["dir"]))
    return urls

def _footer(b, cfg):
    SITE = b.SITE
    return """<footer>%s · %s<br><a class="fhome" href="%s">%s</a>
<span class="biz">상호 %s &middot; 대표 %s &middot; 사업자등록번호 %s<br>%s</span></footer>
<div class="fixed"><a class="f-call" href="tel:%s">📞 전화 걸기</a><a class="f-sms" href="sms:%s">💬 사진 문자</a></div>
%s%s</body></html>""" % (SITE["name"], SITE["phone"], cfg["home"], cfg["fhome"],
                         SITE["name"], SITE["biz_owner"], SITE["biz_no"], SITE["biz_addr"],
                         SITE["phone_raw"], SITE["phone_raw"], b.COPY_JS, b.NAVER_WCS)
