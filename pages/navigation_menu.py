class NavigationMenu:
    def __init__(self, page):
        self.page = page
        self.sidebar_toggle = page.locator("xpath=//div[contains(@class, 'sidebar-toggle-container')]")
        self.config_link = page.get_by_role("link", name="Configuration")

    def go_to_configuration(self):
        self.sidebar_toggle.click()
        self.page.wait_for_timeout(1000) 
        self.config_link.click()
        self.page.wait_for_url(lambda url: "configPage" in url, timeout=10000)