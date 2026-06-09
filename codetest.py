from playwright.sync_api import sync_playwright

def verify_email_error_locator():
    with sync_playwright() as p:
        # Launch browser visibly so you can watch what happens
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        print("1. Navigating to the login page...")
        # ⚠️ IMPORTANT: Replace this with your actual application URL
        page.goto("http://10.101.54.90:4200/login") 

        print("2. Triggering the 'Email is required' error...")
        # Fill the password but leave the email blank to force the email error
        page.get_by_placeholder("Enter password").fill("TestPassword123!")
        page.get_by_role("button", name="Sign In").click()

        print("3. Searching for the exact text: 'Email is required'...")
        # This is the exact locator you want to test
        # We use exact=True to ensure it doesn't accidentally match a longer sentence
        email_required_error = page.get_by_text("Email is required", exact=True)

        try:
            # Wait up to 5 seconds for the text to appear on screen
            email_required_error.wait_for(state="visible", timeout=5000)
            
            print("\n✅ SUCCESS: The locator found the text perfectly!")
            print("👉 The validation message is visible and recognized by Playwright.\n")

        except Exception as e:
            print("\n❌ FAILED: Playwright could not find 'Email is required' within 5 seconds.")
            print("Possible reasons:")
            print(" - The error text has hidden spaces or is slightly different in the DOM.")
            print(" - The button click didn't trigger the validation properly.")
            print(f"Error details: {e}\n")

        # Keep the browser open for 2 seconds so you can see the final state
        page.wait_for_timeout(2000) 
        browser.close()

if __name__ == "__main__":
    verify_email_error_locator()