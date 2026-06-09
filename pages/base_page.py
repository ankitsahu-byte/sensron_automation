from playwright.sync_api import Page

class BasePage:
    """Contains common methods used across all page objects."""
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def wait_for_url_contains(self, text: str, timeout: int = 5000):
        self.page.wait_for_url(lambda url: text in url, timeout=timeout)