'''import pytest
from playwright.sync_api import Page,expect

# Import your Page Objects and Config
from pages.login_page import LoginPage
from pages.navigation_menu import NavigationMenu
from pages.network_config_page import NetworkConfigPage
from utils.config_reader import Config'''
from playwright.sync_api import expect

'''def test_update_and_revert_chassis_name(page: Page):
    # 1. Initialize Page Objects
    login_page = LoginPage(page)
    nav_menu = NavigationMenu(page)
    config_page = NetworkConfigPage(page)

    # 2. Login Phase
    login_page.navigate(config.BASE_URL)
    print(f"Title: {page.title()}")
    
    login_page.login(config.EMAIL, config.PASSWORD)
    assert "dashboard" in page.url, "Failed: Expected to be on dashboard."
    print("Login successful and on the correct page.")

    # 3. Navigation Phase
    nav_menu.go_to_configuration()
    print("Configuration page is displayed correctly.")

    # 4. Open Network Config
    config_page.open_network_config()
    print("Network Config button is clicked.")


    # 5. Edit Phase
    config_page.click_edit()
    assert config_page.is_save_button_visible(), "Failed: Edit mode not activated."
    print("Edit button clicked successfully: Save button is now visible.")

    # 6. Update Data
    old_name = "UAT Testing"
    new_name = "Automation-Test-1"
    
    config_page.update_chassis_name(new_name)
    print(f"Chassis name changed to: {new_name}")
    
    config_page.save_changes()
    print("Changes saved successfully.")

    # 7. Verification Phase
    page.reload() 
    page.wait_for_timeout(2000)  # Wait for backend to process save
    expect(config_page.save_button).not_to_be_visible(timeout=10000)

    # 8. Teardown / Revert Changes to keep environment clean
    page.reload()
    config_page.click_edit()
    config_page.update_chassis_name(old_name)
    config_page.save_changes()
    print(f"Chassis name changed back to: {old_name}")

    #change the hostname and domain name as well
    new_hostname = "myserver"
    new_domain = "example.com"
    config_page.click_edit()
    config_page.update_hostname(new_hostname)
    config_page.update_domain_name(new_domain)
    config_page.save_changes()
    print("Changes saved successfully.")
    nav_menu.sidebar_toggle.click()
    page.reload()
    expect(config_page.save_button).not_to_be_visible(timeout=10000)

    # Click edit to reveal the inputs again so we can read them
    config_page.click_edit()
    assert config_page.get_hostname_value() == new_hostname, "Hostname failed to save."
    assert config_page.get_domain_value() == new_domain, "Domain failed to save."
    print("All fields updated successfully and verified.")
    
    # Brief pause before Pytest automatically closes the browser
    page.wait_for_timeout(2000)'''

from playwright.sync_api import expect

def test_update_and_revert_chassis_name(network_config_setup):
    """Test 1: Safely change the chassis name and verify."""
    config_page = network_config_setup 

    # --- 1. DYNAMIC DATA CAPTURE ---
    config_page.click_edit()
    assert config_page.is_save_button_visible(), "Failed: Edit mode not activated."
    
    old_name = config_page.get_chassis_name_value()
    print(f"Captured original Chassis Name: {old_name}")

    # --- 2. UPDATE DATA ---
    new_name = "Automation-Test-1"
    config_page.update_chassis_name(new_name)
    config_page.save_changes()
    
    # Wait a moment for the backend API request to fire, then forcefully reload
    config_page.page.wait_for_timeout(2000) 
    config_page.page.reload() 

    # --- 3. VERIFICATION ---
    config_page.click_edit()
    assert config_page.get_chassis_name_value() == new_name, "Chassis Name failed to save."
    print("Test 1 Passed: Chassis name updated successfully.")

    # --- 4. TEARDOWN / REVERT ---
    config_page.update_chassis_name(old_name)
    config_page.save_changes()
    
    config_page.page.wait_for_timeout(2000)
    config_page.page.reload()
    print("Environment cleaned up.")


def test_update_and_revert_hostname_and_domain(network_config_setup):
    """Test 2: Safely change the hostname and domain name."""
    config_page = network_config_setup

    # --- 1. DYNAMIC DATA CAPTURE ---
    # Because the last test reloaded the page, we definitely need to click edit
    config_page.click_edit()
        
    old_hostname = config_page.get_hostname_value()
    old_domain = config_page.get_domain_value()
    print(f"Captured original Hostname: {old_hostname}, Domain: {old_domain}")

    # --- 2. UPDATE DATA ---
    new_hostname = "myserver"
    new_domain = "example.com"
    
    config_page.update_hostname(new_hostname)
    config_page.update_domain_name(new_domain)
    config_page.save_changes()

    config_page.page.wait_for_timeout(2000)
    config_page.page.reload()

    # --- 3. VERIFICATION ---
    config_page.click_edit()
    assert config_page.get_hostname_value() == new_hostname, "Hostname failed to save."
    assert config_page.get_domain_value() == new_domain, "Domain failed to save."
    print("Test 2 Passed: Hostname and Domain updated successfully.")

    # --- 4. TEARDOWN / REVERT ---
    config_page.update_hostname(old_hostname)
    config_page.update_domain_name(old_domain)
    config_page.save_changes()
    
    config_page.page.wait_for_timeout(2000)
    config_page.page.reload()
    print("Environment cleaned up.")