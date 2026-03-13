from playwright.sync_api import sync_playwright


def test_google_search():
    # 1. Запускаем Playwright
    with sync_playwright() as p:
        # 2. Запускаем браузер (chromium)
        browser = p.chromium.launch(headless=False)  # headless=True — без окна
        # 3. Открываем новую вкладку
        page = browser.new_page()

        # 4. Переходим на Google
        page.goto("https://www.ya.ru")

        # 5. Проверяем: загрузилась ли страница?
        assert "Яндекс — быстрый поиск в интернете" in page.title()

        # 6. Закрываем браузер
        browser.close()