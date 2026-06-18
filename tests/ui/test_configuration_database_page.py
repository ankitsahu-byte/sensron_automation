import pytest
from playwright.sync_api import expect
from tests.data.test_data import DatabaseData
from pages.configuration_database_page import DatabasePage 

def test_database_fields_continuous_loop(database_setup: DatabasePage):
    db_page = database_setup
    
    # Optional: If your fixture doesn't already click the Database tab, do it here
    db_page.navigate_to_database()

    # 1. Enter edit mode to unlock the form
    db_page.click_edit()

    # 2. Start the Continuous Loop
    for field_placeholder, expected_error in DatabaseData.DATABASE_DATA:
        
        # Locate the specific input box dynamically
        input_box = db_page.get_input_by_placeholder(field_placeholder)
        input_box.wait_for(state="visible")
        
        # Step A: Get Original Value
        original_value = input_box.input_value()

        # Step B: Clear the input box
        db_page.clear_field(input_box)

        # Step C: Verify Error Message Appears
        error_locator = db_page.get_error_message(expected_error)
        expect(error_locator).to_be_visible()

        # Step D: Verify Save Button is Disabled
        expect(db_page.save_button).to_be_disabled()

        # Step E: Restore the Data
        db_page.fill_field(input_box, original_value)

        # Step F: Verify Recovery via Dismiss & Re-Edit
        db_page.click_dismiss()
        expect(db_page.edit_button).to_be_enabled()
        
        # Re-open edit mode to check the value and prepare for the next loop iteration
        db_page.click_edit()
        
        restoring_value = input_box.input_value()
        assert original_value == restoring_value, f"Failed to restore the original value for {field_placeholder}"

    # 3. Final Cleanup
    if db_page.dismiss_button.is_visible():
        db_page.click_dismiss()