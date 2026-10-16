# -*- coding: utf-8 -*-
"""견적 문의 페이지 /contact.html (49째방, 2026-10-17) — 주인님 「모든건 팔도처럼」. 팔도의 문의 접수 페이지 자리.
   정적 사이트라 입력 양식은 두지 않는다 → 전화 · 사진 문자 · (카카오톡) + 종목별로 보낼 사진(svc["guide"] 그대로).
   ★ 없는 사실 금지 — 약속은 SITE["trust"](1년 무상 A/S · 당일 회신)와 출장 권역뿐. 무료 방문·당일 출장 같은 말 안 씀.
   ★ 지역 격리 — 지역 이름은 출장 권역 한 줄(첫 페이지와 같은 문구)만."""
import html, json

URL = "/contact.html"
FOOT = {"foot": "우수관 · 트렌치 · 보도블록 · 카스토퍼 · 에어컨 배관 · 렉산 캐노피 시공"}

STEPS = [
    ("사진 보내기", "문자나 카카오톡으로 사진과 주소(동네까지)를 보내 주세요. 아래 종목별 사진 4장이면 충분합니다."),
    ("당일 회신", "사진을 보고 공사 방법과 대략적인 금액을 그날 안에 알려 드립니다."),
    ("날짜 잡기", "금액이 맞으시면 공사 날짜를 정합니다."),
    ("공사 · A/S", "공사 뒤에는 시공일로부터 1년 동안 무상으로 A/S 해 드립니다."),
]
MORE = [
    ("주소", "동네까지만 알려 주셔도 됩니다. 이동 거리와 장비를 미리 정합니다."),
    ("높이 · 층수", "몇 층 높이인지, 사다리차나 스카이가 들어갈 자리가 있는지."),
    ("길이 · 개수", "대략 몇 미터인지, 몇 군데인지. 모르시면 사진으로 보고 판단합니다."),
    ("원하시는 날짜", "급한 일정이 있으면 같이 적어 주세요."),
]


def page(b):
    S = b.SITE
    title = "견적 문의 · 사진 보내는 법 | %s" % S["name"]
    desc = ("우수관·트렌치·보도블록·카스토퍼·에어컨 배관·렉산 캐노피 견적 문의. 종목별로 보내 주실 사진 4장과 진행 순서. "
            "사진 보내주시면 당일 회신. %s" % S["phone"])
    canonical = S["domain"] + URL
    ld = json.dumps({"@context": "https://schema.org", "@type": "ContactPage", "name": title, "url": canonical,
                     "description": desc, "inLanguage": "ko",
                     "mainEntity": {"@type": "Organization", "name": S["name"], "url": S["domain"] + "/",
                                    "telephone": S["phone"]}}, ensure_ascii=False)
    steps = "".join('<div class="cell"><div class="t"><b>%d. %s</b><span>%s</span></div></div>'
                    % (i, html.escape(t), html.escape(d)) for i, (t, d) in enumerate(STEPS, 1))
    more = "".join('<div class="cell"><div class="t"><b>%s</b><span>%s</span></div></div>'
                   % (html.escape(t), html.escape(d)) for t, d in MORE)
    guides = ""
    for svc in b.SERVICES:
        if svc.get("parent") or not svc.get("guide"):
            continue
        cells = "".join('<div class="cell"><div class="t"><b>%s</b><span>%s</span></div></div>'
                        % (t, d) for t, d in svc["guide"])
        guides += ('<div class="big-t"><h3 style="margin:30px 0 4px"><a href="%s" style="color:#fff;text-decoration:none">%s &rsaquo;</a></h3></div>'
                   '<div class="qg">%s</div>\n'
                   % (b.url_of(svc), html.escape(svc["label"]), cells))
    body = """<section class="hero"><div class="wrap">
<h1>견적 문의</h1>
<p class="sub">사진 몇 장 보내주시면 그날 안에 공사 방법과 대략적인 금액을 알려 드립니다.</p>
%s
%s
</div></section>
<section class="q"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>이렇게 진행합니다</h2></div>
  <div class="qg">%s</div>
</div></section>
<section class="q"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>종목별로 보내 주실 사진</h2>
  <p>사진 없이는 정확한 금액을 드릴 수 없습니다. 아래 4장이면 대부분 판단됩니다.</p></div>
  %s
</div></section>
<section class="q"><div class="wrap">
  <div class="big-t"><div class="hr"></div><h2>같이 적어 주시면 빨라집니다</h2></div>
  <div class="qg">%s</div>
  <div class="qcta">
    <span class="n">%s</span>
    %s
    <button class="copy" type="button" data-num="%s">번호 복사<span>PC 에서 쓰는 버튼</span></button>
  </div>
  <div class="links" style="margin-top:18px"><a href="/area/">출장 지역 — 사는 곳별 안내<i>&rsaquo;</i></a></div>
</div></section>
""" % (b.trust(), b.ctabtns(), steps, guides, more, S["phone"], b.ctabtns(), S["phone"])
    return (b.head(title, desc, canonical, ld, False, None) + b.header(None) + body + b.footer(FOOT))
