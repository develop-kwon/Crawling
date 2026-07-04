# crawling

G마켓 베스트 상품 페이지(`https://www.gmarket.co.kr/n/best`)를 Playwright로 크롤링하여 상위 상품의 순위, 상품명, 원가, 판매가를 수집하고 CSV로 저장하는 스크립트입니다.

## 요구 사항

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) (의존성 관리)
- pandas, playwright

## 설치

```bash
uv sync
uv run playwright install chromium
```

## 실행

```bash
uv run main.py
```

실행하면 브라우저 창이 열리고(headless=False) G마켓 베스트 페이지에 접속해 스크롤을 내리며 상품 목록을 로드한 뒤, 광고 배너 항목을 제외한 상품 정보를 수집합니다. 결과는 `gmarket_bestsellers.csv`로 저장됩니다.

## 파일 구성

- `main.py` — 크롤링 로직
  - `save_gmarket_bestsellers_html()`: 베스트 페이지에 접속해 스크롤 후 렌더링된 HTML 전체를 `gmarket_bestsellers.html`로 저장합니다. (셀렉터 확인 등 디버깅용)
  - `scrape_gmakret_bestsellers()`: 베스트 페이지의 상품 목록(`.box__best-list ul li`)을 순회하며 순위, 상품명, 원가, 판매가를 추출해 리스트로 반환합니다. 광고/추천 배너 항목(`list-item--banner`, `list-item--relation`)은 건너뜁니다.
- `gmarket_bestsellers.csv` — 크롤링 결과 (순위, 상품명, 원가, 판매가)
- `gmarket_bestsellers.html` — 디버깅용으로 저장된 렌더링 완료 HTML 스냅샷

## 출력 데이터 예시

| 순위 | 상품명 | 원가 | 판매가 |
| --- | --- | --- | --- |
| 1 | 25년 햅쌀 새청무 상등급 10kg | 29,900 | 28,900 |
| 2 | (타임딜) 칠성사이다 210ml x 30캔 | | 18,000 |

원가가 없는 상품(할인 전 가격 표기가 없는 경우)은 빈 값으로 저장됩니다.

## 참고

- 페이지 구조(CSS 셀렉터)가 변경되면 각 항목 추출 로직(`box__label-rank`, `box__item-title`, `box__price-original`, `box__price-seller`)을 함께 수정해야 합니다.
- 크롤링 대상 사이트의 이용 약관 및 robots.txt를 확인한 후 사용하세요.
