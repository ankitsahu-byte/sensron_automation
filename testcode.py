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
        page.get_by_role("radio", name="Map").click()
        print("Map tab is clicked.")
        time.sleep(1)
        #----------------------------------------------------------
        # High Proximity Threshold
        High_Proximity_Threshold = [
          (-1, False, "Value must be greater than or equal to 0"),        
          (1, True, None),
          (0,True, None)
        ]
        for value, is_valid, expected_error in High_Proximity_Threshold:
            print(f"\n--- Testing Location offset boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            # Using your wrapper strategy adapted for the Anomaly page
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="High Proximity Threshold")
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
        # Higher Confidence Threshold
        Higher_Confidence_Threshold = [
          (-1, False, "Value must be greater than or equal to 0"),        
          (1, True, None),
          (0,True, None)
        ]
        for value, is_valid, expected_error in Higher_Confidence_Threshold:
            print(f"\n--- Testing Location offset boundary value: {value} ---")
            
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
                edit_button.click()
            
            # Using your wrapper strategy adapted for the Anomaly page
            target_wrapper = page.locator("div.field-wrapper").filter(has_text="Higher Confidence Threshold")
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
                
                # Check for error message
                error_msg = page.locator("div.field-error-message").filter(has_text=expected_error)
                expect(error_msg).to_be_visible()
                print(f"Expected error caught: '{expected_error}'")
                
                page.get_by_role("button", name="Dismiss Changes").click()
                expect(edit_button).to_be_visible()
                print(f"Passed: Invalid input '{value}' is rejected. Changes dismissed.")

            #---------------------------------------------------------------------------------------
             # Map Configuration Toggles (Explicit Definitions)
            print("\n--- Testing Map Toggles ---")
        
        # Ensure we are in Edit mode before interacting with toggles
            edit_button = page.get_by_role("button", name="Edit")
            if edit_button.is_visible():
              edit_button.click()
            page.wait_for_timeout(500) # Brief pause for UI transition
        
        # 1. Enable Offline Map Toggle
            print("Interacting with toggle: Enable Offline Map")
            offline_wrapper = page.locator("div.toggle-field-wrapper").filter(has_text="Enable Offline Map")
            offline_map_toggle = offline_wrapper.locator("button[role='switch']")
        
        # Ensure it's ready before clicking
            offline_map_toggle.wait_for(state="visible")
            offline_map_toggle.dblclick()
            print("sucess")
# 2. Allow Look Forward Toggle
            print("Interacting with toggle: Allow Look Forward")
            look_forward_wrapper = page.locator("div.toggle-field-wrapper").filter(has_text="Allow Look Forward")
            look_forward_toggle = look_forward_wrapper.locator("button[role='switch']")
            
            look_forward_toggle.wait_for(state="visible")
            look_forward_toggle.dblclick()
            print("Allow Look Forward toggle success")
            page.wait_for_timeout(500) # Optional: slight pause for UI stability


            # 3. kilometer Marker Toggle
            # Note: Using exact case from your UI screenshot ("kilometer Marker")
            print("Interacting with toggle: kilometer Marker")
            kilometer_wrapper = page.locator("div.toggle-field-wrapper").filter(has_text="kilometer Marker")
            kilometer_toggle = kilometer_wrapper.locator("button[role='switch']")
            
            kilometer_toggle.wait_for(state="visible")
            kilometer_toggle.dblclick()
            print("kilometer Marker toggle success")
            page.wait_for_timeout(500)


            # 4. Merge Type Toggle
            print("Interacting with toggle: Merge Type")
            merge_type_wrapper = page.locator("div.toggle-field-wrapper").filter(has_text="Merge Type")
            merge_type_toggle = merge_type_wrapper.locator("button[role='switch']")
            
            merge_type_toggle.wait_for(state="visible")
            merge_type_toggle.dblclick()
            print("Merge Type toggle success")
            page.wait_for_timeout(500)


            # Finally, dismiss or save changes to reset state
            dismiss_btn = page.get_by_role("button", name="Dismiss Changes")
            if dismiss_btn.is_visible():
                dismiss_btn.click()
                print("All toggles tested and changes dismissed.")


if __name__ == "__main__":
    run_tests()