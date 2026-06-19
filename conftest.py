import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.navigation_menu import NavigationMenu
from pages.network_config_page import NetworkConfigPage
from utils.config_reader import Config
from pages.das_interrogator_page import DasInterrogatorPage
from pages.configuration_database_page import DatabasePage
from pages.configuration_anomoly_server_page import AnomalyServerPage


config = Config()   
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


@pytest.fixture(scope="module")
def network_config_setup(browser):
    """Logs in, navigates to Network Config, and yields the config page object."""
    # 1. Setup Browser Context
    context = browser.new_context()
    page = context.new_page()
    
    # 2. Initialize Page Objects
    login_pg = LoginPage(page)
    nav_menu = NavigationMenu(page)
    config_pg = NetworkConfigPage(page)
    
    # 3. Use config reader for credentials to Login
    login_pg.navigate(Config.BASE_URL) # Or login_pg.go_to_login() depending on your method name
    login_pg.login(Config.EMAIL, Config.PASSWORD)
    
    # Wait for dashboard to ensure login was successful before navigating
    page.wait_for_url(lambda url: "dashboard" in url, timeout=10000)
    
    # 4. Navigate to Network Config
    nav_menu.go_to_configuration()
    config_pg.open_network_config()
    
    # 5. Yield the specific Page Object to your tests
    yield config_pg
    
    # 6. Teardown: Close context after all tests in the module finish
    context.close()


@pytest.fixture(scope="module")
def das_interrogator_setup(browser):
    """Logs in, navigates to DAS Interrogator, and yields the page object."""
    context = browser.new_context()
    page = context.new_page()
    
    login_pg = LoginPage(page)
    nav_menu = NavigationMenu(page)
    das_pg = DasInterrogatorPage(page)
    
    # Login
    login_pg.navigate(Config.BASE_URL)
    login_pg.login(Config.EMAIL, Config.PASSWORD)
    page.wait_for_url(lambda url: "dashboard" in url, timeout=10000)
    
    # Navigate to Configuration -> DAS Interrogator
    nav_menu.go_to_configuration()
    das_pg.open_das_interrogator()
    
    yield das_pg
    
    context.close()


@pytest.fixture(scope="module")
def database_setup(browser):
    """Logs in, navigates to Database config, and yields the page object."""
    context = browser.new_context()
    page = context.new_page()
    
    login_pg = LoginPage(page)
    nav_menu = NavigationMenu(page)
    db_pg = DatabasePage(page)
    
    # Login
    login_pg.navigate(Config.BASE_URL)
    login_pg.login(Config.EMAIL, Config.PASSWORD)
    page.wait_for_url(lambda url: "dashboard" in url, timeout=10000)
    
    # Navigate to Configuration -> Database
    nav_menu.go_to_configuration()
    db_pg.navigate_to_database()
    
    yield db_pg
    
    context.close()

@pytest.fixture(scope="module")
def anomaly_server_setup(browser):
    """Logs in, navigates to Anomaly Server config, and yields the page object."""
    context = browser.new_context()
    page = context.new_page()
    
    login_pg = LoginPage(page)
    nav_menu = NavigationMenu(page)
    anomaly_pg = AnomalyServerPage(page)
    
    # Login
    login_pg.navigate(Config.BASE_URL)
    login_pg.login(Config.EMAIL, Config.PASSWORD)
    page.wait_for_url(lambda url: "dashboard" in url, timeout=10000)
    
    # Navigate to Configuration -> Anomaly Server
    nav_menu.go_to_configuration()
    anomaly_pg.navigate_to_anomaly_server()
    
    yield anomaly_pg
    
    context.close()