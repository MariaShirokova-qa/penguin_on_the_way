from time import sleep

from playwright.sync_api import expect, Page
import re
import time

def test_yandex_search(page):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Открываем Яндек    с
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



def test_yandex_search2(page: Page):
    # 1. Открываем Яндекс
    page.goto("https://www.ya.ru")

    # 2. Ждём появления поля поиска (надёжнее, чем ждать модалку)
    search_input = page.locator('textarea[name="text"]')
    expect(search_input).to_be_visible(timeout=10000)

    # 3. Закрываем модалку, если она есть (без исключений)
    close_button = page.locator('button:has-text("Закрыть"), button:has-text("Close")')
    if close_button.is_visible(timeout=2000):
        close_button.click()

    # 4. Вводим текст в поле поиска
    search_input.fill("Playwright")

    # 5. Нажимаем Enter
    search_input.press("Enter")

    # 6. Ждём загрузки результатов
    expect(page).to_have_title(re.compile("Playwright", re.IGNORECASE), timeout=10000)

    # 7. Проверяем наличие официального сайта
    expect(page.locator('text=playwright.dev')).to_be_visible(timeout=5000)


def test_todomvc_search3 (page: Page):

    # 1. Открыть сайт demo.playwright.dev/todomvc
    page.goto("https://demo.playwright.dev/todomvc")

    # 2. Найти поле ввода по placeholder
    todo_input = page.get_by_placeholder("What needs to be done?")
    expect(todo_input).to_be_visible

    # 3. Ввести текст в поле
    todo_input.fill("learn python for 2 hours")

    # 4. Нажать Enter
    todo_input.press("Enter")

    # 5. Проверить - задача появилась в "списке дел"
    to_do_item = page.get_by_test_id("todo-item").filter(has_text="learn python for 2 hours")
    expect(to_do_item).to_be_visible()

    # 6. Проверить - задача добавлена в "список дел"
    todo_count = page.get_by_test_id("todo-count")
    expect(todo_count).to_have_text("1 item left")

    # 7. Удалить добавленную задачу из "списка дел"
    delete_button = page.get_by_label("Delete")
    expect(delete_button).to_be_visible()
    delete_button.click()

    # 8. Проверить отсутствие удаленной задачи в "списке дел"
    expect(to_do_item).not_to_be_visible()
    expect(todo_count).not_to_be_visible()



