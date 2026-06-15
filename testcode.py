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
        #varify the Sytem Helth
        page.get_by_role("link", name="System Health").click()
        page.wait_for_url(lambda url: "system-health-monitoring" in url, timeout=5000)
        print("System Health page is displayed correctly.")



        #click the classic link
        page.locator(".system-card").filter(has_text="Chassis").click()
        page.wait_for_url(lambda url: "chassis-monitoring" in url, timeout=5000)
        print("Chassis Monitoring page is displayed correctly.")
        time.sleep(1)

        # scroll down the page
        # page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # print("Scrolled down the page.")
        # time.sleep(1)

        #Live button
        page.locator(".toggle-slider").dblclick()
        print("Live button is clicked.")
        time.sleep(3)

        browser.close()


if __name__ == "__main__":

    run_tests()
