from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # Locators
        self.brand_logo = page.locator("img[src*='sensron.svg']")
        self.summary_btn = page.get_by_role("button", name="Summary")
        self.channel_plot = page.get_by_label("Channel Plot")
        self.alerts_btn = page.get_by_role("button", name="Alerts - Alarms")
        self.zones_btn = page.get_by_role("button", name="Zones")
        self.cameras_btn = page.get_by_role("button", name="Cameras")
        
        # Filter Locators
        self.filter_btn = page.locator("button[mattooltip='Filter Events']")
        self.apply_btn = page.get_by_role("button", name="Apply")
        self.clear_btn = page.get_by_role("button", name="Clear")
        self.severity_btn = page.get_by_text("Severity", exact=True)
        self.high_option = page.get_by_text("High", exact=True)
        
        # Map & Fullscreen Locators
        self.map_style_btn = page.get_by_role("button", name="Map Style")
        self.fullscreen_btn = page.get_by_role("button", name="Fullscreen")
        self.minimize_btn = page.get_by_role("button", name="Exit Fullscreen")
        self.summary_popup_btn = page.locator("button.summary-btn")
        self.live_trigger = page.locator("label[for='summary-dropdown-toggle']")

    # --- Actions & Element Retrievers ---
    def wait_for_dashboard_to_load(self):
        """Waits for the dashboard URL to appear and network traffic to settle."""
        # Using the helper method inherited from BasePage
        self.wait_for_url_contains("dashboard")
        self.page.wait_for_load_state("networkidle")

        
    def is_brand_logo_visible(self) -> bool:
        self.brand_logo.wait_for(state="visible", timeout=5000)
        return self.brand_logo.is_visible()

    def get_sidebar_link(self, route: str):
        return self.page.locator(f"a[href='{route}']")

    def open_zones_panel(self):
        #self.zones_btn.wait_for(state="visible")
        self.zones_btn.click()

    def open_cameras_panel(self):
        #self.cameras_btn.wait_for(state="visible")
        self.cameras_btn.click()

    def get_exact_text_element(self, text: str):
        return self.page.get_by_text(text, exact=True)

    def apply_high_severity_filter(self):
        self.alerts_btn.click()
        #self.filter_btn.wait_for(state="visible")
        self.filter_btn.click()
        
        #self.severity_btn.wait_for(state="visible")
        self.severity_btn.click()
        
        #self.high_option.wait_for(state="visible")
        self.high_option.click()
        
        self.apply_btn.click()

    def clear_filters(self):
        #self.filter_btn.wait_for(state="visible")
        self.filter_btn.click()
        #self.clear_btn.wait_for(state="visible")
        self.clear_btn.click()

    def toggle_fullscreen(self, enter: bool = True):
        if enter:
            #self.fullscreen_btn.wait_for(state="visible")
            self.fullscreen_btn.click()
        else:
            #self.minimize_btn.wait_for(state="visible")
            self.minimize_btn.click()

    def open_summary_popup(self):
        #self.summary_popup_btn.wait_for(state="visible", timeout=5000)
        self.summary_popup_btn.click()

    def select_summary_option(self, option_text: str):
        self.live_trigger.wait_for(state="visible", timeout=5000)
        self.live_trigger.click()
        self.page.wait_for_timeout(500)
        
        option_locator = self.page.locator(f"//div[@class='dropdown-option' and contains(text(), '{option_text}')]")
        option_locator.wait_for(state="visible", timeout=5000)
        
        is_visible = option_locator.is_visible()
        option_locator.click(force=True)
        self.page.wait_for_timeout(500)
        
        return is_visible