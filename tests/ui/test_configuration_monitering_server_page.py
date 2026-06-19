import pytest
from playwright.sync_api import expect
from tests.data.test_data import MoniteringServerData
from pages.configuration_monitering_server_page import MoniteringServerPage

# Import your AnomalyServerPage and AnomalyServerData classes here depending on your folder structure

def test_anomaly_server_fields_continuous_loop(monitering_server_setup: MoniteringServerPage):
    monitering_page = monitering_server_setup
    
    # 1. Enter edit mode to unlock the form
    monitering_page.click_edit()

    # 2. Start the Continuous Loop
    for field_placeholder, expected_error in MoniteringServerData.MONITERING_SERVER_DATA:

        # Locate the specific input box dynamically using the POM
        input_box = monitering_page.get_input_by_placeholder(field_placeholder)
        input_box.wait_for(state="visible")
        
        # Step A: Get Original Value
        original_value = input_box.input_value()

        # Step B: Clear the input box
        monitering_page.clear_field(input_box)

        # Step C: Verify Error Message Appears
        error_locator = monitering_page.get_error_message(expected_error)
        expect(error_locator).to_be_visible()

        # Step D: Verify Save Button is Disabled
        expect(monitering_page.save_button).to_be_disabled()

        # Step E: Restore the Data
        monitering_page.fill_field(input_box, original_value)

        # Step F: Verify Recovery via Dismiss & Re-Edit
        monitering_page.click_dismiss()
        expect(monitering_page.edit_button).to_be_enabled()
        
        # Re-open edit mode to check the value and prepare for the next loop iteration
        monitering_page.click_edit()
        
        restoring_value = input_box.input_value()
        assert original_value == restoring_value, f"Failed to restore the original value for {field_placeholder}"

    # 3. Final Cleanup
    if monitering_page.dismiss_button.is_visible():
        monitering_page.click_dismiss()