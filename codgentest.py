import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://10.101.54.90:4200/login")
    page.get_by_role("textbox", name="Enter Email (eg. someuser@").click()
    page.get_by_role("textbox", name="Enter Email (eg. someuser@").fill("ankit.sahu@stltech.in")
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").fill("#Ankit@1234")
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("link", name="Configuration").click()
    page.get_by_role("radio", name="Map").click()
    page.get_by_role("img", description="Collapse Sidebar", exact=True).click()
    page.get_by_text("0").nth(1).click()
    page.locator("body").press("ControlOrMeta+-")
    page.locator("body").press("ControlOrMeta+-")
    page.locator("body").press("ControlOrMeta+-")
    page.locator("body").press("ControlOrMeta+-")
    page.locator("body").press("ControlOrMeta+-")
    page.locator("body").press("ControlOrMeta+-")
    page.get_by_text("High Proximity Threshold* 0 Allow Look ForwardDisabled Enable Offline").click()
    page.get_by_text("0").nth(2).click()
    page.locator(".boolean-status-circle").first.click()
    page.get_by_text("Disabled").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^Disabled$")).nth(5).click()
    page.get_by_text("Disabled").nth(3).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
