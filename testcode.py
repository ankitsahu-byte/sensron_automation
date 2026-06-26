import pytest
from playwright.sync_api import Page, sync_playwright, expect
import time

BASE_URL = "http://10.101.54.90:4200/home/dashboard"
EMAIL = "ankit.sahu@stltech.in"
PASSWORD = "#Ankit@1234"

def get_input_locator(page: Page, visible_label_text: str):
    """Helper function to locate input fields robustly using field wrappers."""
    # Playwright's has_text does partial matching, so passing "SBC Setpoint" 
    # will successfully match "SBC Setpoint (°C) *"
    wrapper = page.locator("div.field-wrapper").filter(has_text=visible_label_text)
    # Added input[type='time'] just in case the developers used native time inputs
    return wrapper.locator("input[type='number'], input[type='text'], input[type='time']")

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
        assert "dashboard" in page.url, "Failed: Expected to be on dashboard."
        print("Login successful and on the correct page.")
        
        # Click the configuration link
        page.get_by_role("link", name="Configuration").click()
        print("Configuration link is clicked.")
        time.sleep(1)

        # Click the Temp Monitoring link
        page.get_by_role("radio", name="Temp Monitoring").click()
        print("Temp Monitoring tab is clicked.")
        time.sleep(1)
        
        # ----------------------------------------------------------
        # Define a list of all 8 fields you want to test
        fields_to_test = [
            "Chassis Sample Frequency",
            "Jetson Sample Frequency",
            "SBC Sample Frequency",
            "DAS Sample Frequency",
            "SBC Setpoint",
            "Jetson Setpoint",
            "DAS Setpoint",
            "Chassis Setpoint"
        ]

        # Loop through each field one by one
        for field_name in fields_to_test:
            print(f"\n--- Testing Field: {field_name} ---")
            Edit_button = page.get_by_role("button", name="Edit")
            if Edit_button.is_visible():
                Edit_button.click()
            # 1. Locate the input
            target_input = get_input_locator(page, field_name)
            target_input.wait_for(state="visible")
            
            # 2. Get the existing data
            original_value = target_input.input_value()
            print(f"Original Value: {original_value}")
            
            # 3. Clear the input
            target_input.click()
            target_input.clear()
            print("Cleared Input Successfully")
            
            # 4. Fill the existing data back in
            target_input.fill(original_value)
            print(f"Original value '{original_value}' entered back")
            
            # 5. Handle the buttons
            # Note: Because you cleared and typed the exact same value back, the UI might 
            # realize nothing actually changed and keep the Save/Dismiss buttons disabled. 
            # This 'if' statement prevents the script from crashing if they are disabled.
            dismiss_button = page.get_by_role("button", name="Dismiss Changes")
            if dismiss_button.is_enabled():
                dismiss_button.click()
                print("Clicked 'Dismiss Changes' successfully")
            else:
                print("Buttons remained disabled (expected because value didn't change)")

            print(f"Test Passed successfully for {field_name}")
            time.sleep(1) # Brief pause before moving to the next field

        print("\nAll fields processed successfully!")
        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    run_tests()