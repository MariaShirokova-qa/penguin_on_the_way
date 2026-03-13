from playwright.sync_api import Page, expect
from time import sleep


def test_visible(page: Page):
    sleep(3)

    page.goto("https://www.qa-practice.com/elements/input/simple")
    sleep(2)

    reqs = page.locator('#req_text')
    expect(reqs).not_to_be_visible()
    page.locator('#req_header').click()
    sleep(2)

    expect(reqs).to_be_visible()
    sleep(2)