import pytest
from typing import Any
from playwright.sync_api import expect
from tests.data.test_data import MapData
from pages.configuration_map_page import  MapPage

# Pass the imported list directly into parametrize!
@pytest.mark.parametrize("value, is_valid, expected_error", MapData.HIGH_PROXIMITY_THRESHOLD_DATA)
def test_higher_proximity_threshold_boundaries(map_setup: MapPage, value: Any, is_valid: Any, expected_error: Any):
    map_page: MapPage = map_setup

    map_page.click_edit()
    map_page.enter_high_proximity_threshold(value)
    
    try:
        if is_valid:
           expect(map_page.save_button).to_be_enabled()
           map_page.save_changes()
           expect(map_page.edit_button).to_be_visible()
        else:
           error_locator = map_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           map_page.click_dismiss()
           expect(map_page.edit_button).to_be_visible()
           
    finally:
       if map_page.dismiss_button.is_visible():
            map_page.click_dismiss()
       expect(map_page.edit_button).to_be_visible()


@pytest.mark.parametrize("value, is_valid, expected_error", MapData.HIGHER_CONFIDENCE_THRESHOLD_DATA)
def test_higher_confidence_threshold_boundaries(map_setup: MapPage, value: Any, is_valid: Any, expected_error: Any) -> None:
    map_page: MapPage = map_setup

    map_page.click_edit()
    map_page.enter_higher_confidence_threshold(value)

    try:
        if is_valid:
           expect(map_page.save_button).to_be_enabled()
           map_page.save_changes()
           expect(map_page.edit_button).to_be_visible()
        else:
           error_locator = map_page.get_error_message(expected_error)
           expect(error_locator).to_be_visible()
           map_page.click_dismiss()
           expect(map_page.edit_button).to_be_visible()
           
    finally:
        if map_page.dismiss_button.is_visible():
            map_page.click_dismiss()
        expect(map_page.edit_button).to_be_visible()

def test_map_toggles(map_setup: MapPage) -> None:
    map_page: MapPage = map_setup

    map_page.click_edit()

    try:
        # Pulling the toggles list dynamically from your test data file
        for toggle in MapData.MAP_TOGGLES:
            map_page.double_click_toggle(toggle)
            map_page.page.wait_for_timeout(500) # Replicating the stability pause from your script
        
        # Dismiss changes to reset state for subsequent tests
        map_page.click_dismiss()
        expect(map_page.edit_button).to_be_visible()
        
    finally:
        if map_page.dismiss_button.is_visible():
            map_page.click_dismiss()
        expect(map_page.edit_button).to_be_visible()
