import pytest
from playwright.sync_api import Page, sync_playwright, expect
import time

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

        # Check login is successful by waiting for the dashboard URL
        page.wait_for_url(lambda url: "dashboard" in url, timeout=5000)
        assert "dashboard" in page.url, "Failed: Expected to be on dashboard, but URL is incorrect."
        print("Login successful and on the correct page.")
        
        # Click the configuration link
        page.get_by_role("link", name="Configuration").click()
        print("Configuration link is clicked.")
        time.sleep(1)

        # Click the Anomaly link (Adapted for the new page)
        page.get_by_role("radio", name="Temp Monitoring").click()
        print("Temp Monitoring tab is clicked.")
        time.sleep(1)
        #----------------------------------------------------------
        # Chassis Sample Frequency
        print(f"\n--- Testing Chassis Sample Frequency ---")
        edit_button = page.get_by_role("button", name="Edit")
        if edit_button.is_visible():
            edit_button.click()
            
            # Using your wrapper strategy adapted for the Anomaly page
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Chassis Sample Frequency")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            original_value = target_input.input_value()
            print(f"Original Value: {original_value}")
            target_input.click()
            target_input.clear()
            print("Clear Input Sucessfully")
            target_input.fill(original_value)
            print("Orginal value entered")
            dismis_butoon = page.get_by_role("button", name="Dismiss Changes")
            dismis_butoon.click()
            expect(edit_button).to_be_visible()
            print("Test Passed sucessfully")
            time.sleep(2)



            


# Keep this at the very bottom
if __name__ == "__main__":
    run_tests()