import pytest
from typing import Any
from playwright.sync_api import expect
from tests.data.test_data import LoggerData
from pages.configuration_logger_config_page import LoggerPage


# Reusable validation helper to keep tests DRY
def validate_form_submission(log_page: LoggerPage, is_valid: bool, expected_error: str):
    """Handles the standard save/dismiss logic and assertions."""
    try:
        if is_valid:
           expect(log_page.save_button).to_be_enabled()
           log_page.save_changes()
           expect(log_page.edit_button).to_be_visible()
        else:
           error_locator = log_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           log_page.click_dismiss()
           expect(log_page.edit_button).to_be_visible()
    finally:
       if log_page.dismiss_button.is_visible():
            log_page.click_dismiss()
       expect(log_page.edit_button).to_be_visible()


@pytest.mark.parametrize("value, is_valid, expected_error", LoggerData.RETENTION_TIME_DATA)
def test_logger_retention_time_boundaries(logger_setup: LoggerPage, value: Any, is_valid: Any, expected_error: Any):
    log_page: LoggerPage = logger_setup

    log_page.click_edit()
    log_page.enter_logger_retention_time(value)
    
    # Execute standardized assertions
    validate_form_submission(log_page, is_valid, expected_error)


def test_logger_toggles(logger_setup: LoggerPage) -> None:
    log_page: LoggerPage= logger_setup

    log_page.click_edit()

    try:
        # Pulling the toggles list dynamically from test_data.py
        for toggle in LoggerData.LOGGER_TOGGLES:
            log_page.double_click_toggle(toggle)
            log_page.page.wait_for_timeout(500) # Brief pause for UI transition
        
        # Dismiss changes to reset state for subsequent tests
        log_page.click_dismiss()
        expect(log_page.edit_button).to_be_visible()
        
    finally:
        if log_page.dismiss_button.is_visible():
            log_page.click_dismiss()
        expect(log_page.edit_button).to_be_visible()