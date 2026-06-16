import pytest
from typing import Any
from playwright.sync_api import expect
from tests.data.test_data import DasInterrogatorData
from pages.das_interrogator_page import DasInterrogatorPage  # <-- Import your data

# Pass the imported list directly into parametrize!
@pytest.mark.parametrize("value, is_valid, expected_error", DasInterrogatorData.EDFA_BOUNDARIES)
def test_edfa_current_enforces_min_max_boundaries(das_interrogator_setup: DasInterrogatorPage, value: Any, is_valid: Any, expected_error: Any):
    das_page: DasInterrogatorPage = das_interrogator_setup

    das_page.click_edit()
    das_page.enter_pulse_edfa_current(value)
    try:
        if is_valid:
           expect(das_page.save_button).to_be_enabled()
           das_page.save_changes()
           expect(das_page.edit_button).to_be_visible()
        else:
           das_page.save_changes()
           expect(das_page.save_button).to_be_disabled()
           das_page.force_save_changes()
        
           error_locator = das_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
    finally:
        if das_page.dismiss_button.is_visible():
            das_page.click_dismiss()
        expect(das_page.edit_button).to_be_visible()

# Do the exact same for the next test
@pytest.mark.parametrize("value, is_valid, expected_error", DasInterrogatorData.VOA_BOUNDARIES)
def test_voa_voltage_rejects_values_outside_hardware_limits(das_interrogator_setup: DasInterrogatorPage, value: Any, is_valid: Any, expected_error: Any):
    das_page: DasInterrogatorPage = das_interrogator_setup

    das_page.click_edit()
    das_page.enter_voa_voltage(value)

    try:
        if is_valid:
           expect(das_page.save_button).to_be_enabled()
           das_page.save_changes()
           expect(das_page.edit_button).to_be_visible()
        else:
           das_page.save_changes()
           expect(das_page.save_button).to_be_disabled()
           das_page.force_save_changes()
        
           error_locator = das_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
    finally:
        if das_page.dismiss_button.is_visible():
            das_page.click_dismiss()
        expect(das_page.edit_button).to_be_visible()

# Do the exact same for the next test
@pytest.mark.parametrize("value, is_valid, expected_error", DasInterrogatorData.DAQ_PULSE_BOUNDARIES)
def test_pulse_width_boundary_validation(das_interrogator_setup: DasInterrogatorPage, value: Any, is_valid: Any, expected_error: Any):
    # ... logic stays exactly the same ...
    das_page: DasInterrogatorPage = das_interrogator_setup

    das_page.click_edit()
    das_page.enter_pulse_width(value)

    try:
        if is_valid:
           expect(das_page.save_button).to_be_enabled()
           das_page.save_changes()
           expect(das_page.edit_button).to_be_visible()
        else:
           das_page.save_changes()
           expect(das_page.save_button).to_be_disabled()
           das_page.force_save_changes()
        
           error_locator = das_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
    finally:
        if das_page.dismiss_button.is_visible():
            das_page.click_dismiss()
        expect(das_page.edit_button).to_be_visible()

# Do the exact same for the next test
@pytest.mark.parametrize("value, is_valid, expected_error", DasInterrogatorData.DAQ_PULSE_FREQUENCY)
def test_pulse_frequency_accepts_only_valid_ranges(das_interrogator_setup: DasInterrogatorPage, value: Any, is_valid: Any, expected_error: Any):
    # ... logic stays exactly the same ...
    das_page: DasInterrogatorPage = das_interrogator_setup

    das_page.click_edit()
    das_page.enter_pulse_frequency(value)

    try:
        if is_valid:
           expect(das_page.save_button).to_be_enabled()
           das_page.save_changes()
           expect(das_page.edit_button).to_be_visible()
        else:
           das_page.save_changes()
           expect(das_page.save_button).to_be_disabled()
           das_page.force_save_changes()
        
           error_locator = das_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
    finally:
        if das_page.dismiss_button.is_visible():
            das_page.click_dismiss()
        expect(das_page.edit_button).to_be_visible()


@pytest.mark.parametrize("value, is_valid, expected_error", DasInterrogatorData.DAQ_SAMPLE_NUMBER)
def test_sample_number_accepts_only_valid_ranges(das_interrogator_setup: DasInterrogatorPage, value: Any, is_valid: Any, expected_error: Any):
    das_page: DasInterrogatorPage = das_interrogator_setup

    das_page.click_edit()
    das_page.enter_sample_number(value)

    try:
        if is_valid:
           expect(das_page.save_button).to_be_enabled()
           das_page.save_changes()
           expect(das_page.edit_button).to_be_visible()
        else:
           das_page.save_changes()
           expect(das_page.save_button).to_be_disabled()
           das_page.force_save_changes()
        
           error_locator = das_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
    finally:
        if das_page.dismiss_button.is_visible():
            das_page.click_dismiss()
        expect(das_page.edit_button).to_be_visible()

@pytest.mark.parametrize("value, is_valid, expected_error", DasInterrogatorData.DAQ_PULSE_NUMBER)
def test_pulse_number_accepts_only_valid_ranges(das_interrogator_setup: DasInterrogatorPage, value: Any, is_valid: Any, expected_error: Any):
    das_page: DasInterrogatorPage = das_interrogator_setup

    das_page.click_edit()
    das_page.enter_pulse_number(value)
    try:
        if is_valid:
           expect(das_page.save_button).to_be_enabled()
           das_page.save_changes()
           expect(das_page.edit_button).to_be_visible()
        else:
           das_page.save_changes()
           expect(das_page.save_button).to_be_disabled()
           das_page.force_save_changes()
        
           error_locator = das_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
    finally:
        if das_page.dismiss_button.is_visible():
            das_page.click_dismiss()
        expect(das_page.edit_button).to_be_visible()