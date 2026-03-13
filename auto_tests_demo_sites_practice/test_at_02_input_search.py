from playwright.sync_api import sync_playwright


def test_yandex_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Открываем Яндекс
        page.goto("https://www.ya.ru")

        # 2. Ждём немного, чтобы модалка успела появиться (макс. 3 сек)
        page.wait_for_timeout(2000)  # 2 секунды — достаточно для модалки

        # 3. Пытаемся закрыть модалку (кнопка "Закрыть" — часто просто X или текст "Закрыть")
        try:
            # Селектор для кнопки "Закрыть" в модалке
            if page.is_visible('button:has-text("Закрыть")'):
                page.click('button:has-text("Закрыть")')
            elif page.is_visible('div[role="dialog"] button:last-child'):
                # Последняя кнопка в диалоговом окне (часто "Закрыть")
                page.click('div[role="dialog"] button:last-child')
        except Exception as e:
            print("Модалка не найдена или уже закрыта — продолжаем")

        # 4. Теперь ищем поле поиска — используем более надёжный селектор:
        # На Яндексе сейчас работает: input[type="search"] или [name="text"]
        page.wait_for_selector('textarea[name="text"]', timeout=5000)

        # 3. Вводим текст в поле поиска
        page.fill('textarea[name="text"]', "Playwright")

        # 4. Нажимаем Enter
        page.keyboard.press("Enter")

        # 5. Ждём, пока загрузится страница результатов
        page.wait_for_selector('text=playwright.dev')

        # 6. Проверяем: есть ли в результатах официальный сайт?
        assert page.is_visible('text=playwright.dev'), "Официальный сайт не найден"

        browser.close()