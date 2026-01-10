from playwright.sync_api import sync_playwright
import pandas as pd

def save_gmarket_bestsellers_html():
    with sync_playwright() as p:
        # 1. 브라우저 실행
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        url = "https://www.gmarket.co.kr/n/best"

        try:
            print(f"접속 중: {url}")
            page.goto(url, wait_until="domcontentloaded")

            # 3. 스크롤 로직 (작성하신 부분을 그대로 쓰되, 안정성을 위해 조금 더 반복)
            print("데이터 로딩을 위해 스크롤 중...")
            for _ in range(10):
                page.keyboard.press(key="PageDown")
                # Playwright 자체 대기 함수인 wait_for_timeout
                page.wait_for_timeout(200) 

            # 4. 파일 저장
            html_content = page.content()
            with open(file="gmarket_bestsellers.html", mode="w", encoding="UTF-8") as f:
                f.write(html_content)

            print("페이지 콘텐츠를 gmarket_bestsellers.html로 저장했습니다.")

        except Exception as e:
            print(f"에러 발생: {e}")

def scrape_gmakret_bestsellers():
    with sync_playwright() as p:
        # 크롬 브라우저 실행. 헤드리스 False로 브라우저 창을 직접 보이게 한다.
        # slow_mo =50은 각 동작 사이에 50ms 지연을 주어서 너무 빠르지 않게 설정
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        url = "https://www.gmarket.co.kr/n/best"
        print("G마켓 베스트 페이지로 이동합니다.", url)

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
        except TimeoutError:
            print("페이지 로드 시간이 초과되었습니다. 다시 시도합니다.")
        
        print("스크롤을 내려서 데이터들을 로드합니다.")
        for _ in range(5):
            page.keyboard.press(key="PageDown")
            page.wait_for_timeout(200)

        items=page.locator(selector=".box__best-list  ul  li").all()
        print(f"총 {len(items)}개 상품을 찾았습니다.")

        all_products=[]
        for i,item in enumerate(iterable=items):
            item_class=item.get_attribute('class') or ''
            
            if 'list-item--banner' in item_class or 'list-item--relation' in item_class:
                print(f'{i}번째 아이템은 광고 배너이므로 건너뜁니다.')
                continue

            rank=None
            title=None
            original_price=None
            sale_price=None

            try:
                rank = item.locator(".box__label-rank").inner_text()
            except Exception as e:
                print(f"{i}번째 아이템의 랭크를 가져오는 도중에 {e} 에러가 발생했습니다.")

            try:
                title = item.locator(".box__item-title").inner_text()
            except Exception as e:
                print(f"{i}번째 아이템의 타이틀을 가져오는 도중에 {e} 에러가 발생했습니다.")

            try:
                original_price_element = item.locator(".box__price-original .text.text__value")
                if original_price_element.count() > 0:
                    original_price=original_price_element.inner_text()
            except Exception as e:
                print(f"{i}번째 아이템의 원가를 가져오는 도중에 {e} 에러가 발생했습니다.")

            try:
                sale_price_element = item.locator(".box__price-seller .text.text__value")
                if sale_price_element.count() > 0:
                    sale_price=sale_price_element.inner_text()
            except Exception as e:
                print(f"{i}번째 아이템의 판매가를 가져오는 도중에 {e} 에러가 발생했습니다.")

            all_products.append(
                {
                    "순위":rank,
                    "상품명":title,
                    "원가":original_price,
                    "판매가":sale_price
                }
            )
        
        return all_products

if __name__ == "__main__":
    all_products = scrape_gmakret_bestsellers()
    if all_products:
        df = pd.DataFrame(all_products)
        df.to_csv("gmarket_bestsellers.csv", index=False, encoding="utf-8-sig")
        print("상품 정보를 gmarket_bestsellers.csv 파일로 저장했습니다.")
    else:
        print("상품 정보를 추출할 수 없습니다.")