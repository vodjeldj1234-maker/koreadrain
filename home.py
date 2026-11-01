# -*- coding: utf-8 -*-
"""메인 / — 회사 소개 (51째방, 2026-11-01)

주인님: 「메인홈페이지는 메인이여야되고 우수관은 우수관카테고리여야지 … 내 업체를 검색했으면 메인카테고리로 들어가서
주로 어떤공사를하고있으며 다양한보수공사를 진행하고있다 뭐 이런식으로」 → 시안 2(명함처럼 흰 바탕 + 「FO 포스원」 로고) 고르심.
  - 맨 위: 명함 문구 그대로(시설물 유지보수 및 전문시공 · 세 줄) + 우리 사례 사진 한 장. 명함의 전화번호는 홈페이지 번호와 달라 쓰지 않는다.
  - 주로 하는 공사 6종목(사진 카드 → 종목 첫 페이지) · 이런 보수도 합니다(이미 공개된 정보글로만 잇는다) · 최근 사례 4 · 진행 순서.
  - 지역 격리: 이 페이지에 지역 이름은 출장 범위(서울·인천·경기·충청)뿐. 없는 약속·숫자는 쓰지 않는다.
"""
import os, html, json

URL = "/"
HERO_CASE = ("six-storey-stainless-pipes-double-wall", 8, "6층 건물 외벽에 새로 낸 스테인리스 우수관")

# (종목 key, 카드 제목, 한 줄, 사진)
SVC = [
    ("usugwan", "우수관 · 홈통 · 빗물받이", "외벽 우수관 누수 · 교체 · 신설, 처마 빗물받이", "/img/case/brick-house-gutter-square-downpipes-11.jpg"),
    ("trench", "트렌치 · 그레이팅", "무소음 덮개, 녹슨 앵글 교체, 측구 · 배수로 보수", "/img/hero-musoeum.jpg"),
    ("block", "보도블록 · 점자블록", "꺼진 블록 재시공, 점자블록 · 경계석 교체", "/img/hero-block.jpg"),
    ("carstop", "카스토퍼 · 과속방지턱", "주차장 카스토퍼, 방지턱, 주차선 도색", "/img/hero-carstop.jpg"),
    ("aircon", "에어컨 배관", "삭은 보온재 · 테이프 교체", "/img/hero-aircon.jpg"),
    ("lexan", "렉산 · 캐노피", "캐노피 설치, 렉산 지붕 교체, 파고라 철거", "/img/hero-lexan.jpg"),
]
# 이런 보수도 합니다 — (줄 이름, [(글자, 정보글 주소)]) · 공개된 글만 (빌드 때 dist 에 없으면 글자만 남긴다)
MORE = [
    ("우수관", [("매립 우수관 누수", "/info/maerip-usugwan-nusu.html"), ("물홈통만 교체", "/info/mulhomtong-gyoche.html"),
             ("선홈통 꺾임", "/info/seonhomtong-kkeokim-45do.html"), ("옥상 배수구 추가", "/info/oksang-baesu-bujok.html"),
             ("처마 물받이 교체", "/info/cheoma-mulbaji-gyoche.html"), ("한 구간만 수리", "/info/usugwan-bubun-suri.html")]),
    ("트렌치", [("덜컹거리는 덮개", "/trench/info/musoeum-deopgae-sori.html"), ("주방 · 실내 트렌치", "/trench/info/jubang-silnae-trench.html"),
             ("세차장 바닥", "/trench/info/sechajang-badak-trench.html"), ("공장 배수로", "/trench/info/gongjang-baesuro-sinseol.html"),
             ("측구 보수", "/trench/info/cheukgu-bosu.html")]),
    ("보도블록", [("내려앉는 블록", "/block/info/bodo-block-naeryeoanjeum.html"), ("가로수 옆 들뜬 블록", "/block/info/garosu-ppuri-bodo-block.html"),
              ("경계석 교체", "/block/info/gyeonggyeseok-gyoche.html"), ("점자블록 설치 · 교체", "/block/info/jeomja-block-seolchi-gyoche.html")]),
    ("주차장", [("카스토퍼 설치", "/carstop/info/carstop-seolchi-junbi.html"), ("과속방지턱 · 반사경", "/carstop/info/gwasok-bangjiteok-bansagyeong.html"),
             ("주차선 도색", "/carstop/info/juchaseon-gyugyeok-dosaek.html")]),
    ("에어컨", [("배관 테이프", "/aircon/info/aircon-baegwan-tape.html"), ("보온재 교체", "/aircon/info/aircon-bonjae-gyoche.html")]),
    ("렉산", [("깨진 칸만 교체", "/lexan/info/lexan-bubun-jeonche-gyoche.html"), ("아치 캐노피 렉산", "/lexan/info/arch-canopy-lexan-gyoche.html"),
            ("캐노피 설치", "/lexan/info/canopy-seolchi-sunseo.html"), ("캐노피 · 파고라 철거", "/lexan/info/canopy-pergola-cheolgeo.html")]),
]

CSS = """
.hm{background:#f7f5f1;border-bottom:1px solid #e7e1d7}
.hm .wrap{max-width:1040px;display:grid;grid-template-columns:1.05fr 1fr;gap:40px;align-items:center;padding-top:44px;padding-bottom:44px}
.hm .mk{display:block;height:120px;width:auto}
.hm h1{font-size:46px;font-weight:900;letter-spacing:-1.8px;color:#1d3557;line-height:1.15;margin-top:14px}
.hm .sl{font-size:20px;font-weight:700;color:#1d3557;margin-top:6px}
.hm ul{list-style:none;margin-top:18px;font-size:17px;color:#2d3a46}
.hm li{padding-left:16px;position:relative;line-height:1.9}
.hm li::before{content:"";position:absolute;left:2px;top:.85em;width:6px;height:6px;border-radius:50%;background:#6b7a88}
.hm .tel{display:inline-block;margin-top:20px;font-family:'IBM Plex Mono';font-size:26px;font-weight:600;color:#16202a;text-decoration:none}
.hm .pic img{width:100%;height:auto;aspect-ratio:4/3.4;object-fit:cover;border-radius:6px;display:block}
.hm-trust{background:#f4f1ec;border-bottom:1px solid #e7e1d7}
.hm-trust .wrap{max-width:1040px;display:grid;grid-template-columns:repeat(3,1fr)}
.hm-trust div{padding:18px 14px;border-left:1px solid #e2dbcf}.hm-trust div:first-child{border-left:0}
.hm-trust b{display:block;font-size:16px}.hm-trust span{font-size:13.5px;color:#5d6b78}
.hs{padding:56px 0}.hs .wrap{max-width:1040px}
.hs .ey{font-size:13px;font-weight:700;color:#E0521A;letter-spacing:.5px}
.hs h2{font-size:28px;letter-spacing:-1px;margin-top:4px}
.hs .ld{color:#5d6b78;margin-top:6px;font-size:15.5px}
.hsv{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:24px}
.hsv a{display:block;text-decoration:none;color:inherit;border:1px solid #e4e0d8;border-radius:10px;overflow:hidden;background:#fff}
.hsv a img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block}
.hsv a div{padding:14px 16px 16px}
.hsv b{font-size:17.5px;font-weight:900;letter-spacing:-.5px}.hsv p{font-size:14px;color:#5d6b78;margin-top:2px;line-height:1.6}
.hsv i{font-style:normal;font-size:13.5px;font-weight:700;color:#E0521A;display:inline-block;margin-top:8px}
.hs.dk{background:#16202a;color:#fff}.hs.dk .ld{color:#b7c3cd}
.hmore{margin-top:22px;border-top:1px solid #2f3e4c}
.hmore div{display:grid;grid-template-columns:120px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #2f3e4c}
.hmore b{color:#FFB443}.hmore p{color:#dbe3ea;font-size:15px}
.hmore a{color:#dbe3ea;text-decoration:underline;text-decoration-color:#4a5d6e;text-underline-offset:3px}
.hcs{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:24px}
.hcs a{text-decoration:none;color:inherit}.hcs img{width:100%;height:auto;aspect-ratio:1;object-fit:cover;border-radius:8px;display:block}
.hcs em{font-style:normal;font-size:12.5px;font-weight:700;color:#E0521A;display:block;margin-top:8px}.hcs span{font-size:14.5px;font-weight:700;line-height:1.5}
.hs.gy{background:#f4f1ec}
.hst{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:24px;counter-reset:s}
.hst div{border-top:3px solid #16202a;padding-top:10px}.hst b{display:block;font-size:15.5px}.hst span{font-size:13.5px;color:#5d6b78}
.hst div::before{counter-increment:s;content:"0" counter(s);font-family:'IBM Plex Mono';font-size:13px;color:#E0521A;font-weight:600}
@media(max-width:760px){
 .hm .wrap{grid-template-columns:1fr;gap:22px;padding-top:28px;padding-bottom:28px}.hm .mk{height:84px}.hm h1{font-size:32px}.hm .sl{font-size:16.5px}.hm ul{font-size:15px}.hm .tel{font-size:21px}
 .hm-trust .wrap{grid-template-columns:1fr}.hm-trust div{border-left:0;border-top:1px solid #e2dbcf;padding:12px 4px}.hm-trust div:first-child{border-top:0}
 .hs{padding:40px 0}.hs h2{font-size:23px}.hsv{grid-template-columns:1fr 1fr;gap:10px}.hsv a div{padding:10px 11px 12px}.hsv b{font-size:15px}.hsv p{font-size:12.5px}
 .hmore div{grid-template-columns:1fr;gap:2px}.hcs{grid-template-columns:1fr 1fr}.hst{grid-template-columns:1fr 1fr}}
"""


def _latest(lst):
    return sorted(lst, key=lambda c: c.get("date", ""), reverse=True)[0]


def _cover(b, c):
    """사례의 마지막 사진(완료 컷)."""
    import glob
    last = sorted(glob.glob(os.path.join(b.IMG, "case", "%s-[0-9][0-9].jpg" % c["slug"])))[-1]
    return "/img/case/" + os.path.basename(last)


def build(b):
    import data, cases33, lexan_gen
    S = b.SITE
    svcs = {s["key"]: s for s in b.SERVICES}
    E = html.escape

    hero_src = "/img/case/%s-%02d.jpg" % HERO_CASE[:2]
    hero = """<div class="hm"><div class="wrap"><div>
<img class="mk" src="/img/logo-fo.png" alt="포스원 로고" width="161" height="120" fetchpriority="high">
<h1>%s</h1><div class="sl">시설물 유지보수 및 전문시공</div>
<ul><li>외벽 우수관 및 배수설비 공사</li><li>바닥 트렌치 및 기초공사</li><li>건물 외장 및 특수 종합 공사</li></ul>
<a class="tel" href="tel:%s">%s</a></div>
<div class="pic">%s</div>
</div></div>
<div class="hm-trust"><div class="wrap"><div><b>사진 보내주시면 당일 회신</b><span>전체 한 장, 망가진 곳 가까이 한 장</span></div>
<div><b>시공일로부터 1년 무상 A/S</b><span>공사한 자리는 저희가 다시 봅니다</span></div>
<div><b>서울 · 인천 · 경기 전역, 충청 전 시군</b><span>출장 시공</span></div></div></div>
""" % (E(S["name"]), S["phone_raw"], S["phone"], b.imgtag(hero_src, HERO_CASE[2], cls="hp", lazy=False))

    cards = "".join('<a href="%s">%s<div><b>%s</b><p>%s</p><i>자세히 보기 &rarr;</i></div></a>'
                    % (b.url_of(svcs[k]), b.imgtag(img, t, cls="hc"), E(t), E(line), ) for k, t, line, img in SVC)
    sec_svc = """<section class="hs"><div class="wrap"><div class="ey">주로 하는 공사</div><h2>건물 밖 물길과 바닥, 지붕까지</h2>
<p class="ld">사진을 누르면 종목별 시공 방법과 사례를 보실 수 있습니다.</p><div class="hsv">%s</div></div></section>
""" % cards

    def item(t, u):
        f = os.path.join(b.DIST, *u.strip("/").split("/"))
        return '<a href="%s">%s</a>' % (u, E(t)) if os.path.exists(f) else E(t)
    rows = "".join("<div><b>%s</b><p>%s</p></div>" % (E(n), " &middot; ".join(item(t, u) for t, u in its)) for n, its in MORE)
    sec_more = """<section class="hs dk"><div class="wrap"><div class="ey">이런 보수도 합니다</div><h2>한 군데만 고치는 일도 합니다</h2>
<p class="ld">한 줄만 샌다, 덮개 하나만 덜컹거린다, 블록 몇 장만 꺼졌다 — 그 자리만 고칩니다.</p><div class="hmore">%s</div></div></section>
""" % rows

    picks = [("우수관", "usugwan", _latest(data.USUGWAN_CASES)), ("트렌치", "trench", _latest(data.TRENCH_CASES)),
             ("보도블록", "block", _latest(cases33.BLOCK_CASES)), ("렉산 · 캐노피", "lexan", _latest(lexan_gen.CASES))]
    import cases as C
    cs = ""
    for lab, k, c in picks:
        cfg = svcs[k].get("case_cfg") or next(s["case_cfg"] for s in b.SERVICES if s.get("case_cfg") and s["case_cfg"]["dir"].startswith(k))
        cs += '<a href="%s">%s<em>%s</em><span>%s</span></a>' % (C.url(cfg, c), b.imgtag(_cover(b, c), c["title"], cls="hq"), E(lab), E(c["title"]))
    sec_cases = """<section class="hs"><div class="wrap"><div class="ey">최근 시공 사례</div><h2>다녀온 현장</h2><div class="hcs">%s</div></div></section>
""" % cs

    sec_steps = """<section class="hs gy"><div class="wrap"><div class="ey">진행 순서</div><h2>사진 한 장이면 시작합니다</h2>
<div class="hst"><div><b>사진 문자</b><span>전체 · 가까이</span></div><div><b>당일 회신</b><span>공사 범위와 견적</span></div>
<div><b>날짜 상의</b><span>통행 · 영업 시간 맞춰</span></div><div><b>시공</b><span>정한 날에</span></div><div><b>1년 A/S</b><span>시공일로부터</span></div></div></div></section>
"""

    title = "%s | 우수관·트렌치·보도블록·카스토퍼·에어컨 배관·렉산 캐노피 시공" % S["name"]
    desc = ("시설물 유지보수 및 전문시공 %s. 외벽 우수관·빗물받이, 바닥 트렌치, 보도블록·점자블록, 카스토퍼·방지턱, "
            "에어컨 배관, 렉산 캐노피를 시공합니다. 사진 보내주시면 당일 회신." % S["name"])
    canonical = S["domain"] + URL
    area = [{"@type": "City", "name": c} for r in b.REGIONS for c in r["cities"]]
    ld = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": S["name"],
          "telephone": "+82-" + S["phone"][1:], "url": canonical, "logo": S["domain"] + "/img/logo-fo.png",
          "image": [S["domain"] + hero_src], "areaServed": area,
          "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t}} for _, t, _, _ in SVC]}
    page = b.head(title, desc, canonical, json.dumps(ld, ensure_ascii=False), True, hero_src).replace("</style>", CSS + "</style>", 1)
    foot_svc = {"foot": "외벽 우수관 · 바닥 트렌치 · 보도블록 · 카스토퍼 · 에어컨 배관 · 렉산 캐노피 시공"}
    page += b.header(None, is_home=True) + hero + sec_svc + sec_more + sec_cases + sec_steps + b.footer(foot_svc)
    b.write(os.path.join(b.DIST, "index.html"), page)
    return [URL]
