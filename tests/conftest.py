import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config_reader import Config

@pytest.fixture
def login_page(page: Page):
    """Provides a fresh LoginPage instance for each test."""
    return LoginPage(page)

@pytest.fixture
def dashboard_page(page: Page):
    """Provides a fresh DashboardPage instance."""
    return DashboardPage(page)

@pytest.fixture(scope="module")
def authenticated_dashboard(browser):
    """Logs in once per module and yields the dashboard page."""
    context = browser.new_context()
    page = context.new_page()
    
    login_pg = LoginPage(page)
    dashboard_pg = DashboardPage(page)
    
    # Use config reader for credentials
    login_pg.go_to_login(Config.BASE_URL)
    login_pg.login(Config.EMAIL, Config.PASSWORD)
    dashboard_pg.wait_for_dashboard_to_load()
    
    yield dashboard_pg
    
    context.close()