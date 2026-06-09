import pytest
from playwright.sync_api import expect
from utils.config_reader import Config

# SUCCESS SCENARIOS
@pytest.mark.parametrize("email, password", [
    (Config.EMAIL, Config.PASSWORD),
    (f"   {Config.EMAIL}   ", Config.PASSWORD) # Test whitespace cleanup
])
def test_successful_login(login_page, page, email, password):
    """Verifies that valid credentials allow access to the dashboard."""
    login_page.go_to_login(Config.BASE_URL)
    login_page.login(email, password)
    
    # Web-first check for redirection
    login_page.wait_for_url_contains("dashboard")
    expect(page).not_to_have_url(f"{Config.BASE_URL.rstrip('/')}/login")

# NEGATIVE/VALIDATION SCENARIOS
@pytest.mark.parametrize("email, password", [
    (Config.EMAIL, "WrongPassword123!"), # Invalid password
    ("", ""),                             # Empty credentials
    (Config.EMAIL.upper(), Config.PASSWORD), # Case sensitivity check
])
def test_failed_login_remains_on_page(login_page, email, password):
    """Verifies that invalid login attempts stay on the login page."""
    login_page.go_to_login(Config.BASE_URL)
    login_page.login(email, password)
    
    # Assert we are still on the login page
    expect(login_page.sign_in_button).to_be_visible()
    
# UI ERROR MESSAGE TESTS
def test_empty_email_shows_error(login_page):
    """Verifies specific UI feedback for missing email."""
    login_page.go_to_login(Config.BASE_URL)
    login_page.login("", Config.PASSWORD)
    
    expect(login_page.email_required_error).to_be_visible()
    expect(login_page.password_required_error).not_to_be_visible()

def test_empty_password_shows_error(login_page):
    """Verifies specific UI feedback for missing password."""
    login_page.go_to_login(Config.BASE_URL)
    login_page.login(Config.EMAIL, "")
    
    expect(login_page.password_required_error).to_be_visible()
    expect(login_page.email_required_error).not_to_be_visible()