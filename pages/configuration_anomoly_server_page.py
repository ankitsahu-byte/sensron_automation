import re

class AnomalyServerPage:
    def __init__(self, page):
        self.page = page
        
        # Navigation
        self.anomaly_tab = page.get_by_role("radio", name="Anomaly Server*")
        
        # Buttons
        self.edit_button = page.get_by_role("button", name="Edit")
        self.save_button = page.get_by_role("button", name="Save Changes")
        self.dismiss_button = page.get_by_role("button", name="Dismiss Changes")

    def navigate_to_anomaly_server(self):
        self.anomaly_tab.click()

    def click_edit(self):
        self.edit_button.click()

    def click_dismiss(self):
        self.dismiss_button.click()

    def get_error_message(self, expected_text: str):
        return self.page.get_by_text(expected_text)

    # --- Regex Placeholder Methods ---
    def get_input_by_placeholder(self, field_placeholder: str):
        """Returns the input locator using a case-insensitive regex partial match."""
        return self.page.get_by_placeholder(re.compile(field_placeholder, re.IGNORECASE))

    def clear_field(self, input_locator):
        """Clicks, clears, and blurs the input to trigger validation."""
        input_locator.click()
        input_locator.clear()
        input_locator.blur()

    def fill_field(self, input_locator, value: str):
        """Clicks, fills, and blurs the input."""
        input_locator.click()
        input_locator.fill(str(value))
        input_locator.blur()