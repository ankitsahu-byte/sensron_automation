import pytest
import os
from playwright.sync_api import expect
from tests.data.test_data import LogConfigData
from pages.configuration_log_config_page import LogConfigPage


@pytest.mark.parametrize("tab_name", LogConfigData.TABS_TO_TEST)
def test_log_config_edit_and_download(log_config_setup: LogConfigPage, artifact_dir: str, tab_name: str):
    log_page: LogConfigPage = log_config_setup
    
    # 1. Navigate to the specific tab
    log_page.click_sub_tab(tab_name)
    
    # --- 2. VALIDATE EDIT FUNCTIONALITY ---
    file_size_input = log_page.get_file_size_input()
    duration_input = log_page.get_duration_count_input()
    
    # Ensure fields are hidden before clicking edit
    expect(file_size_input).to_be_hidden()
    expect(duration_input).to_be_hidden()
    
    # Click Edit and verify fields are unlocked
    log_page.click_edit()
    log_page.page.wait_for_timeout(500) # Replicating brief pause from your script
    
    expect(file_size_input).to_be_enabled()
    expect(duration_input).to_be_enabled()
    
    # Dismiss to reset state
    log_page.click_dismiss()
    expect(log_page.edit_button).to_be_visible()
    
    # --- 3. VALIDATE DOWNLOAD FUNCTIONALITY ---
    download_path = log_page.download_file(artifact_dir, tab_name)
    
    assert os.path.exists(download_path), f"Failed: File not found at {download_path}."
    file_size = os.path.getsize(download_path)
    assert file_size > 0, f"Failed: Downloaded file for {tab_name} is empty (0 bytes)."