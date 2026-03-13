from playwright.sync_api import Page, expect
from time import sleep
import re


def test_at_05(page: Page):
    page.goto("https://www.google.com/")
    search_field = page.get_by_role('combobox')
    search_field.fill('cat')
    search_field.press('enter')
    expect(page).to_have_title('')




def test_at_05_2(page: Page):
    page.goto("https://www.qa-practice.com/elements/input/simple")
    sleep(3)
    page.get_by_role("button").click()

    # Проверяем, что текст отображается
    requirements_text = page.locator('#req_text')
    expect(requirements_text).to_be_visible()
    sleep(3)

    # Проверяем содержимое текста
    expect(requirements_text).to_have_text(
        re.compile(
            r"This is a required field.*"
            r"User should be able to enter text into this field.*"
            r"Text should be a valid string.*"
            r"Text length limits.*"
            r"Max: 25 characters.*"
            r"Min: 2 characters.*"
            r"User can submit this one-field form by pressing Enter.*"
            r"After submitting the form, the text entered by the user is displayed on the page",
            re.DOTALL
        )
    )
    sleep(3)

