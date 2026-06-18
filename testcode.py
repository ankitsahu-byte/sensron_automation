import pytest
from playwright.sync_api import Page, sync_playwright, expect
import time
import re  # Added for dynamic placeholder matching

BASE_URL = "http://10.101.54.90:4200/home/dashboard"
EMAIL = "ankit.sahu@stltech.in"
PASSWORD = "#Ankit@1234"

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("Navigating to base URL...")
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

        # --- 1. NAVIGATE TO DATABASE TAB ---
        # Note: The UI has an asterisk "Database*" so we use a partial match locator
        page.get_by_role("radio", name="Database*").click()
        print("Database* link is clicked.")
        time.sleep(1)

        # --- 3. THE CONTINUOUS LOOP TEST LOGIC ---
        
        # Click Edit once to unlock the entire form
        edit_button = page.get_by_role("button", name="Edit")
        edit_button.click()
        print("Edit button is clicked. Form is unlocked.")
        
        # Define the fields and the exact error we expect to see
        fields_to_test = [
            ("Username", "Username is required"),
            ("Password", "Password is required"),
            ("Database", "Database is required"),
            #("Port", "Port is required"),
            ("Host", "Host is required"),
            ("postgres", "Dialect is required")
        ]

        save_button = page.get_by_role("button", name="Save Changes")
        dismiss_button = page.get_by_role("button", name="Dismiss Changes")

        # Start the loop
        for field_label, expected_error in fields_to_test:
            print(f"\n--- Testing Field: {field_label} ---")
            
            # UPDATED LOCATOR: Find the input by a partial match of its placeholder using Regex
            # This will match "Enter Username (e.g. Ravi Sharma)", "Enter Password", etc.
            input_box = page.get_by_placeholder(re.compile(field_label, re.IGNORECASE))
            input_box.wait_for(state="visible")
            
            # Step A: Get Original Value
            original_value = input_box.input_value()
            print(f"Original {field_label} value is: '{original_value}'")

            # Step B: Clear the input box
            print("Clearing field...")
            input_box.click()
            input_box.clear()
            input_box.blur() # Trigger Angular's validation

            # Step C: Verify Error Message Appears
            error_locator = page.get_by_text(expected_error)
            expect(error_locator).to_be_visible()
            print(f"SUCCESS: Error '{expected_error}' is visible.")

            # Step D: Verify Save Button is Disabled
            expect(save_button).to_be_disabled()
            print("SUCCESS: Save button is securely locked.")

            # Step E: Restore the Data
            print(f"Restoring {field_label} back to: '{original_value}'...")
            input_box.click()
            input_box.fill(original_value)
            input_box.blur()

            # Step F: Verify Recovery
            dismiss_button.click()
            expect(edit_button).to_be_enabled()
            edit_button.click()
            restoring_value = input_box.input_value()
            assert original_value == restoring_value,'Failed to resotre the original value'

            print("SUCCESS: Valid data restored. Save button is awake.")

        # Finally: Safely Dismiss
        print("\nAll fields tested successfully!")
        dismiss_button = page.get_by_role("button", name="Dismiss Changes")
        if dismiss_button.is_visible():
            dismiss_button.click()
            print("Test Complete. Changes Dismissed.")

# Keep this at the very bottom
if __name__ == "__main__":
    run_tests()