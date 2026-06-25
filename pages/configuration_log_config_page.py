import os

class LogConfigPage:
    def __init__(self, page):
        self.page = page
        
        # --- Core Navigation & Action Buttons ---
        self.log_config_radio = page.get_by_role("radio", name="Log Configuration", exact=True)
        
        self.edit_button = page.get_by_role("button", name="Edit")
        self.dismiss_button = page.get_by_role("button", name="Dismiss Changes")
        self.download_button = page.get_by_role("button", name="Download")

    # --- Core Actions ---
    def open_log_config(self):
        """Navigates to the Log Configuration sub-tab."""
        self.log_config_radio.scroll_into_view_if_needed()
        self.log_config_radio.click()

    def click_sub_tab(self, tab_name: str):
        """Clicks the specific sub-tab, handling the unique locator for 'Anomaly'."""
        if tab_name == "Anomaly":
            tab_locator = self.page.get_by_label("Log Config Tabs").get_by_role("radio", name=tab_name)
        else:
            tab_locator = self.page.get_by_role("radio", name=tab_name, exact=True)
        
        tab_locator.click()
        tab_locator.wait_for(state="visible")

    def click_edit(self):
        self.edit_button.click()

    def click_dismiss(self):
        self.dismiss_button.click()

    # --- Helper Methods ---
    def _get_input_locator(self, visible_label_text: str):
        """Helper function to locate input fields robustly using field wrappers."""
        wrapper = self.page.locator("div.field-wrapper").filter(has_text=visible_label_text)
        return wrapper.locator("input[type='number'], input[type='text']")

    def get_file_size_input(self):
        return self._get_input_locator("File Size")
        
    def get_duration_count_input(self):
        return self._get_input_locator("Duration Count")

    # --- Download Handling ---
    def download_file(self, artifact_dir: str, tab_name: str) -> str:
        """Triggers the download, saves it to the artifact directory, and returns the path."""
        with self.page.expect_download() as download_info:
            self.download_button.click()
            
        download = download_info.value
        file_name = download.suggested_filename
        
        # Ensure artifact directory exists
        os.makedirs(artifact_dir, exist_ok=True)
        
        download_path = os.path.join(artifact_dir, f"{tab_name}_{file_name}")
        download.save_as(download_path)
        
        return download_path