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
        page.get_by_role("radio", name="Anomaly", exact=True).click()
        print("Anomaly tab is clicked.")
        time.sleep(1)

#--------------------------------------------------------------------------
        # 1. Location offset [-40000 to 40000]
        # NOTE: Update the expected_error strings with the exact text your UI shows when it fails.
        location_offset_cases = [
          (-40001, False, "Value must be at least -40000"), 
          (-40000, True, None),          
          (40000, True, None),
          (0, True, None),
          (40001, False, "Value must be between -40000 and 40000")
        ]

        for value, is_valid, expected_error in location_offset_cases:
            print(f"\n--- Testing Location offset boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            # Using your wrapper strategy adapted for the Anomaly page
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Location offset")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            
            target_input.click()
            target_input.clear()
            target_input.fill(str(value))
            target_input.blur() 
            
            save_button = page.get_by_role("button", name="Save Changes")
            
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                expect(save_button).to_be_enabled()
                save_button.click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted. Saved successfully.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                #save_button.click()
                #expect(save_button).to_be_disabled()
                
                # Check for error message
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")

#-------------------------------------------------------------------------------------------------
     # 2. Process anomaly interval [1000 to 60000]
        process_interval_cases = [
          ("999", False, "Value must be at least 1000"), 
          ("1000", True, None),                                            
          ("30000", True, None),                                         
          ("60000", True, None),
          ("1300", True, None),                                        
          ("60001", False, "Value must be between 1000 and 60000")
        ]

        for value, is_valid, expected_error in process_interval_cases:
            print(f"\n--- Testing Process anomaly interval boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Process anomaly interval")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            
            target_input.click()
            target_input.clear()
            target_input.fill(value)
            target_input.blur() 
            
            save_button = page.get_by_role("button", name="Save Changes")
            
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                expect(save_button).to_be_enabled()
                save_button.click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected.")

#-----------------------------------------------------------------------------
        # 3. Max anomaly limit [10 to 1000]
        max_limit_cases = [
          ("9", False, "Value must be at least 10"),
          ("10", True, None),
          ("1000", True, None),
          ("1001", False, "Value must be between 10 and 1000")
        ]

        for value, is_valid, expected_error in max_limit_cases:
            print(f"\n--- Testing Max anomaly limit boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Max anomaly limit")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            
            target_input.click()
            target_input.clear()
            target_input.fill(value)
            target_input.blur()
            
            save_button = page.get_by_role("button", name="Save Changes")
            
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                expect(save_button).to_be_enabled()
                save_button.click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected.")
#-----------------------------------------------------------------------------
        # 4.  System idle time threshold (s)[1 to 300]
        idle_time_cases = [
          ("-1", False, "The Minimum value is greater than 1"),
          ("0", False, "The Minimum value is greater than 1"),
          ("300", True, None),
          ("1", True, None),
          ("301", False, "Value must be between 1 and 300")
        ]

        for value, is_valid, expected_error in idle_time_cases:
            print(f"\n--- Testing Max anomaly limit boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="System idle time threshold (s)")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            
            target_input.click()
            target_input.clear()
            target_input.fill(value)
            target_input.blur()
            
            save_button = page.get_by_role("button", name="Save Changes")
            
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                expect(save_button).to_be_enabled()
                save_button.click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected.")
#-----------------------------------------------------------------------------
        # 5. Auto-Ack Timeout (m) [1 to 1440]
        max_limit_cases = [
          ("0", False, "The Minimum value is greater than 1"),
          ("1440", True, None),
          ("10", True, None),
          ("1441", False, "Value must be between 1 and 1440")
        ]

        for value, is_valid, expected_error in max_limit_cases:
            print(f"\n--- Testing Max anomaly limit boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Auto-Ack Timeout (m)")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            
            target_input.click()
            target_input.clear()
            target_input.fill(value)
            target_input.blur()
            
            save_button = page.get_by_role("button", name="Save Changes")
            
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                expect(save_button).to_be_enabled()
                save_button.click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected.")
#-----------------------------------------------------------------------------
        # 3. Max anomaly limit [10 to 1000]
# Keep this at the very bottom
if __name__ == "__main__":
    run_tests()