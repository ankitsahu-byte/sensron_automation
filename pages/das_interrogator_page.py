class DasInterrogatorPage:
    def __init__(self, page):
        self.page = page
        
        # --- Core Navigation & Action Buttons ---
        self.das_radio_tab = page.get_by_role("radio", name="DAS Interrogator")
        self.edit_button = page.get_by_role("button", name="Edit")
        
        # Using a locator that matches 'Save Changes' (adjust if exact text varies)
        self.save_button = page.get_by_role("button", name=" Save Changes ")
        self.dismiss_button = page.get_by_role("button", name="Dismiss Changes")

    # --- Core Actions ---
    def open_das_interrogator(self):
        """Navigates to the DAS Interrogator sub-tab."""
        self.das_radio_tab.click()

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

    def get_error_message(self, expected_text: str):
        """Returns a locator for a specific error message text."""
        return self.page.get_by_text(expected_text, exact=False)


    # --- 🌟 THE MAGIC HELPER METHOD 🌟 ---
    def _get_number_input(self, visible_label_text: str):
        """
        Dynamically finds any Angular Material number input based on its visible label.
        This prevents dynamic ID failures and keeps the code DRY (Don't Repeat Yourself).
        """
        wrapper = self.page.locator("div.field-wrapper").filter(has_text=visible_label_text)
        return wrapper.locator("input[type='number']")


    # --- Field Interactions ---
    
    # 1. Pulse EDFA
    def enter_pulse_edfa_current(self, value: str):
        input_el = self._get_number_input("Pulse EDFA Current Reading Value")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))       
        input_el.blur()  # Triggers UI validation

    def get_pulse_edfa_value(self) -> str:
        return self._get_number_input("Pulse EDFA Current Reading Value").input_value()

    # 2. Pulse Frequency 
    def enter_voa_voltage(self, value: str):
        input_el = self._get_number_input("VOA Voltage Value")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))
        input_el.blur()

    # 3. Pulse Width 
    def enter_pulse_width(self, value: str):
        input_el = self._get_number_input("Pulse Width")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))
        input_el.blur()
        
    # 4. Resolution 
    def enter_pulse_frequency(self, value: str):
        input_el = self._get_number_input("Pulse Frequency")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(str(value))
        input_el.blur()
    
    # 5. Sample Number
    def enter_sample_number(self, value: str):
        input_el = self._get_number_input("Sample Number")
        input_el.wait_for(state="visible")
        input_el.click()
        input_el.clear()
        input_el.fill(value)
        input_el.blur()

    