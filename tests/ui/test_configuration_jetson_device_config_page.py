import pytest
from typing import Any
from playwright.sync_api import expect
from tests.data.test_data import JetsonDeviceData
from pages.configuration_jetson_device_config_page import JetsonDevicePage




def validate_form_submission(jetson_page: JetsonDevicePage, is_valid: bool, expected_error: str):
    """Handles the unified form submission logic and error block validation state."""
    try:
        if is_valid:
            expect(jetson_page.save_button).to_be_enabled()
            jetson_page.save_changes()
            expect(jetson_page.edit_button).to_be_visible()
        else:
            error_locator = jetson_page.get_error_message(expected_error)
            expect(error_locator).to_be_visible()
            jetson_page.click_dismiss()
            expect(jetson_page.edit_button).to_be_visible()
    finally:
        if jetson_page.dismiss_button.is_visible():
            jetson_page.click_dismiss()
        expect(jetson_page.edit_button).to_be_visible()


@pytest.mark.parametrize("value, is_valid, expected_error", JetsonDeviceData.REQUEST_TIMEOUT_DATA)
def test_request_timeout_boundaries(jetson_setup: JetsonDevicePage, value: Any, is_valid: Any, expected_error: Any):
    jetson_page: JetsonDevicePage = jetson_setup

    if jetson_page.edit_button.is_visible():
        jetson_page.click_edit()
        
    jetson_page.enter_input_value("Request Timeout (ms)", value)
    validate_form_submission(jetson_page, is_valid, expected_error)


@pytest.mark.parametrize("value, is_valid, expected_error", JetsonDeviceData.RETRY_DELAY_DATA)
def test_retry_delay_boundaries(jetson_setup: JetsonDevicePage, value: Any, is_valid: Any, expected_error: Any):
    jetson_page: JetsonDevicePage = jetson_setup

    if jetson_page.edit_button.is_visible():
        jetson_page.click_edit()
        
    jetson_page.enter_input_value("Retry Delay (ms)", value)
    validate_form_submission(jetson_page, is_valid, expected_error)


@pytest.mark.parametrize("value, is_valid, expected_error", JetsonDeviceData.MAX_RETRY_ATTEMPTS_DATA)
def test_max_retry_attempts_boundaries(jetson_setup: JetsonDevicePage, value: Any, is_valid: Any, expected_error: Any):
    jetson_page: JetsonDevicePage = jetson_setup

    if jetson_page.edit_button.is_visible():
        jetson_page.click_edit()
        
    jetson_page.enter_input_value("Max Retry Attempts", value)
    validate_form_submission(jetson_page, is_valid, expected_error)