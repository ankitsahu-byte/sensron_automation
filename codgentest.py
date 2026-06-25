from playwright.sync_api import Page, sync_playwright, expect
import time
import os

BASE_URL = "http://10.101.54.90:4200/home/dashboard"
EMAIL = "ankit.sahu@stltech.in"
PASSWORD = "#Ankit@1234"

def run_tests():
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
        print("Login successful and on the correct page.")
        
        # Click the configuration link
        page.get_by_role("link", name="Configuration").click()
        print("Configuration link is clicked.")
        time.sleep(1)

        # Click the Log Configuration link
        page.get_by_role("radio", name="Log Configuration").click()
        print("Log Configuration Config tab is clicked.")
        time.sleep(1)

        # --- CONSOLIDATED LOOP FOR ALL TABS ---
        # Define the tabs we want to iterate through
        tabs = ["DAS", "DAQ", "Alarm", "Anomaly"]

        for tab in tabs:
            print(f"\n--- Processing Tab: {tab} ---")
            
            # 1. Click the specific tab
            # We handle "Anomaly" slightly differently based on your original working code
            if tab == "Anomaly":
                tab_locator = page.get_by_label("Log Config Tabs").get_by_role("radio", name=tab)
            else:
                tab_locator = page.get_by_role("radio", name=tab, exact=True)
            
            tab_locator.click()
            expect(tab_locator).to_be_visible()
            print(f"{tab} Config tab is clicked.")
            time.sleep(1) # Allow page to render the new tab's data

            # 2. Trigger and validate the download inline
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Download").click()
                
            download = download_info.value
            file_name = download.suggested_filename
            print(f"[{tab}] Download triggered. Suggested filename: {file_name}")
            
            # Validate filename exists
            assert file_name is not None, f"Failed: No filename suggested for {tab}."
            
            # Save the file with a unique prefix (e.g., "DAS_config.json")
            download_path = os.path.join(os.getcwd(), f"{tab}_{file_name}")
            download.save_as(download_path)
            
            # Validate file existence and size
            assert os.path.exists(download_path), f"Failed: File not found at {download_path}."
            file_size = os.path.getsize(download_path)
            assert file_size > 0, f"Failed: Downloaded file for {tab} is empty (0 bytes)."
            
            print(f"[{tab}] Download validated successfully! Saved to: {download_path} ({file_size} bytes)")
        
        # End of loop
        print("\nAll tabs processed successfully.")
        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    run_tests()