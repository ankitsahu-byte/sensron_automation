class RbacPage:
    def __init__(self, page):
        self.page = page
        
        # --- Core Navigation & Action Buttons ---
        self.rbac_radio_tab = page.get_by_role("radio", name="RBAC Control", exact=True)
        self.edit_button = page.get_by_role("button", name="Edit")
        self.save_button = page.get_by_role("button", name="Save Changes")
        self.dismiss_button = page.get_by_role("button", name="Dismiss Changes")

    # --- Core Actions ---
    def open_rbac(self):
        """Navigates to the RBAC Control sub-tab."""
        self.rbac_radio_tab.click()

    def click_edit(self):
        self.edit_button.click()

    def save_changes(self):
        self.save_button.click()

    def click_dismiss(self):
        self.dismiss_button.click()

    def get_error_message(self, expected_error: str):
        return self.page.locator("div.field-error-message").filter(has_text=expected_error)

    # --- Helper Methods ---
    def _get_number_input(self, visible_label_text: str):
        """Dynamically finds a number input based on its wrapper label."""
        wrapper = self.page.locator("div.field-wrapper").filter(has_text=visible_label_text)
        return wrapper.locator("input[type='number'], input[type='text']")

    def _get_toggle(self, visible_label_text: str):
        """Dynamically finds a toggle switch based on its wrapper label."""
        wrapper = self.page.locator("div.toggle-field-wrapper").filter(has_text=visible_label_text)
        return wrapper.locator("button[role='switch']")

    # --- Field Interactions ---
    def enter_session_time(self, value: str):
        """Enters a value into the Session Time field."""
        input_el = self._get_number_input("Session Time (minutes)")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))       
        input_el.blur()
        
    def double_click_toggle(self, toggle_name: str):
        """Locates the specific toggle and double clicks it."""
        toggle = self._get_toggle(toggle_name)
        toggle.wait_for(state="visible")
        toggle.dblclick()