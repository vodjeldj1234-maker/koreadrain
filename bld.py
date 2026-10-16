# -*- coding: utf-8 -*-
"""건물·현장 유형별 페이지 (48째방, 2026-10-16) — 주인님 「건물 유형 페이지도 진행해」.

   팔도의 「빌라 우수관」「공장 트렌치」 같은 페이지를 우리 식으로: **실제 사례가 있는 유형만** 만든다.
   ★ 사진 = 그 유형 사례의 실제 사진(이미 검수된 img/case/…) → alt·캡션은 사례 데이터 그대로.
   ★ 소개 글 = 그 유형 사례 요약에 적힌 사실만 다시 묶었다. 사례에 없는 말(작업 기간·가격·「영업 중 작업」 등)은 안 쓴다.
   ★ 아파트 트렌치처럼 실제 현장이 없는 유형은 만들지 않는다 (10/16 원본 폴더에 아파트 트렌치 현장 0곳).
   ★ 지역 이름 없음 — 첫 페이지처럼 출장 지역(권역 전체)만 보인다. 종목 사이 링크는 된다(48째방 서비스 격리 해제).
   slug 는 한 번 정하면 바꾸지 않는다."""
import html

# (slug, 이름, 제목 앞말, 설명, 사례 slug 목록, 소개 제목, 소개 문단들)
B = {
"usugwan": [
    ("shop", "상가", "상가 우수관 교체·신설 업체",
     "상가·상가주택 우수관 교체·신설 업체. 매립 우수관 누수는 막고 외벽으로 새로, 새던 홈통·선홈통 전체 교체, 빗물받이 신설. 사진 보내주시면 당일 견적 회신. {phone}",
     ["commercial-building-stainless-pipe-new-hole", "embedded-leak-rope-pvc-four-storey", "shop-row-zinc-downpipe-full-replace",
      "shop-building-gutter-two-downpipes", "embedded-leak-rope-pvc-offset-eave", "alley-rope-stainless-75-redesign",
      "rooftop-parapet-core-pvc-pipe-add", "leaking-zinc-header-to-pvc", "fallen-pipe-pvc-rope-jump-over",
      "shop-building-gutter-bridge", "rooftop-drain-new-hole-stainless-75", "rooftop-parking-drain-slope-new-pipe"],
     "상가 건물에서 한 우수관 공사",
     ["상가 건물에서는 벽 속 매립 우수관이 새는 일이 많았습니다. 4층 상가는 기존 매립 구멍을 막고 바로 옆을 새로 타공해 스텐 우수관을 외벽에 곧게 내렸고, "
      "상가주택 여러 곳은 옥상 배수 홈 안쪽이나 난간 벽을 새로 뚫어 PVC 우수관을 내린 뒤 배수 홈 바닥의 구배와 방수를 다시 잡았습니다.",
      "오래돼 군데군데 구멍이 나고 이음부 실리콘이 떠서 물이 벽을 타고 흐르던 2층 벽돌 상가는 홈통과 선홈통을 전부 바꿨고, "
      "빗물받이가 처음부터 없던 3층 벽돌 상가에는 징크 빗물받이와 선홈통을 새로 달았습니다. 건물 사이 좁은 뒷골목처럼 차가 못 들어가는 자리는 로프를 타고 작업했습니다."]),
    ("house", "단독주택", "단독주택 우수관·빗물받이 시공 업체",
     "단독주택 처마 빗물받이 신설, 낡은 우수관 교체, 옥상 매립 배관 누수 보수. 높은 곳은 스카이·로프로 작업. 사진 보내주시면 당일 견적 회신. {phone}",
     ["house-zinc-gutter-new", "brick-house-zinc-gutter-lines", "brick-house-gutter-square-downpipes", "entrance-roof-gutter-new",
      "brick-house-old-pvc-pipe-replace", "house-drain-outlet-pvc-downpipe", "rooftop-balcony-drain-channel-rebuild"],
     "단독주택에서 한 우수관 공사",
     ["처마에 빗물받이가 아예 없어 빗물이 벽을 타고 흐르거나, 처마에서 떨어진 물이 벽과 바닥을 때려 이끼와 물때가 끼던 집이 많았습니다. "
      "이런 집은 처마에 징크나 사각 빗물받이를 달고 선홈통을 모서리로 내렸습니다. 현관 지붕 물이 현관 앞으로 그대로 떨어지던 집도 같은 방법으로 막았습니다.",
      "오래돼 깨지고 이음부가 새던 3층 벽돌 주택은 처마 물받이는 그대로 두고 PVC 우수관만 바꿨습니다. "
      "옥상 겸 베란다의 매립 배관에서 물이 새 아래층으로 떨어지던 3층 주택은 기존 구멍을 막고 외벽을 타공해 우수관을 새로 낸 뒤, 배수 홈을 몰탈로 다시 잡아 방수했습니다."]),
    ("villa", "빌라", "빌라 우수관 교체·신설 업체",
     "빌라 매립 우수관 누수, 떨어진 선홈통 재고정, 찌그러진 하단 관 교체, 처마 빗물받이 신설. 사진 보내주시면 당일 견적 회신. {phone}",
     ["top-floor-terrace-embedded-leak-100", "dryvit-villa-loose-downpipe-refix", "villa-crushed-zinc-bottom-one-pipe", "tile-eave-gutter-to-rooftop"],
     "빌라에서 한 우수관 공사",
     ["빌라 탑층 테라스의 매립관에서 물이 새던 집은 난간 벽 아래를 코어로 관통하고 매립관 입구를 막은 뒤, 100파이 관을 외벽으로 내렸습니다. "
      "드라이비트 외벽 빌라는 선홈통이 일반 피스로 스티로폼에만 걸려 있어 떨어졌던 것이라, 관은 그대로 두고 13cm 칼블럭으로 벽 깊숙이 다시 고정했습니다.",
      "필로티 주차장 모서리에서 하단이 찌그러진 징크 선홈통은 그 관 한 개만 잘라 바꿔 다시 세웠습니다. "
      "기와 처마에 물받이가 없던 벽돌 빌라는 건물주 요청대로 물을 옥상 바닥으로 보내 기존 옥상 배수구로 흐르게 했습니다."]),
    ("factory", "공장", "공장 우수관·빗물받이 시공 업체",
     "공장 처마 빗물받이 새로 설치, 우수관 신설, 떨어진 스텐 우수관 다시 붙이기. 높은 곳은 스카이·로프 고소작업. 사진 보내주시면 당일 견적 회신. {phone}",
     ["factory-gutter-new-brackets", "factory-gutter-new-stainless-100", "factory-roof-water-stainless-100-new",
      "factory-fallen-stainless-125-refix", "garage-rooftop-small-drain-core-100"],
     "공장·정비소에서 한 우수관 공사",
     ["폭설에 빗물받이가 무너져 옛 브라켓만 남아 있던 공장 처마는 브라켓을 새로 달고 공장용 절곡 빗물받이를 이어 붙였습니다. "
      "우수관 없이 물이 옆으로 흘러 비가 많이 오면 옥상이 넘치던 공장에는 스텐 100파이 우수관을 새로 세웠고, "
      "중간중간 새던 옆 배관은 철거하고 지붕 물을 받는 우수관을 새로 냈습니다.",
      "스텐 125파이 우수관 하단이 떨어져 나간 공장은 떨어진 관을 그대로 다시 붙이고 부러진 브라켓만 바꿨습니다. "
      "비가 오면 옥상에 발목까지 물이 차던 정비소는 작은 매립 배관을 없애고 옆을 크게 타공해 우수관을 냈습니다."]),
    ("rooftop", "옥상", "옥상 우수관 신설·증설 업체",
     "옥상 물이 잘 안 빠질 때 — 난간 벽·바닥을 코어 타공해 우수관 증설, 매립 배관 대신 외벽 우수관 신설, 배수로 구배 재시공. 사진 보내주시면 당일 견적 회신. {phone}",
     ["rooftop-drain-new-hole-stainless-75", "garage-rooftop-small-drain-core-100", "rooftop-deck-side-core-stainless-add",
      "rooftop-parapet-core-pvc-pipe-add", "rooftop-parking-drain-slope-new-pipe", "rooftop-balcony-drain-channel-rebuild"],
     "옥상 물길을 새로 낸 공사",
     ["옥상 배수구 구멍이 작아 물이 빨리 빠지지 않거나, 매립 배관이 작아 비만 오면 발목까지 물이 차던 건물이 있었습니다. "
      "이런 곳은 기존 배수구를 살리거나 없앤 뒤, 바로 옆 벽 하부나 바닥을 코어 드릴로 관통해 외벽으로 우수관을 새로 냈습니다.",
      "방수는 다 해 두었는데 배수가 모자랄 것 같다던 큰 건물 옥상은 데크를 걷지 않고 바로 옆 바닥을 뚫어 한 줄을 더 냈습니다. "
      "옥상 주차장은 벽을 따라 배수로를 일반 몰탈로 새로 쳐서 구배를 잡고 낮은 쪽에 새 배수구를 만들었습니다."]),
    # 49째방 (10/16) — 주인님 「아파트 우수관도 사례로 올리고 페이지 만들어」. 단지 이름·동 번호는 글·사진 모두 없음.
    ("apartment", "아파트", "아파트 우수관 교체·신설 업체",
     "아파트 단지 건물의 새는 우수관 스텐 교체, 물홈통 교체, 옥상 캐노피 빗물받이·선홈통 신설. 사진 보내주시면 당일 견적 회신. {phone}",
     ["apartment-office-pvc-to-stainless-45", "apartment-rooftop-canopy-gutter-new"],
     "아파트에서 한 우수관 공사",
     ["아파트 단지 안 관리사무소 건물은 오래된 흰색 PVC 우수관 이음새에서 물이 새 외벽에 빗물 자국이 남던 곳이었습니다. "
      "옛 관을 아래쪽부터 떼어 내고 빗물받이 안 낙엽과 흙을 걷어낸 뒤, 처마 밑에 스텐 물홈통을 새로 달아 안팎 이음부를 실리콘으로 막았습니다. "
      "처마가 벽보다 나와 있어 직각 대신 45도로 꺾어 벽에 붙이고, 바닥에 묻혀 있던 배수관에 바로 이어 내렸습니다.",
      "꼭대기 층 옥상 테라스의 캐노피는 빗물받이가 처음부터 없어 벽돌 벽으로 녹물 자국이 흘러내리던 곳이었습니다. "
      "캐노피 끝에 징크 빗물받이를 수평과 물 흐를 방향을 맞춰 얹고 브라켓을 1미터 간격으로 단 뒤, 옥상이라 캐노피 지붕 위로 보강 띠를 걸어 고정하고 모서리로 선홈통을 내렸습니다."]),
],
"trench": [
    ("factory", "공장·작업장", "공장·작업장 트렌치 신설 업체",
     "공장 외벽·지하 배수로 신설, 세차장·디테일링샵 실내 바닥 트렌치. 바닥 컷팅부터 앵글·그레이팅까지. 사진 보내주시면 당일 견적 회신. {phone}",
     ["factory-wall-drain", "factory-basement-trench", "carwash-indoor-trench", "detailing-shop-grid-trench"],
     "공장·작업장에서 한 트렌치 공사",
     ["공장 외벽을 따라 배수로를 새로 낸 현장은 바닥을 굴삭기로 깨어 내고, 홈 바닥을 몰탈로 채워 수평을 보며 앵글을 앉힌 뒤 그레이팅을 얹었습니다. "
      "공장 지하는 벽을 따라 앵글을 모서리까지 돌리고 슬롯 덮개와 집수구 그레이팅으로 마감했습니다.",
      "세차장 실내 바닥에는 ㄱ자로, 자동차 디테일링샵 실내 바닥에는 격자 모양으로 트렌치를 이어 앉혔습니다. "
      "두 곳 모두 바닥에 줄을 그어 자리를 잡고 깨어 낸 뒤 트렌치 몸체를 앉혔습니다."]),
    ("indoor", "실내 바닥", "실내 바닥 트렌치 신설 업체",
     "매장 타일 바닥, 빈 실내 바닥, 수영장 바닥에 트렌치 신설·연장. 벽 따라 스텐 트렌치, 벽 하단 배관 구멍까지. 사진 보내주시면 당일 견적 회신. {phone}",
     ["shop-tile-floor-trench", "indoor-trench-catch-basin", "indoor-door-side-trench", "indoor-wall-stainless-trench",
      "pool-tile-trench-extend", "carwash-indoor-trench"],
     "실내 바닥에 낸 트렌치",
     ["매장 타일 바닥은 집기와 벽을 비닐로 덮은 뒤, 트렌치 폭만큼만 타일을 걷어내 바닥을 깨고 몸체를 앉혔습니다. 트렌치 끝은 바닥 배수구로 이었습니다. "
      "빈 실내 바닥은 줄 맞춰 컷팅하고 브레이커로 깨어 낸 뒤, 트렌치 끝을 배관으로 이어 건물 밖에 새로 묻은 집수정까지 보냈습니다.",
      "벽을 따라 스텐 트렌치를 낼 때는 집진기를 달고 두 줄로 컷팅했고, 필요한 자리는 코어 드릴로 벽 하단에 배관 구멍을 뚫었습니다. "
      "수영장은 짧게 끊겨 있던 기존 트렌치를 옆으로 이어 늘렸습니다."]),
    ("driveway", "진입로·측구", "진입로 측구·배수로 보수 업체",
     "무너진 측구 재시공, 진입로를 가로지르는 배수로 덮개 교체(무소음·줄무늬), 녹슨 그레이팅 배수로 보수. 사진 보내주시면 당일 견적 회신. {phone}",
     ["entrance-gutter-noiseless", "entrance-striped-cover", "gutter-rebar-noiseless", "sidewalk-gutter-rebuild", "parking-entrance-grating-repair"],
     "진입로·측구에서 한 배수로 공사",
     ["진입로를 가로지르는 측구의 낡은 주철 덮개를 걷어 보면 받침 앵글이 삭아 있는 경우가 있어, 새 앵글을 앉힌 뒤 무소음 덮개를 얹었습니다. "
      "모서리가 깨진 진입로 배수로는 받침 자리를 정리하고 새 덮개를 한 줄로 맞춰 노란색·검은색 줄무늬 덮개로 마감했습니다.",
      "건물 앞이나 인도 옆 측구가 무너지고 흙과 낙엽이 차 있던 자리는 깨진 측벽을 걷어내고 철근을 넣거나 거푸집을 대 새로 친 뒤 그레이팅이나 무소음 덮개로 마감했습니다. "
      "녹슨 그레이팅 배수로가 있던 주차장 진입로도 옆 바닥을 깨어 내고 새 앵글을 앉혀 같은 순서로 보수했습니다."]),
],
"block": [
    ("entrance-tactile", "건물 출입구 점자블록", "건물 출입구·계단 점자블록 설치·교체 업체",
     "건물 출입구·계단·복도 점자블록 신설, 깨진 점자블록 교체. 화강석·테라조 바닥을 잘라 매립하거나 피스로 고정. 사진 보내주시면 당일 견적 회신. {phone}",
     ["entrance-braille-new", "shop-entrance-braille-new", "stair-landing-braille-new", "stair-front-braille-new",
      "corridor-braille-terrazzo-granite", "lobby-braille-block-replace", "doormat-braille-partial-replace", "screw-fixed-braille-new"],
     "건물 안팎에 넣은 점자블록",
     ["점자블록이 없던 건물 출입구와 상가 출입구, 계단참, 계단 앞, 복도에 새로 넣은 현장이 많습니다. "
      "화강석이나 테라조 바닥을 블록 크기대로 잘라 걷어내고 모르타르를 채워 높이를 잡은 뒤, 블록을 앉혀 기존 바닥 높이에 맞췄습니다.",
      "빛이 바래고 깨진 점자블록은 걷어내고 새 블록으로 바꿨고, 출입 발판 틀에 끼워져 있던 것은 틀을 두고 깨진 것만 골라 바꿔 끼웠습니다. "
      "바닥을 잘라 내지 않고 앵커를 박아 피스로 조이는 점자블록을 설치한 현장도 있습니다."]),
    ("sidewalk", "인도", "인도 보도블록 재시공 업체",
     "들뜨고 꺼진 인도 보도블록 재시공 — 가로수 뿌리로 들뜬 블록, 벽 밑단을 따라 꺼진 블록, 빠진 블록 재설치. 사진 보내주시면 당일 견적 회신. {phone}",
     ["tree-walk-herringbone-relay", "tree-walk-long-section-relay", "tree-walk-curb-block-fix", "roadside-walk-block-relay", "building-front-walk-block-fix"],
     "인도에서 한 보도블록 공사",
     ["가로수 인도의 블록이 들뜨고 틈이 벌어져 걷어내 보면, 흙 속에서 굵은 뿌리가 드러나기도 했습니다. 뿌리를 정리하고 모래 바닥을 평평하게 고른 뒤 본래 무늬대로 다시 깔았습니다.",
      "건물 앞 인도가 벽 밑단을 따라 꺼진 자리, 가로등 기초 옆으로 블록이 빠져 있던 도로변 보도도 블록을 걷어내고 모래로 높이를 잡아 다시 깐 뒤 모래로 줄눈을 채웠습니다."]),
    ("plaza", "광장·진입로", "광장·진입로 바닥 보수 업체",
     "건물 앞 광장 보도블록 재포장, 들뜨고 깨진 화강석 판석 보수, 내려앉은 차량 진입로 블록 재포장. 사진 보내주시면 당일 견적 회신. {phone}",
     ["plaza-block-repave", "plaza-granite-slab-fix", "driveway-sunken-block-relay", "plaza-flowerbed-curve-curb"],
     "넓은 바닥을 다시 깐 공사",
     ["유리 건물 앞 넓은 광장은 사각 블록을 걷어내고 모래를 나눠 부어 바닥을 고른 뒤 새 블록을 이어 깔았습니다. "
      "주차 광장의 들뜨고 깨진 화강석 판석은 걷어내고 모래로 높이를 잡아 새 판석을 깐 뒤 줄눈에 모르타르를 밀어 넣었습니다.",
      "차가 드나들어 블록이 내려앉은 진입로는 걷어내 보니 모래층으로 전선과 관이 지나가고 있어, 바닥을 조심해서 고른 뒤 곧은 자로 높이를 맞춰 다시 깔았습니다."]),
    ("curb", "화단 경계석", "화단 경계석 교체 업체",
     "밀려나고 깨진 화단 경계석 교체 — 곡선·일자·반원 경계석, 잔디밭 둘레 화강석 경계석 보수. 사진 보내주시면 당일 견적 회신. {phone}",
     ["flowerbed-curve-curb-replace", "flowerbed-straight-curb-replace", "plaza-flowerbed-curve-curb", "lawn-edge-curb-fix",
      "flowerbed-round-curb-replace", "tree-walk-curb-block-fix"],
     "경계석을 바꾼 공사",
     ["길가 화단 둘레 경계석이 밀려나고 깨진 곳은 옛 돌을 들어내 자리를 파낸 뒤, 곡선으로 다듬은 새 화강석 경계석을 한 개씩 맞춰 이어 앉혔습니다. "
      "같은 화단의 일자 구간은 갈라진 돌만 빼내 새 돌을 끼우고 밑을 모르타르로 메웠습니다.",
      "광장 화단의 직각 모서리는 포장을 덮개로 보호한 채 곡선 돌로 바꿨고, 잔디밭과 차로 사이 화강석 경계석은 들어내 모르타르로 다시 앉혀 곡선을 맞췄습니다."]),
],
"carstop": [
    ("piloti", "필로티 주차장", "필로티 주차장 카스토퍼 설치 업체",
     "기둥 사이 필로티 주차장 카스토퍼 설치 — 기둥 옆·벽 앞·배수구 앞 좁은 칸까지 줄 맞춰. 사진 보내주시면 당일 견적 회신. {phone}",
     ["piloti-lot-carstop-row", "stone-floor-piloti-carstop", "piloti-stop-mark-carstop", "wall-side-carstop-set"],
     "필로티 주차장에 놓은 카스토퍼",
     ["기둥이 서 있는 필로티 주차장의 주차칸 앞쪽에 카스토퍼를 한 줄로 놓을 때는 줄자로 주차선에서 위치를 쟀습니다. "
      "기둥 옆 칸·벽 앞 칸·배수구 앞 칸처럼 자리가 좁은 칸도 줄을 맞춰 설치했습니다.",
      "돌 무늬 바닥이나 벽으로 막힌 주차칸에도 칸마다 카스토퍼를 놓고 고정했습니다."]),
    ("outdoor", "야외 주차장", "야외 주차장 카스토퍼 설치 업체",
     "야외·아스팔트 주차장 카스토퍼 설치 — 실을 띄워 줄을 잡고 칸마다 반듯하게, 고정 자리는 마개로 마무리. 사진 보내주시면 당일 견적 회신. {phone}",
     ["outdoor-lot-carstop-set", "asphalt-lot-carstop-line", "wide-outdoor-lot-carstop"],
     "야외 주차장에 놓은 카스토퍼",
     ["야외 주차장은 주차선을 기준으로 칸마다 자리를 먼저 나눠 놓고, 실을 띄워 설치 줄을 잡은 뒤 주차칸 끝에 반듯하게 놓았습니다.",
      "풀숲과 맞닿은 넓은 주차장처럼 칸이 많은 곳도 같은 방법으로 길게 줄지어 설치했고, 고정한 자리는 노란 마개로 덮어 마무리했습니다."]),
    ("speedbump", "실내 주차장 과속방지턱", "실내 주차장 과속방지턱 설치 업체",
     "실내·지하 주차장 경사로 앞과 통로에 조각형 과속방지턱 설치 — 레이저 기준선으로 줄을 잡아 한 줄로. 사진 보내주시면 당일 견적 회신. {phone}",
     ["indoor-ramp-speed-bump", "indoor-aisle-long-speed-bump"],
     "실내 주차장에 놓은 과속방지턱",
     ["실내 주차장 경사로 앞 통로에는 노랑·검정 조각을 번갈아 이어 통로를 가로질러 한 줄로 잇고, 조각마다 흰 화살표가 들어가게 맞췄습니다.",
      "넓은 실내 주차장 통로에는 레이저 기준선으로 줄을 잡아 조각을 통로 끝까지 한 줄로 이어 긴 과속방지턱을 만들었습니다."]),
    ("lines", "주차선 도색", "주차선 도색 업체",
     "주차칸 새로 칠하기 · 지워진 주차선 다시 칠하기 — 테이프로 선 폭을 잡고 롤러로. 사진 보내주시면 당일 견적 회신. {phone}",
     ["narrow-aisle-parking-line-paint", "block-floor-parking-line-paint"],
     "주차선을 새로 칠한 공사",
     ["건물 옆 좁은 통로 바닥에 주차칸을 새로 칠할 때는 먼지를 털어내고 테이프로 선 폭을 잡은 뒤 롤러로 칠했습니다.",
      "상가 앞 포장 바닥도 파란 테이프로 선 폭을 잡고 흰색으로 주차칸 선을 칠했습니다."]),
],
"lexan": [
    ("apartment", "아파트", "아파트 캐노피·렉산 지붕 교체 업체",
     "아파트 출입구·통로·관리동 캐노피, 파고라 채광 지붕, 자전거 보관대·분리수거장·주차장 진입로 렉산 지붕 교체와 보수. 사진 보내주시면 당일 견적 회신. {phone}",
     ["apt-entrance-canopy-lexan-one-row", "apt-walkway-canopy-lexan-full-replace", "apt-office-front-canopy-lexan-replace",
      "apt-pergola-skylight-lexan-replace", "apt-bike-shelter-lexan-partial-replace", "apt-parking-ramp-roof-silicone",
      "apt-recycling-shed-roof-silicone", "apt-recycling-shed-lexan-roof-repair", "apt-park-round-pergola-lexan-strips"],
     "아파트 단지에서 한 렉산 공사",
     ["아파트 단지에는 출입구·통로·관리동 앞 캐노피, 파고라 채광 지붕, 자전거 보관대와 분리수거장 지붕처럼 렉산 지붕이 여러 곳에 있습니다. "
      "판이 깨진 한 줄만 바꾼 출입구 캐노피, 덮개바가 일어나 바람에 들릴 것 같던 통로 캐노피 전면 교체, 누렇게 바래 금이 간 관리동 앞 캐노피를 복층렉산으로 바꾼 현장이 있습니다.",
      "주차장 진입로·분리수거장 지붕은 판을 그대로 두고 덮개바 양옆 이음부를 따라 실리콘을 새로 쏴 보강했습니다. "
      "자전거 보관대처럼 한 칸에만 구멍이 난 곳은 그 칸만 바꿨습니다."]),
    ("entrance", "건물 출입구 캐노피", "상가·건물 출입구 캐노피 교체 업체",
     "상가·건물 출입구 아치 캐노피 교체, 터널형 캐노피 렉산 전체 교체, 낡은 캐노피 떼고 새 캐노피 설치. 사진 보내주시면 당일 견적 회신. {phone}",
     ["shop-entrance-arch-canopy-replace", "shop-front-arch-canopy-lexan-replace", "entrance-tunnel-canopy-lexan-replace",
      "entrance-arch-roof-lexan-replace", "building-entrance-canopy-replace", "warehouse-door-canopy-install"],
     "출입구 캐노피를 바꾼 공사",
     ["택배차가 지나가다 쳐서 망가진 1층 상가 출입구 아치 캐노피는 사이즈를 실측한 뒤 옛 캐노피를 통째로 떼어 내고 새 캐노피를 석재 벽에 고정했습니다. "
      "이끼와 얼룩이 낀 상가 앞 아치 캐노피는 골조만 남기고 현장에서 판을 재단해 전체를 바꿨습니다.",
      "곰팡이와 때로 뿌옇게 된 터널형 캐노피, 판이 찢어져 벌어진 정문 위 아치 지붕도 헌 판을 걷어내고 새 판으로 다시 씌웠습니다. "
      "캐노피가 없던 창고형 건물 출입구에는 처마에 고정쇠와 와이어를 걸어 새로 달았습니다."]),
    ("house", "주택 캐노피", "주택 캐노피·렉산 지붕 업체",
     "주택 벽면 캐노피 판 교체, 처마 아래 브라켓 캐노피 설치, 데크 위 복층렉산 지붕. 사진 보내주시면 당일 견적 회신. {phone}",
     ["house-wall-canopy-lexan-replace", "house-eaves-bracket-canopy-install", "house-deck-canopy-lexan-roof"],
     "주택에 한 캐노피 공사",
     ["판 없이 브라켓만 남아 있던 주택 벽면 캐노피에는 새 판을 올려 고정했고, 기존 판에 금이 가 있던 벽돌 주택은 벽을 따라 브라켓을 줄지어 고정하고 판을 올려 집 앞면 전체를 덮었습니다.",
      "출입구에서 데크까지 이어지는 주택 캐노피는 벽에서 뻗은 골조 위에 복층렉산 판을 올려 덮었습니다."]),
],
}


def pages(svc):
    """이 종목의 건물 유형 페이지(region 꼴 dict) 목록"""
    out = []
    by = {c["slug"]: c for c in (svc.get("cases") or [])}
    for slug, name, head, desc, cs, st, paras in B.get(svc["key"], []):
        cases = [by[s] for s in cs if s in by]
        assert len(cases) == len(cs), (svc["key"], slug, [s for s in cs if s not in by])
        out.append(dict(kind="bld", slug=slug, name=name, head=head, desc_t=desc, cases=cases, story=(st, paras)))
    # ★ 49째방 — 실제 사례가 없는 종목×장소 페이지(「아파트 트렌치 시공·교체 업체」 등, 글은 place_data.json)를 뒤에 붙인다.
    #   사진은 종목 공통 사진 + 「같은 공사를 한 다른 현장 사진」 안내, 사례 칸은 그 종목 전체 사례.
    import place
    have = {p["slug"] for p in out}
    for p in place.combo_pages(svc["key"]):
        assert p["slug"] not in have, (svc["key"], p["slug"])
        out.append(p)
    return out


def setup(b, svc, p):
    """페이지 그릴 때 필요한 값을 채운다 (b = build 모듈)."""
    S = b.SITE
    p["title"] = "%s | %s" % (p["head"], S["name"])
    p["desc"] = p["desc_t"].format(phone=S["phone"])
    p["area"] = svc.get("area")
    regs = svc.get("region_list") or b.REGIONS
    p["cities"] = svc.get("cities") or [c for r in regs for c in r["cities"]]
    if p.get("combo"):                       # 49째방 종목×장소 — 종목 공통 사진 (그 장소에서 찍은 사진이 아니라고 밝힌다)
        p["hero_src"] = b.pick("hero-" + svc["key"])
        p["hero_alt"] = "%s 시공 현장" % svc["label"]
        p["gal"] = [(b.pick("%s-%d" % (svc["key"], i)), row[0], row[1], row[2]) for i, row in enumerate(svc["gallery"][:6], 1)]
        p["gal_h2"] = "%s <em>현장 사진</em>" % html.escape(svc["label"])
        p["gal_p"] = "%s 현장 사진은 시공하는 대로 올립니다. 아래는 같은 공사를 한 다른 현장 사진입니다." % html.escape(p["name"])
        return p
    c0 = p["cases"][0]
    p["hero_src"] = "/img/case/%s-%02d.jpg" % (c0["slug"], c0["cover"])
    p["hero_alt"] = c0["title"]
    # 사진 6장 = 사례 3곳의 「시공 전」 한 장 + 「완료」 한 장
    gal = []
    for c in p["cases"][:3]:
        ph = c["photos"]
        bi = next((i for i, x in enumerate(ph) if "전" in x[0]), 0)
        ai = next((i for i in range(len(ph) - 1, -1, -1) if ph[i][0] in ("완료", "시공 후", "후")), len(ph) - 1)
        for i in (bi, ai):
            stage, title, desc = ph[i][0], ph[i][1], ph[i][2]
            gal.append(("/img/case/%s-%02d.jpg" % (c["slug"], i + 1), stage, title, desc))
    p["gal"] = gal
    return p


def links(b, svc, current=None, title=None):
    """같은 종목 건물 유형 페이지 링크 묶음 (종목 첫 페이지 · 다른 유형 페이지 · 도시 페이지에 붙인다)."""
    rows = []
    for p in pages(svc):
        if current and p["slug"] == current["slug"]:
            continue
        rows.append('<a href="%s">%s<i>&rsaquo;</i></a>' % (b.url_of(svc, p), html.escape(p["head"].replace(" 업체", ""))))
    if not rows:
        return ""
    if current:
        rows.append('<a href="%s">%s<i>&rsaquo;</i></a>' % (b.url_of(svc), html.escape(svc["home_label"])))
    return ('<section class="nav"><div class="wrap">\n'
            '  <h2>%s</h2><p>실제로 해 본 현장만 따로 정리했습니다.</p>\n'
            '  <div class="links">%s</div>\n'
            '</div></section>\n' % (html.escape(title or "건물·현장별 안내"), "".join(rows)))
