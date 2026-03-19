from playwright.sync_api import expect, Page
import re
from locators import Locators

def test_yandex_search(page: Page):
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


from playwright.sync_api import Page, expect


def test_todomvc_search_add_and_delete_one_task_locators_byhand(page: Page):
    # 1. Открыть сайт (убрали лишние пробелы в URL)
    page.goto("https://demo.playwright.dev/todomvc")

    # 2. Найти поле ввода по placeholder
    todo_input = page.get_by_placeholder("What needs to be done?")
    expect(todo_input).to_be_visible()

    # 3. Ввести текст в поле
    todo_input.fill("learn python for 2 hours")

    # 4. Нажать Enter
    todo_input.press("Enter")

    # 5. Проверить - задача появилась в списке дел
    to_do_item = page.get_by_test_id("todo-item").filter(has_text="learn python for 2 hours")
    expect(to_do_item).to_be_visible()

    # 6. Проверить счётчик задач
    todo_count = page.get_by_test_id("todo-count")
    expect(todo_count).to_have_text("1 item left")

    # 7. Удалить задачу (ищем кнопку ВНУТРИ элемента задачи)
    to_do_item.hover()
    delete_button = to_do_item.get_by_role("button", name="Delete")  # ← исправлено!
    expect(delete_button).to_be_visible()
    delete_button.click()

    # 8. Проверить удаление (ищем заново, а не через старый локатор)
    expect(
        page.get_by_test_id("todo-item").filter(has_text="learn python for 2 hours")
    ).to_have_count(0)  # ← исправлено!

    # 9. Проверить обновлённый счётчик
    expect(page.get_by_test_id("todo-count")).to_have_count(0)


def test_todomvc_add_and_delete_one_task_class_locators(page: Page):
    """Добавление задачи и ее удаление"""


    # 1. Открыть сайт demo.playwright.dev/todomvc
    page.goto("https://demo.playwright.dev/todomvc")

    # 2. Ввести текст в поле
    expect(Locators.TODO_INPUT).to_be_visible()

    Locators.TODO_INPUT.fill("learn python for 2 hours")
    Locators.TODO_INPUT.press("Enter")

    # 3. Проверить - задача появилась в "списке дел"
    Locators.TODO_ITEM.filter(has_text="learn python for 2 hours")
    expect(Locators.TODO_ITEM).to_be_visible()

    # 4. Проверить - задача добавлена в "список дел"
    todo_count = page.get_by_test_id("todo-count")
    expect(todo_count).to_have_text("1 item left")

    # 5. Удалить добавленную задачу из "списка дел"
    Locators.TODO_ITEM.hover()
    expect(Locators.DELETE_BUTTON).to_be_visible()
    Locators.DELETE_BUTTON.click()

    # 6. Проверить отсутствие удаленной задачи в "списке дел"
    expect(page.get_by_test_id("todo-item").filter(has_text="learn python for 2 hours")).to_have_count(0)

    # 7. Проверить отсутствие счетчика, при пустом списке задач
    expect(Locators.TODO_COUNT).to_have_count(0)


def test_todomvc_add_more_one_task(page: Page):
    """"Составление целого списка задач"""

    page.goto("https://demo.playwright.dev/todomvc")

