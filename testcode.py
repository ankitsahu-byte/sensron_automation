import pytest
from playwright.sync_api import Page, sync_playwright, expect
import time
import os

BASE_URL = "http://10.101.54.90:4200/home/dashboard"
EMAIL = "ankit.sahu@stltech.in"
PASSWORD = "#Ankit@1234"

def get_input_locator(page: Page, visible_label_text: str):
    """Helper function to locate input fields robustly using field wrappers."""
    wrapper = page.locator("div.field-wrapper").filter(has_text=visible_label_text)
    return wrapper.locator("input[type='number'], input[type='text']")

def run_tests():
    # --- SETUP ARTIFACT FOLDER ---
    # Define the path for the artifact folder in the current working directory
    artifact_dir = os.path.join(os.getcwd(), "artifact")
    
    # Create the folder if it does not exist (exist_ok=True prevents errors if it's already there)
    os.makedirs(artifact_dir, exist_ok=True)
    print(f"Artifact folder ready at: {artifact_dir}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        print("Title:", page.title())

        # Enter credentials
        page.get_by_placeholder("Enter Email").fill(EMAIL)
        page.get_by_placeholder("Enter password").fill(PASSWORD)

        # Submit form
        page.get_by_role("button", name="Sign In").click()

        # Check login is successful
        page.wait_for_url(lambda url: "dashboard" in url, timeout=5000)
        assert "dashboard" in page.url, "Failed: Expected to be on dashboard, but URL is incorrect."
        print("Login successful.")
        
        # Click the configuration link
        page.get_by_role("link", name="Configuration").click()
        time.sleep(1)

        # Click the Log Configuration link
        page.get_by_role("radio", name="Log Configuration").click()
        time.sleep(1)

        # Define the tabs we want to iterate through
        tabs = ["DAS", "DAQ", "Alarm", "Anomaly"]

        for tab in tabs:
            print(f"\n--- Processing Tab: {tab} ---")
            
            # 1. Click the specific tab
            if tab == "Anomaly":
                tab_locator = page.get_by_label("Log Config Tabs").get_by_role("radio", name=tab)
            else:
                tab_locator = page.get_by_role("radio", name=tab, exact=True)
            
            tab_locator.click()
            expect(tab_locator).to_be_visible()
            print(f"{tab} Config tab is clicked.")
            time.sleep(1) 

            # --- 2. VALIDATE EDIT FUNCTIONALITY ---
            print(f"[{tab}] Validating Edit button...")
            
            # Use the new robust locator strategy
            file_size_input = get_input_locator(page, "File Size")
            duration_input = get_input_locator(page, "Duration Count")
            
            # Ensure fields are locked before clicking edit
            expect(file_size_input).to_be_hidden()
            expect(duration_input).to_be_hidden()

            
            # Click the Edit button
            page.get_by_role("button", name="Edit").click()
            time.sleep(0.5)
            
            # Ensure fields are now unlocked and editable
            expect(file_size_input).to_be_enabled()
            expect(duration_input).to_be_enabled()
            print(f"[{tab}] Edit validation passed! Fields are now editable.")
            page.get_by_role("button", name="Dismiss Changes").click()
            time.sleep(1)

            # --- 3. VALIDATE DOWNLOAD FUNCTIONALITY ---
            print(f"[{tab}] Validating Download...")
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Download").click()
                
            download = download_info.value
            file_name = download.suggested_filename
            print(f"[{tab}] Download triggered. Suggested filename: {file_name}")
            
            assert file_name is not None, f"Failed: No filename suggested for {tab}."
            
            # --- SAVE TO ARTIFACT FOLDER ---
            # Update the download path to use the artifact_dir created earlier
            download_path = os.path.join(artifact_dir, f"{tab}_{file_name}")
            download.save_as(download_path)
            
            assert os.path.exists(download_path), f"Failed: File not found at {download_path}."
            file_size = os.path.getsize(download_path)
            assert file_size > 0, f"Failed: Downloaded file for {tab} is empty (0 bytes)."
            
            print(f"[{tab}] Download validated successfully! Saved to: {download_path}")
        
        print("\nAll tabs processed successfully.")
        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    run_tests()