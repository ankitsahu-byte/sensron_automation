import pytest
from playwright.sync_api import expect
from utils.config_reader import Config

pytestmark = pytest.mark.order(1) # Forces this entire file to run first

login_scenarios = [
    ("Valid Login", Config.EMAIL, Config.PASSWORD, True),
    ("Invalid Password", Config.EMAIL, "WrongPassword123!", False),
    ("Empty Credentials", "", "", False),
    #Case Sensitivity Tests
    ("Username Case Insensitive", Config.EMAIL.upper(), Config.PASSWORD, False),
    ("Password Case Sensitive", Config.EMAIL, Config.PASSWORD.swapcase(), False),
    #Whitespace Handling Tests
    ("Whitespace in Username", f"   {Config.EMAIL}   ", Config.PASSWORD, True)
]
# Extract the scenario names to use as safe IDs in the report
scenario_names = [scenario[0] for scenario in login_scenarios]

@pytest.mark.parametrize("test_name, email, password, expect_success", login_scenarios, ids=scenario_names)
def test_login_validation(login_page, page, test_name, email, password, expect_success):
    login_page.go_to_login(Config.BASE_URL)
    login_page.login(email, password)

    if expect_success:
        login_page.wait_for_url_contains("dashboard")
        assert "login" not in page.url
    else:
        expect(login_page.sign_in_button).to_be_visible()
        assert "login" in page.url


# --- SPECIFIC UI ERROR MESSAGE TESTS ---

def test_empty_email_shows_error(login_page):
    """Test Case: Leaving email empty triggers 'Email is required' text."""
    login_page.go_to_login(Config.BASE_URL)
    
    # Fill password, leave email blank
    login_page.login("", Config.PASSWORD)
    
    # Validate the email error appears, and password error does NOT appear
    expect(login_page.email_required_error).to_be_visible()
    expect(login_page.password_required_error).not_to_be_visible()


def test_empty_password_shows_error(login_page):
    """Test Case: Leaving password empty triggers 'Password is required' text."""
    login_page.go_to_login(Config.BASE_URL)
    
    # Fill email, leave password blank
    login_page.login(Config.EMAIL, "")
    
    # Validate the password error appears, and email error does NOT appear
    expect(login_page.password_required_error).to_be_visible()
    expect(login_page.email_required_error).not_to_be_visible()
