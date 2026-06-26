import pytest
from playwright.sync_api import expect
from tests.data.test_data import TempMonitoringData
from pages.configuration_temp_monitering_page import TempMonitoringPage

@pytest.mark.parametrize("field_name", TempMonitoringData.FIELDS_TO_TEST)
def test_temp_monitoring_fields_read_write(temp_monitoring_setup: TempMonitoringPage, field_name: str):
    temp_page: TempMonitoringPage = temp_monitoring_setup

    # Ensure we are in edit mode
    if temp_page.edit_button.is_visible():
        temp_page.click_edit()

    # 1. Get the existing data from the UI
    original_value = temp_page.get_field_value(field_name)
    
    # 2. Clear the input and fill the original data back in
    temp_page.fill_field_value(field_name, original_value)
    
    # 3. Handle the buttons
    # Note: Because you cleared and typed the exact same value back, the UI might 
    # realize nothing actually changed and keep the Save/Dismiss buttons disabled. 
    try:
        if temp_page.dismiss_button.is_enabled():
            temp_page.click_dismiss()
    finally:
        # Fallback to ensure we are out of edit mode if something failed
        if temp_page.dismiss_button.is_visible() and temp_page.dismiss_button.is_enabled():
             temp_page.click_dismiss()
             
    # Verify the state has returned to normal
    expect(temp_page.edit_button).to_be_visible()