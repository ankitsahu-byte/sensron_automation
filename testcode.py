import pytest
from playwright.sync_api import Page, sync_playwright, expect
import time
import pyotp

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
        page.get_by_role("radio", name="Jetson Device Config").click()
        print("Jetson Device Config tab is clicked.")
        time.sleep(1)
        #----------------------------------------------------------
        # Request Timeout (ms)
        REQUEST_TIMEOUT_DATA = [
          ("100", False, "Value must be at least 1000"),   
          ("999", False, "Value must be at least 1000"),   
          ("1000", True, None),                          
          ("60000", True, None),
          ("10000",True, None),                          
          ("60001", False, "Value must be between 1000 and 60000"),                        
          ("-1", False, "The Minimum value is greater than 1000")  
        ]
        for value, is_valid, expected_error in REQUEST_TIMEOUT_DATA:
            print(f"\n--- Testing Request Timeout (ms) boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            # Using your wrapper strategy adapted for the Anomaly page
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Request Timeout (ms)")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            
            target_input.click()
            target_input.clear()
            
            # NOTE: If you run into the "disabled" save button error again, 
            # change .fill() to .press_sequentially(str(value), delay=50)
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
                # Check for error message
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")
#---------------------------------------------------------------------------------------
        # Retry Delay (ms)
        RETRY_DELAY_DATA = [
          ("100", False, "Value must be at least 500"),   
          ("499", False, "Value must be at least 500"),   
          ("500", True, None),                          
          ("10000", True, None),
          ("1000",True, None),                          
          ("10001", False, "Value must be between 500 and 10000"),                        
          ("-1", False, "The Minimum value is greater than 500")  
        ]
        for value, is_valid, expected_error in RETRY_DELAY_DATA:
            print(f"\n--- Testing Retry Delay (ms) boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            # Using your wrapper strategy adapted for the Anomaly page
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Retry Delay (ms)")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            
            target_input.click()
            target_input.clear()
            
            # NOTE: If you run into the "disabled" save button error again, 
            # change .fill() to .press_sequentially(str(value), delay=50)
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
                # Check for error message
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")
#---------------------------------------------------------------------------------------
        # Max Retry Attempts
        MAX_RETRY_ATTEMPTS_DATA = [
          ("0", False, "The Minimum value is greater than 1"),   
          ("1", True, None),   
          ("10", True, None),                          
          ("3", True, None),                          
          ("11", False, "Value must be between 1 and 10"),                        
          ("-1", False, "The Minimum value is greater than 1")  
        ]
        for value, is_valid, expected_error in MAX_RETRY_ATTEMPTS_DATA:
            print(f"\n--- Testing Max Retry Attempts boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            # Using your wrapper strategy adapted for the Anomaly page
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Max Retry Attempts")
            target_input = target_wrapper.locator("input[type='number'], input[type='text']")
            target_input.wait_for(state="visible")
            
            target_input.click()
            target_input.clear()
            
            # NOTE: If you run into the "disabled" save button error again, 
            # change .fill() to .press_sequentially(str(value), delay=50)
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
                # Check for error message
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")


if __name__ == "__main__":
    run_tests()