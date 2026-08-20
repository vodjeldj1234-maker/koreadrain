# -*- coding: utf-8 -*-
"""전체 CSS — 디자인 수정은 이 파일만 고치면 전 페이지에 반영된다"""

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans KR',sans-serif;background:#fff;color:#16202a;padding-bottom:80px;line-height:1.75;word-break:keep-all;-webkit-font-smoothing:antialiased}
.wrap{max-width:900px;margin:0 auto;padding:0 16px}
h1,h2,h3{font-family:'Noto Sans KR',sans-serif;font-weight:900;letter-spacing:-1.2px}
.ph{position:relative;background:repeating-linear-gradient(45deg,#c9c3b6,#c9c3b6 14px,#d5d0c4 14px,#d5d0c4 28px);display:flex;align-items:center;justify-content:center;color:#5c5749;font-size:13px;font-weight:700;overflow:hidden}
img.ph{object-fit:cover;width:100%;height:auto;display:block}
.gal .item{align-self:start}
.ph::after{content:attr(data-f);position:absolute;bottom:8px;left:8px;font-family:'IBM Plex Mono';font-size:10px;color:#7a7466;background:rgba(255,255,255,.6);padding:2px 6px;border-radius:3px}
header{background:#16202a;color:#fff}
header .wrap{display:flex;align-items:center;justify-content:space-between;height:56px}
.logo{font-weight:900;font-size:18px;letter-spacing:-.8px}
.hcall{color:#FFB443;font-family:'IBM Plex Mono';font-size:16px;text-decoration:none}
/* 히어로: 큰 사진 + 큰 카피 */
.hero{position:relative}
.hero .ph{aspect-ratio:16/11}
.hero .cap{background:#16202a;color:#fff;padding:34px 0 30px;text-align:center}
.hero h1{font-size:38px;line-height:1.4}
.hero h1 em{font-style:normal;color:#FFB443}
.hero p{color:#b7c3cd;margin-top:12px;font-size:16px}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#2c3a47;margin-top:22px}
.tri div{background:#16202a;padding:14px 6px;text-align:center}
.tri b{display:block;color:#FFB443;font-family:'IBM Plex Mono';font-size:15px}
.tri span{font-size:12.5px;color:#98a6b2}
section{padding:52px 0}
.big-t{text-align:center;margin-bottom:28px}
.big-t h2{font-size:32px;line-height:1.45}
.big-t h2 em{font-style:normal;color:#E0521A}
.big-t p{color:#5d6b78;margin-top:12px;font-size:16px;line-height:1.8;max-width:560px;margin-left:auto;margin-right:auto}
.hr{width:46px;height:4px;background:#E0521A;margin:0 auto 18px}
/* 사진 2열 초대형 */
.gal{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.gal .item{position:relative}
.gal .ph{aspect-ratio:1/1;border-radius:8px}
.gal .lb{position:absolute;left:10px;top:10px;background:#16202a;color:#fff;font-size:12px;padding:4px 10px;border-radius:4px;font-weight:700}
.gal .cp{margin-top:8px;font-size:15px;font-weight:700;color:#16202a}
.gal .cp span{display:block;font-weight:400;font-size:13.5px;color:#6b7885}
.more{text-align:center;margin-top:26px}
.more a{display:inline-block;border:2px solid #16202a;color:#16202a;padding:12px 30px;border-radius:30px;text-decoration:none;font-weight:700}
/* 포커스 섹션 - 강조 밴드 */
.sil{background:#FFF3E6}
.sil .big-t h2{color:#16202a}
.silbig{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:24px}
.silbig .ph{aspect-ratio:4/3;border-radius:8px}
.silrow{background:#fff;border-radius:10px;padding:6px 20px;box-shadow:0 2px 10px rgba(22,32,42,.07)}
.silrow>div{display:flex;gap:14px;padding:16px 0;border-bottom:1px dashed #e7dfd4;align-items:flex-start}
.silrow>div:last-child{border:0}
.silrow .ck{flex:0 0 26px;height:26px;background:#E0521A;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:900}
.silrow b{display:block;font-size:17px;color:#16202a}
.silrow span{font-size:14.5px;color:#5d6b78}
/* 견적 */
.q{background:#16202a;color:#fff}
.q .big-t h2{color:#fff}.q .big-t p{color:#b7c3cd}
.warn{background:#E0521A;border-radius:10px;padding:22px;text-align:center;margin-bottom:24px}
.warn b{font-weight:900;font-size:23px;display:block;letter-spacing:-1px}
.warn span{font-size:14.5px;opacity:.95}
.qg{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:26px}
.qg .cell{background:#1f2b36;border-radius:10px;overflow:hidden}
.qg .ph{aspect-ratio:4/3}
.qg .t{padding:14px 16px}
.qg .t b{display:block;color:#FFB443;font-size:16px}
.qg .t span{font-size:13.5px;color:#98a6b2}
.qcta{text-align:center;border-top:1px solid #2c3a47;padding-top:26px}
.qcta .n{font-family:'IBM Plex Mono';font-size:34px;color:#FFB443;display:block}
.qcta a{display:inline-block;margin-top:14px;background:#E0521A;color:#fff;padding:16px 40px;border-radius:8px;text-decoration:none;font-weight:900;font-size:19px}
footer{background:#0f171f;color:#7b8894;padding:32px 0;font-size:13px;text-align:center}
.fixed{position:fixed;bottom:0;left:0;right:0;background:#E0521A;color:#fff;text-align:center;padding:18px;font-weight:900;font-size:18px;text-decoration:none;z-index:60}
@media(max-width:760px){.hero h1{font-size:30px}.big-t h2{font-size:26px}.silbig{grid-template-columns:1fr}.gal{gap:10px}}
@media(min-width:761px){.hero .ph{aspect-ratio:auto;height:min(48vh,470px)}.hero img.ph{height:min(48vh,470px);object-fit:cover}}
"""