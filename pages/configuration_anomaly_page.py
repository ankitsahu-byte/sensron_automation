class AnomalyPage:
    def __init__(self, page):
        self.page = page
        
        # --- Core Navigation & Action Buttons ---
        self.amo_radio_tab = page.get_by_role("radio", name="Anomaly", exact=True)
        self.edit_button = page.get_by_role("button", name="Edit")
        
        # Using a locator that matches 'Save Changes' (adjust if exact text varies)
        self.save_button = page.get_by_role("button", name=" Save Changes ")
        self.dismiss_button = page.get_by_role("button", name="Dismiss Changes")

    # --- Core Actions ---
    def open_anomoly(self):
        """Navigates to the DAS Interrogator sub-tab."""
        self.amo_radio_tab.click()

    def click_edit(self):
        """Activates the form for editing."""
        self.edit_button.click()

    def save_changes(self):
        """Clicks the save button. Use force=True if testing disabled states."""
        self.save_button.click()
        
    def force_save_changes(self):
        """Bypasses Playwright's disabled-button protection for negative testing."""
        self.save_button.click(force=True)

    def click_dismiss(self):
        """Discards current changes and reverts the form."""
        self.dismiss_button.click()

    def get_error_message(self, expected_error: str):
        """Returns a locator for a specific error message text."""
        return self.page.locator("div.field-error-message").filter(has_text=expected_error)


    # --- 🌟 THE MAGIC HELPER METHOD 🌟 ---
    def _get_number_input(self, visible_label_text: str):
        """
        Dynamically finds any Angular Material number input based on its visible label.
        This prevents dynamic ID failures and keeps the code DRY (Don't Repeat Yourself).
        """
        wrapper = self. page.locator("div.field-wrapper").filter(has_text=visible_label_text)
        return wrapper.locator("input[type='number'], input[type='text']")


    # --- Field Interactions ---
    
    # 1. Location offset
    def enter_location_offset_values(self, value: str):
        input_el = self._get_number_input("Location offset")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))       
        input_el.blur()  # Triggers UI validation

    def get_pulse_edfa_value(self) -> str:
        return self._get_number_input("Location offset").input_value()

    # 2. Process anomaly interval
    def enter_porcess_anomaly_interval_values(self, value: str):
        input_el = self._get_number_input("Process anomaly interval")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))
        input_el.blur()

    # 3. Max anomaly limit
    def enter_max_anomaly_limit_values(self, value: str):
        input_el = self._get_number_input("Max anomaly limit")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))
        input_el.blur()
        
    # 4. System idle time threshold (s)
    def enter_system_idle_time_threshold_values(self, value: str):
        input_el = self._get_number_input("System idle time threshold (s)")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))
        input_el.blur()
    
    # 5. Auto-Ack Timeout (m)
    def enter_auto_ack_timeout_values(self, value: str):
        input_el = self._get_number_input("Auto-Ack Timeout (m)")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(value)
        input_el.blur()

