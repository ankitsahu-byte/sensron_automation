import pytest
from typing import Any
from playwright.sync_api import expect
from tests.data.test_data import RbacData
from pages.configuration_rbac_controllor import RbacPage


# Reusable validation helper to keep tests DRY
def validate_form_submission(rbac_page: RbacPage, is_valid: bool, expected_error: str):
    """Handles the standard save/dismiss logic and assertions."""
    try:
        if is_valid:
           expect(rbac_page.save_button).to_be_enabled()
           rbac_page.save_changes()
           expect(rbac_page.edit_button).to_be_visible()
        else:
           error_locator = rbac_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           rbac_page.click_dismiss()
           expect(rbac_page.edit_button).to_be_visible()
    finally:
       if rbac_page.dismiss_button.is_visible():
            rbac_page.click_dismiss()
       expect(rbac_page.edit_button).to_be_visible()


@pytest.mark.parametrize("value, is_valid, expected_error", RbacData.SESSION_TIME_DATA)
def test_session_time_boundaries(rbac_setup: RbacPage, value: Any, is_valid: Any, expected_error: Any):
    rbac_page: RbacPage = rbac_setup

    rbac_page.click_edit()
    rbac_page.enter_session_time(value)
    
    # Execute standardized assertions
    validate_form_submission(rbac_page, is_valid, expected_error)


def test_rbac_toggles(rbac_setup: RbacPage) -> None:
    rbac_page: RbacPage = rbac_setup

    rbac_page.click_edit()

    try:
        # Pulling the toggles list dynamically from test_data.py
        for toggle in RbacData.RBAC_TOGGLES:
            rbac_page.double_click_toggle(toggle)
            rbac_page.page.wait_for_timeout(500) # Brief pause for UI transition
        
        # Dismiss changes to reset state for subsequent tests
        rbac_page.click_dismiss()
        expect(rbac_page.edit_button).to_be_visible()
        
    finally:
        if rbac_page.dismiss_button.is_visible():
            rbac_page.click_dismiss()
        expect(rbac_page.edit_button).to_be_visible()