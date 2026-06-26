class TempMonitoringPage:
    def __init__(self, page):
        self.page = page
        
        # --- Core Navigation & Action Buttons ---
        self.temp_monitoring_radio = page.get_by_role("radio", name="Temp Monitoring", exact=True)
        self.edit_button = page.get_by_role("button", name="Edit")
        self.save_button = page.get_by_role("button", name="Save Changes")
        self.dismiss_button = page.get_by_role("button", name="Dismiss Changes")

    # --- Core Actions ---
    def open_temp_monitoring(self):
        """Navigates to the Temp Monitoring sub-tab."""
        self.temp_monitoring_radio.scroll_into_view_if_needed()
        self.temp_monitoring_radio.click()

    def click_edit(self):
        self.edit_button.click()

    def click_dismiss(self):
        self.dismiss_button.click()

    # --- Helper Method ---
    def _get_input_locator(self, visible_label_text: str):
        """Dynamically finds an input field based on its wrapper text."""
        wrapper = self.page.locator("div.field-wrapper").filter(has_text=visible_label_text)
        return wrapper.locator("input[type='number'], input[type='text'], input[type='time']")

    # --- Field Interactions ---
    def get_field_value(self, field_name: str) -> str:
        """Retrieves the current value inside the specified input field."""
        input_el = self._get_input_locator(field_name)
        input_el.wait_for(state="visible")
        return input_el.input_value()

    def fill_field_value(self, field_name: str, value: str):
        """Clears and fills a specified input field."""
        input_el = self._get_input_locator(field_name)
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))       
        input_el.blur()