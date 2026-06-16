import pytest
from playwright.sync_api import Page, sync_playwright, expect

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

        # Click the DAS Interrogator radio option
        page.get_by_role("radio", name="DAS Interrogator").click()
        print("DAS Interrogator link is clicked.")       
#--------------------------------------------------------------------------

        # EDFA Details check the boundary values of Pulse EDFA Current reading value(mA)
        boundary_test_cases = [
          ("-1", False, "Pulse EDFA Current Reading must be at least 0 mA"), 
          ("0", True, None),      
          ("110", True, None),    
          #("1800", True, None),   
          ("1801", False, "Pulse EDFA Current Reading must not exceed 1800 mA")
        ]

        # Loop through the cases testing each boundary completely
        for value, is_valid, expected_error in boundary_test_cases:
            print(f"\n--- Testing boundary value: {value} ---")
            
            # 1. Start the cycle: Click Edit
            edit_button = page.get_by_role("button", name="Edit")
            edit_button.click()
            
            # 2. Locate the input using your custom wrapper method
            edfa_wrapper = page.locator("div.field-wrapper").filter(has_text="Pulse EDFA Current Reading Value")
            pulse_edfa_input = edfa_wrapper.locator("input[type='number']")
            
            # Wait for the input to actually be visible and ready before typing
            pulse_edfa_input.wait_for(state="visible")
            
            # 3. Fill the value and trigger validation
            pulse_edfa_input.click()
            pulse_edfa_input.clear()
            pulse_edfa_input.fill(value)
            pulse_edfa_input.blur() # Click away to trigger error messages
            
            # 4. Locate the Save button 
            save_button = page.get_by_role("button", name="Save Changes")
            
            # 5. Assertions using auto-retrying EXPECT instead of hard ASSERTS
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                # Check it is enabled, then click it
                expect(save_button).to_be_enabled()
                save_button.click()
                # Safety Buffer: Wait for the save to finish and the Edit button to return
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted. Saved successfully.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                
                # Check it is disabled, then forcefully try to click it
                save_button.click()
                expect(save_button).to_be_disabled()
                
                # Verify the specific red error message appears based on our data table
                error_msg = page.get_by_text(expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                # Click Dismiss Changes to throw away the bad data
                page.get_by_role("button", name="Dismiss Changes").click()
                
                # Safety Buffer: Wait for the Edit button to return before looping
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")
#-------------------------------------------------------------------------------------------------
       ''' # VOA Detaisls
        boundary_test_cases = [
          ("-1", False, "VOA Voltage Value must be at least 0 V"), 
          ("0", True, None),                                            
          ("2000", True, None),                                         
          #("4000", True, None),                                         
          ("4001", False, "VOA Voltage Value must not exceed 4000 V")
        ]

        # Loop through the cases testing each boundary completely
        for value, is_valid, expected_error in boundary_test_cases:
            print(f"\n--- Testing boundary value: {value} ---")
            
            # 1. Start the cycle: Click Edit
            edit_button = page.get_by_role("button", name="Edit")
            edit_button.click()
            
            # 2. Locate the input using your custom wrapper method
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="VOA Voltage Value")
            target_input = target_wrapper.locator("input[type='number']")
            
            # Wait for the input to actually be visible and ready before typing
            target_input.wait_for(state="visible")
            
            # 3. Fill the value and trigger validation
            target_input.click()
            target_input.clear()
            target_input.fill(value)
            target_input.blur() # Click away to trigger error messages
            
            # 4. Locate the Save button 
            save_button = page.get_by_role("button", name="Save Changes")
            
            # 5. Assertions using auto-retrying EXPECT instead of hard ASSERTS
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                # Check it is enabled, then click it
                expect(save_button).to_be_enabled()
                save_button.click()
                # Safety Buffer: Wait for the save to finish and the Edit button to return
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted. Saved successfully.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                
                # Check it is disabled, then forcefully try to click it
                save_button.click()
                expect(save_button).to_be_disabled()
                
                # Verify the specific red error message appears based on our data table
                error_msg = page.get_by_text(expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                # Click Dismiss Changes to throw away the bad data
                page.get_by_role("button", name="Dismiss Changes").click()
                
                # Safety Buffer: Wait for the Edit button to return before looping
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")
        
#-----------------------------------------------------------------------------
        #
        boundary_test_cases = [
          ("49", False, "Pulse Width must be between 50 and 500 nanoseconds"),
          ("50", True, None),
          #("250", True, None),
          #("500", True, None),
          ("501", False, "Pulse Width must be between 50 and 500 nanoseconds")
        ]

        # Loop through the cases testing each boundary completely
        for value, is_valid, expected_error in boundary_test_cases:
            print(f"\n--- Testing boundary value: {value} ---")
            
            # 1. Start the cycle: Click Edit
            edit_button = page.get_by_role("button", name="Edit")
            edit_button.click()
            
            # 2. Locate the input using your custom wrapper method
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Pulse Width")
            target_input = target_wrapper.locator("input[type='number']")
            
            # Wait for the input to actually be visible and ready before typing
            target_input.wait_for(state="visible")
            
            # 3. Fill the value and trigger validation
            target_input.click()
            target_input.clear()
            target_input.fill(value)
            target_input.blur() # Click away to trigger error messages
            
            # 4. Locate the Save button 
            save_button = page.get_by_role("button", name="Save Changes")
            
            # 5. Assertions using auto-retrying EXPECT instead of hard ASSERTS
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                # Check it is enabled, then click it
                expect(save_button).to_be_enabled()
                save_button.click()
                # Safety Buffer: Wait for the save to finish and the Edit button to return
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted. Saved successfully.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                
                # Check it is disabled, then forcefully try to click it
                save_button.click()
                expect(save_button).to_be_disabled()
                
                # Verify the specific red error message appears based on our data table
                error_msg = page.get_by_text(expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                # Click Dismiss Changes to throw away the bad data
                page.get_by_role("button", name="Dismiss Changes").click()
                
                # Safety Buffer: Wait for the Edit button to return before looping
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")
#---------------------------------------------------------------------------------------
        boundary_test_cases = [
          ("-1", False, "Pulse Frequency must be between 100 and 100000 Hz"),
          #("0", True, None),#Pulse Frequency must be between 100 and 100000 Hz
          ("1200", True, None),
          # ("2441.40625", True, None),#Pulse Frequency must be less than 2441.41 Hz for the current Resolution and Sample Number
          ("2442", False, "Pulse Frequency must be less than 2441.41 Hz for the current Resolution and Sample Number")
        ]
        # Loop through the cases testing each boundary completely
        for value, is_valid, expected_error in boundary_test_cases:
            print(f"Setti\--- Testing boundary value: {value} ---")
            
            # 1. Start the cycle: Click Edit
            edit_button = page.get_by_role("button", name="Edit")
            edit_button.click()
            
            # 2. Locate the input using your custom wrapper method
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Pulse Frequency")
            target_input = target_wrapper.locator("input[type='number']")
            
            # Wait for the input to actually be visible and ready before typing
            target_input.wait_for(state="visible")
            
            # 3. Fill the value and trigger validation
            target_input.click()
            target_input.clear()
            target_input.fill(value)
            target_input.blur() # Click away to trigger error messages
            
            # 4. Locate the Save button 
            save_button = page.get_by_role("button", name="Save Changes")
            
            # 5. Assertions using auto-retrying EXPECT instead of hard ASSERTS
            if is_valid:
                print(f"Valid value '{value}' entered. Executing TRUE flow.")
                # Check it is enabled, then click it
                expect(save_button).to_be_enabled()
                save_button.click()
                # Safety Buffer: Wait for the save to finish and the Edit button to return
                expect(edit_button).to_be_visible()
                print(f"Passed: Valid input '{value}' is accepted. Saved successfully.")
            else:
                print(f"Invalid value '{value}' entered. Executing FALSE flow.")
                
                # Check it is disabled, then forcefully try to click it
                save_button.click()
                expect(save_button).to_be_disabled()
                
                # Verify the specific red error message appears based on our data table
                error_msg = page.get_by_text(expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                # Click Dismiss Changes to throw away the bad data
                page.get_by_role("button", name="Dismiss Changes").click()
                
                # Safety Buffer: Wait for the Edit button to return before looping
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")'''
                      
# Keep this at the very bottom
if __name__ == "__main__":
    run_tests()