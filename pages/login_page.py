from pages.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/login"
        
        # Locators
        self.email_input = page.get_by_placeholder("Enter Email")
        self.password_input = page.get_by_placeholder("Enter password")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        
        # Exact Text Locators for Validation Errors
        self.email_required_error = page.get_by_text("Email is required", exact=True)
        self.password_required_error = page.get_by_text("Password is required", exact=True)

    def go_to_login(self, base_url: str):
       clean_url = f"{base_url.rstrip('/')}{self.url}"
       self.navigate(clean_url)

    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()