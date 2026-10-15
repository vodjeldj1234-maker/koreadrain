# -*- coding: utf-8 -*-
"""도시별 페이지 (48째방, 2026-10-15) — 주인님 「아파트 원칙 삭제하고 팔도처럼 개조해」 · 「1. 이어 · 3. 권역은 전체」.

   우수관 · 트렌치 · 보도블록(점자블록) 세 종목을 도시 하나에 한 장씩 만든다 (98곳 — 서울·인천은 구, 그 밖은 시·군).
   제목은 「수원 트렌치 시공·교체 업체 | 포스원종합공사」 꼴.

   ★ 지역 격리는 지킨다 — 도시 페이지에는 그 도시 이름과 그 도시의 구·동만 보인다. 다른 도시로 가는 링크도 없다.
     권역 페이지(예: 수원·오산)는 자기 권역 도시 목록만, 종목 첫 페이지는 전체 도시 목록을 단다.
   ★ 서비스 격리는 푼다 — 같은 도시의 다른 종목 페이지, 종목 첫 페이지끼리 잇는다(헤더 메뉴도).
   ★ 사진은 종목 공통 사진이다 → alt·캡션에 도시 이름을 넣지 않는다(그 도시에서 찍은 사진이 아니다).
   ★ 행정구역·행정동은 city_data.json (행정안전부 주민등록 인구통계 읍면동 현황 2026-09 · 위키백과 — 항목마다 src).
   slug 는 한 번 정하면 바꾸지 않는다(주소가 된다)."""
import os, io, json, html, zlib

_HERE = os.path.dirname(os.path.abspath(__file__))
_RAW = json.load(io.open(os.path.join(_HERE, "city_data.json"), encoding="utf-8"))
GROUPS = ["서울", "인천", "경기", "대전·세종", "충남", "충북"]

# 시·군 붙이기 — 본문에 쓰는 공식 이름 (예: 경기 수원시)
_GUN = {"가평", "양평", "연천", "금산", "부여", "서천", "청양", "홍성", "예산", "태안",
        "보은", "옥천", "영동", "증평", "진천", "괴산", "음성", "단양", "강화", "옹진"}
_SPECIAL = {"bundang": "경기 성남시 분당구", "ilsan": "경기 고양시 일산", "dongtan": "경기 화성시 동탄",
            "gyeonggi-gwangju": "경기 광주시", "daejeon": "대전광역시", "sejong": "세종특별자치시"}
_PRE = {"경기": "경기 ", "충남": "충남 ", "충북": "충북 ", "인천": "인천 ", "서울": "서울 "}


def _official(c):
    if c["slug"] in _SPECIAL:
        return _SPECIAL[c["slug"]]
    n = c["name"]
    if c["group"] in ("서울", "인천") and n.endswith("구"):
        return _PRE[c["group"]] + n
    return _PRE.get(c["group"], "") + n + ("군" if n in _GUN else "시")


CITIES = []
for i, c in enumerate(_RAW):
    CITIES.append(dict(slug=c["slug"], short=c["name"], name=c["full"], official=_official(c),
                       group=c["group"], gu=c["gu"], src=c.get("src", ""), idx=i))
C = {c["slug"]: c for c in CITIES}
assert len(CITIES) == 98, len(CITIES)

# ───────────────────────── 종목별 문구 (도시 페이지에만 쓴다)
#   ⚠ 없는 사실 금지 — 종목 첫 페이지·FAQ 에 이미 있는 말만 줄여 쓴다. 「당일 출장」 금지, 「사진 보내주시면 당일 견적 회신」은 된다.
SVC = {
    "usugwan": dict(short="우수관", menu="우수관 · 홈통",
                    title="{name} 우수관 교체·시공 업체 | {site}",
                    desc="{official} 우수관 교체·시공 업체. 새는 우수관·선홈통 교체, 벽 속 매립 우수관은 막고 외벽으로 새로 냅니다. "
                         "{official} 전 지역 출장. 사진 보내주시면 당일 견적 회신. {phone}",
                    link="{short} 우수관 교체"),
    "trench": dict(short="트렌치", menu="트렌치 · 배수로",
                   title="{name} 트렌치 시공·교체 업체 | {site}",
                   desc="{official} 트렌치 시공·교체 업체. 내려앉은 그레이팅·부식된 앵글 교체, 무소음 덮개, 배수로 신설. "
                        "{official} 전 지역 출장. 사진 보내주시면 당일 견적 회신. {phone}",
                   link="{short} 트렌치 시공"),
    "block": dict(short="보도블록", menu="보도블록 · 점자블록",
                  title="{name} 보도블록·점자블록 시공 업체 | {site}",
                  desc="{official} 보도블록·점자블록·경계석 시공 업체. 내려앉은 보도블록 재시공, 깨진 점자블록·경계석 교체. "
                       "{official} 전 지역 출장. 사진 보내주시면 당일 견적 회신. {phone}",
                  link="{short} 보도블록 · 점자블록"),
}
KEYS = list(SVC)
# 헤더 메뉴 — 종목 첫 페이지끼리 잇는다 (서비스 격리 해제)
MENU = [("usugwan", "우수관"), ("trench", "트렌치"), ("block", "보도블록·점자블록"),
        ("carstop", "카스토퍼·방지턱"), ("aircon", "에어컨 배관"), ("lexan", "렉산·캐노피")]


def _jong(s):
    """마지막 글자에 받침이 있나 (은/는 · 이/가)"""
    ch = s.strip()[-1]
    return "가" <= ch <= "힣" and (ord(ch) - 0xAC00) % 28 != 0


def _eun(s):
    return s + ("은" if _jong(s) else "는")


# ───────────────────────── 도시 ↔ 권역 (종목마다 권역 목록이 다르다)
_BYNAME = {}
for c in CITIES:
    _BYNAME.setdefault(c["short"], []).append(c["slug"])
_EXTRA_IN = {"성남": ["bundang"], "고양": ["ilsan"], "화성": ["dongtan"]}   # 시 안의 동네 이름 페이지


def cities_of_region(region):
    """권역(region dict)의 cities 이름 → 도시 slug 목록"""
    out = []
    for nm in region["cities"]:
        if nm == "서울특별시":
            out += [c["slug"] for c in CITIES if c["group"] == "서울"]; continue
        if nm == "인천광역시":
            out += [c["slug"] for c in CITIES if c["group"] == "인천"]; continue
        if nm == "세종특별자치시":
            out.append("sejong"); continue
        if nm == "대전광역시":
            out.append("daejeon"); continue
        if nm == "광주시":
            out.append("gyeonggi-gwangju"); continue
        stem = nm[:-1] if nm[-1] in "시군" and len(nm) > 2 else nm
        for s in _BYNAME.get(stem, []):
            if C[s]["group"] not in ("서울", "인천") and s != "gyeonggi-gwangju":
                out.append(s)
        out += _EXTRA_IN.get(stem, [])
    seen = []
    for s in out:
        if s not in seen:
            seen.append(s)
    return seen


def _regs(svc, REGIONS):
    return svc.get("region_list") or (REGIONS if svc.get("regions", True) else [])


_PAGES = {}


def pages(svc, REGIONS, SITE):
    """이 종목의 도시 페이지(region 꼴 dict) 목록. 권역 slug 와 겹치면: 권역이 그 도시 하나뿐 → 권역 페이지를 쓴다(새로 안 만듦),
       아니면 slug 뒤에 -si."""
    key = svc["key"]
    if key not in SVC:
        return []
    if key in _PAGES:
        return _PAGES[key]
    regs = _regs(svc, REGIONS)
    rslug = {r["slug"]: r for r in regs}
    out = []
    for c in CITIES:
        slug = c["slug"]
        if slug in rslug:
            r = rslug[slug]
            if cities_of_region(r) == [slug]:
                continue                          # 권역 페이지가 곧 도시 페이지 (대전)
            slug += "-si"
        out.append(_page_dict(svc, c, slug, SITE))
    _PAGES[key] = out
    return out


def url_for(svc, c, REGIONS, SITE):
    """도시 c 의 이 종목 주소 — 도시 페이지가 없으면(대전) 권역 페이지 주소."""
    for p in pages(svc, REGIONS, SITE):
        if p["city"]["slug"] == c["slug"]:
            return "/%s/%s.html" % (svc.get("rdir", svc["dir"]), p["slug"])
    for r in _regs(svc, REGIONS):
        if cities_of_region(r) == [c["slug"]]:
            return "/%s/%s.html" % (svc.get("rdir", svc["dir"]), r["slug"])
    return None


def _dongs(c):
    out = []
    for g, ds in c["gu"]:
        out += ds
    return out


def _page_dict(svc, c, slug, SITE):
    s = SVC[svc["key"]]
    fmt = dict(name=c["name"], short=c["short"], official=c["official"], site=SITE["name"], phone=SITE["phone"])
    groups = []
    for g, ds in c["gu"]:
        label = g or c["official"]
        groups.append((html.escape(label), html.escape(" · ".join(ds))))
    ds = _dongs(c)
    # 행정동 몇 개를 고르는 자리는 종목마다 다르게 (같은 도시 세 페이지가 같은 동을 앞세우지 않게)
    k = KEYS.index(svc["key"])
    pick = [ds[(k * 3 + j * 5) % len(ds)] for j in range(3)] if ds else []
    pick = list(dict.fromkeys(pick))
    gu_names = [g for g, _ in c["gu"] if g]
    unit = "읍·면·동" if any(d.endswith(("읍", "면")) for d in ds) else "동"
    if gu_names:
        lead = "%s %s로 나뉩니다. %s %d곳 모두 출장 범위입니다." % (
            _eun(c["official"]), " · ".join(gu_names), unit, len(ds))
    else:
        lead = "%s %s %d곳 모두 출장 범위입니다." % (c["official"], unit, len(ds))
    area = dict(h2="%s <em>어디든</em> 갑니다" % html.escape(c["short"]),
                sub=html.escape(lead + " 사진 보내주시면 당일 견적 회신드립니다."),
                groups=groups,
                tail=html.escape("목록에 없는 동네라도 %s 안이면 똑같이 갑니다." % c["official"]))
    faq_r = []
    if pick:
        faq_r.append(("%s인데 와 주시나요?" % pick[0],
                      "갑니다. %s 안이면 동네를 가리지 않습니다. 현장 사진과 주소를 문자로 보내주시면 당일 견적 회신드립니다." % c["official"]))
    return dict(kind="city", slug=slug, name=c["name"], cities=[c["official"]], city=c,
                title=s["title"].format(**fmt), desc=s["desc"].format(**fmt),
                area=area, faq_r=faq_r, idx=c["idx"],
                gal_p="%s 현장 사진은 시공하는 대로 올립니다. 아래는 같은 공사를 한 다른 현장 사진입니다." % c["short"])


# ───────────────────────── 화면 조각
def _a(href, text):
    return '<a href="%s">%s<i>&rsaquo;</i></a>' % (href, html.escape(text))


def menu(b, current=None):
    """헤더 아래 종목 메뉴 (서비스 격리 해제 — 48째방)."""
    rows = []
    for key, label in MENU:
        svc = next((s for s in b.SERVICES if s["key"] == key), None)
        if not svc:
            continue
        cls = ' class="on"' if current and (current["key"] == key or (current.get("parent") or {}).get("key") == key) else ""
        rows.append('<a%s href="%s">%s</a>' % (cls, b.url_of(svc), html.escape(label)))
    return '<nav class="smenu"><div class="wrap">%s</div></nav>\n' % "".join(rows)


def city_nav(b, svc, page):
    """도시 페이지 아래 — 같은 도시의 다른 종목 + 다른 종목 첫 페이지 + 이 종목 첫 페이지. 다른 도시로는 안 잇는다(지역 격리)."""
    c = page["city"]
    rows = []
    for key in KEYS:
        if key == svc["key"]:
            continue
        o = next(s for s in b.SERVICES if s["key"] == key)
        u = url_for(o, c, b.REGIONS, b.SITE)
        if u:
            rows.append(_a(u, SVC[key]["link"].format(short=c["short"])))
    for key, label in MENU:
        if key in KEYS:
            continue
        o = next((s for s in b.SERVICES if s["key"] == key), None)
        if o:
            rows.append(_a(b.url_of(o), label))
    rows.append(_a(b.url_of(svc), "%s 시공 안내 전체 보기" % SVC[svc["key"]]["short"]))
    return ('<section class="nav"><div class="wrap">\n'
            '  <h2>%s에서 하는 다른 공사</h2><p>같은 업체가 직접 와서 합니다.</p>\n'
            '  <div class="links">%s</div>\n'
            '</div></section>\n' % (html.escape(c["short"]), "".join(rows)))


def hub_links(b, svc, region):
    """권역 페이지 — 이 권역 도시 페이지 목록 (자기 권역 이름만 나온다)."""
    if svc["key"] not in SVC:
        return ""
    rows = []
    for s in cities_of_region(region):
        u = url_for(svc, C[s], b.REGIONS, b.SITE)
        if u and not u.endswith("/%s.html" % region["slug"]):
            rows.append(_a(u, SVC[svc["key"]]["link"].format(short=C[s]["short"])))
    if not rows:
        return ""
    return ('<section class="nav"><div class="wrap">\n'
            '  <h2>%s 도시별 안내</h2><p>시·구마다 따로 정리했습니다.</p>\n'
            '  <div class="links">%s</div>\n'
            '</div></section>\n' % (html.escape(region["name"]), "".join(rows)))


def directory(b, svc):
    """종목 첫 페이지 — 출장 도시 전체 목록 (시·도별)."""
    if svc["key"] not in SVC or svc.get("parent"):
        return ""
    blocks = []
    for g in GROUPS:
        rows = []
        for c in CITIES:
            if c["group"] != g:
                continue
            u = url_for(svc, c, b.REGIONS, b.SITE)
            if u:
                rows.append('<a href="%s">%s</a>' % (u, html.escape(c["short"])))
        if rows:
            blocks.append('<div class="cg"><b>%s</b><div>%s</div></div>' % (g, "".join(rows)))
    return ('<section class="cdir"><div class="wrap">\n'
            '  <div class="big-t"><div class="hr"></div><h2>%s <em>도시별</em> 안내</h2>\n'
            '  <p>사는 곳을 누르면 그 도시 안내로 갑니다. 목록에 없는 곳도 연락 주시면 갑니다.</p></div>\n'
            '  %s\n'
            '</div></section>\n' % (html.escape(SVC[svc["key"]]["short"]), "".join(blocks)))
