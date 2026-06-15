import time
from playwright.sync_api import sync_playwright

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


        #Enter credentials
        page.get_by_placeholder("Enter Email").fill(EMAIL)
        page.get_by_placeholder("Enter password").fill(PASSWORD)
        # submit form
        page.get_by_role("button", name="Sign In").click()

        # check login is successful by waiting for the dashboard URL
        page.wait_for_url(lambda url: "dashboard" in url, timeout=5000)

        # Verify the URL is correct
        assert "dashboard" in page.url, "Failed: Expected to be on dashboard, but URL is incorrect."
        print("Login successful and on the correct page.")

        #click the slider button
        page.locator("xpath=//img[contains(@class, 'sidebar-toggle')]").click()
        print("Slider button is clicked.")
        time.sleep(1)

        #verify the Configuration
        page.get_by_role("link", name="Configuration").click()
        page.wait_for_url(lambda url: "configPage" in url, timeout=5000)
        print("Configuration page is displayed correctly.")

        #click the netwrkconfig button
        page.get_by_role("radio", name="Network Config").click()
        print("Network Config button is clicked.")

        #click the edit button
        Edit_button = page.get_by_role("button", name="Edit")
        Edit_button.click()

        # Validate the edit button is clicked successfully by checking if the Save button appears
        save_button = page.get_by_role("button", name="Save Changes")
        assert save_button.is_visible(), "Failed: Edit mode not activated (Save button not visible)."
        print("Edit button clicked successfully: Save button is now visible.")

        # Change the chassis name 
        old_name = "UAT Testing"
        new_name = "Automation-Test-1"
        chassis_input = page.get_by_placeholder("Enter Chassis Name")
        chassis_input.click()
        chassis_input.clear()
        chassis_input.fill(new_name)
        print(f"Chassis name changed to: {new_name}")
        save_button.click()
        print("Changes saved successfully.")

        # Verify the chassis name is updated by checking the input value after saving
        page.wait_for_timeout(2000)  # Wait for the changes to be processed
        updated_name = chassis_input.input_value()
        assert updated_name == new_name, f"Failed: Expected chassis name to be '{new_name}', but got '{updated_name}'."
        print("Chassis name updated successfully and verified.")

        #now make the changes back to original
        page.reload()
        Edit_button.click()
        chassis_input.click()
        chassis_input.clear()
        chassis_input.fill(old_name)
        print(f"Chassis name changed back to: {old_name}")
        save_button.click()
        print("Changes saved successfully.")


        

 
        time.sleep(5)




        browser.close()


if __name__ == "__main__":

    run_tests()
