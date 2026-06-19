import pytest
from typing import Any
from playwright.sync_api import expect
from tests.data.test_data import AnomalyData
from pages.configuration_anomaly_page import  AnomalyPage # <-- Import your data

# Pass the imported list directly into parametrize!
@pytest.mark.parametrize("value, is_valid, expected_error", AnomalyData.LOCTION_OFFSET_DATA)
def test_location_offset_boundaries(anomaly_setup: AnomalyPage, value: Any, is_valid: Any, expected_error: Any):
    amo_page: AnomalyPage = anomaly_setup

    amo_page.click_edit()
    amo_page.enter_location_offset_values(value)
    try:
        if is_valid:
           expect(amo_page.save_button).to_be_enabled()
           amo_page.save_changes()
           expect(amo_page.edit_button).to_be_visible()
        else:
           error_locator = amo_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           amo_page.click_dismiss()
           expect(amo_page.edit_button).to_be_visible()
           

    finally:
       if amo_page.dismiss_button.is_visible():
            amo_page.click_dismiss()
       expect(amo_page.edit_button).to_be_visible()


# Do the exact same for the next test
@pytest.mark.parametrize("value, is_valid, expected_error", AnomalyData.PROCESS_ANOMALY_INTERVAL_DATA)
def test_process_anomaly_interval_data(anomaly_setup: AnomalyPage, value: Any, is_valid: Any, expected_error: Any) -> None:
    amo_page: AnomalyPage = anomaly_setup

    amo_page.click_edit()
    amo_page.enter_porcess_anomaly_interval_values(value)

    try:
        if is_valid:
           expect(amo_page.save_button).to_be_enabled()
           amo_page.save_changes()
           expect(amo_page.edit_button).to_be_visible()
        else:
           error_locator = amo_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           amo_page.click_dismiss()
           expect(amo_page.edit_button).to_be_visible()
    finally:
        if amo_page.dismiss_button.is_visible():
            amo_page.click_dismiss()
        expect(amo_page.edit_button).to_be_visible()


# Do the exact same for the next test
@pytest.mark.parametrize("value, is_valid, expected_error", AnomalyData.MAX_ANOMALY_LIMIT_DATA)
def test_max_anomaly_limit_ranges(anomaly_setup: AnomalyPage, value: Any, is_valid: Any, expected_error: Any):
    # ... logic stays exactly the same ...
    amo_page: AnomalyPage = anomaly_setup

    amo_page.click_edit()
    amo_page.enter_max_anomaly_limit_values(value)

    try:
        if is_valid:
           expect(amo_page.save_button).to_be_enabled()
           amo_page.save_changes()
           expect(amo_page.edit_button).to_be_visible()
        else:
           error_locator = amo_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           amo_page.click_dismiss()
           expect(amo_page.edit_button).to_be_visible()
    finally:
        if amo_page.dismiss_button.is_visible():
            amo_page.click_dismiss()
        expect(amo_page.edit_button).to_be_visible()

# Do the exact same for the next test
@pytest.mark.parametrize("value, is_valid, expected_error", AnomalyData.SYSTEM_IDLE_TIME_THRESOLD_DATA)
def test_system_idel_thresold_validation(anomaly_setup: AnomalyPage, value: Any, is_valid: Any, expected_error: Any):
    # ... logic stays exactly the same ...
    amo_page: AnomalyPage = anomaly_setup

    amo_page.click_edit()
    amo_page.enter_system_idle_time_threshold_values(value)

    try:
        if is_valid:
           expect(amo_page.save_button).to_be_enabled()
           amo_page.save_changes()
           expect(amo_page.edit_button).to_be_visible()
        else:
           error_locator = amo_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           amo_page.click_dismiss()
           expect(amo_page.edit_button).to_be_visible()
    finally:
        if amo_page.dismiss_button.is_visible():
            amo_page.click_dismiss()
        expect(amo_page.edit_button).to_be_visible()




@pytest.mark.parametrize("value, is_valid, expected_error", AnomalyData.AUOT_ACT_TIMEOUT_DATA)
def test_auto_act_timeout_ranges(anomaly_setup: AnomalyPage, value: Any, is_valid: Any, expected_error: Any):
    amo_page: AnomalyPage = anomaly_setup

    amo_page.click_edit()
    amo_page.enter_auto_ack_timeout_values(value)

    try:
        if is_valid:
           expect(amo_page.save_button).to_be_enabled()
           amo_page.save_changes()
           expect(amo_page.edit_button).to_be_visible()
        else:
           error_locator = amo_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           amo_page.click_dismiss()
           expect(amo_page.edit_button).to_be_visible()
    finally:
        if amo_page.dismiss_button.is_visible():
            amo_page.click_dismiss()
        expect(amo_page.edit_button).to_be_visible()


     