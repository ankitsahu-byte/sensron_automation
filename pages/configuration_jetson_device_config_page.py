class JetsonDevicePage:
    def __init__(self, page):
        self.page = page
        
        # --- Core Navigation & Action Buttons ---
        self.jetson_radio_tab = page.get_by_role("radio", name="Jetson Device Config", exact=True)
        self.edit_button = page.get_by_role("button", name="Edit")
        self.save_button = page.get_by_role("button", name="Save Changes")
        self.dismiss_button = page.get_by_role("button", name="Dismiss Changes")

    # --- Core Actions ---
    def open_jetson_config(self):
        """Navigates to the Jetson Device Config sub-tab."""
        self.jetson_radio_tab.scroll_into_view_if_needed()
        self.jetson_radio_tab.click()

    def click_edit(self):
        self.edit_button.click()

    def save_changes(self):
        self.save_button.click()

    def click_dismiss(self):
        self.dismiss_button.click()

    def get_error_message(self, expected_error: str):
        return self.page.locator("div.field-error-message").filter(has_text=expected_error)

    # --- Helper Method ---
    def _get_number_input(self, visible_label_text: str):
        """Dynamically finds a number input field based on its wrapper text."""
        wrapper = self.page.locator("div.field-wrapper").filter(has_text=visible_label_text)
        return wrapper.locator("input[type='number'], input[type='text']")

    # --- Field Interactions ---
    def enter_input_value(self, label_name: str, value: str):
        """Enters a value into any target number field by its visible label text."""
        input_el = self._get_number_input(label_name)
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))       
        input_el.blur()