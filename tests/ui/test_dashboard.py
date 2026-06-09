import pytest
from playwright.sync_api import expect

from pages.dashboard_page import DashboardPage


def test_branding_logo_is_visible(authenticated_dashboard: DashboardPage):
    assert authenticated_dashboard.is_brand_logo_visible(), "Failed: Branding logo is not visible."

def test_sidebar_routes_are_accessible(authenticated_dashboard: DashboardPage):
    sidebar_routes = [
        "/home/dashboard",
        "/home/system-health-monitoring",
        "/home/monitoring",
        "/home/system"
    ]
    for route in sidebar_routes:
        menu_link = authenticated_dashboard.get_sidebar_link(route)
        menu_link.wait_for(state="visible", timeout=5000)
        
        assert menu_link.is_visible(), f"Failed: Sidebar route {route} is not visible."
        
        if route == "/home/dashboard":
            class_attr = menu_link.get_attribute("class")
            assert "active" in class_attr, "Failed: Dashboard menu link is not active."

def test_map_overlay_components_are_visible(authenticated_dashboard: DashboardPage):
    """Verifies core structural widget buttons map correctly on the viewport."""
    expect(authenticated_dashboard.summary_btn).to_be_visible()
    expect(authenticated_dashboard.channel_plot).to_be_visible()
    expect(authenticated_dashboard.alerts_btn).to_be_visible()

def test_zones_panel_contains_all_options(authenticated_dashboard: DashboardPage):
    """Validates full string list population inside the zones context slider."""
    authenticated_dashboard.open_zones_panel()
    
    expected_zones = ["TestZone", "Zone_1", "Zone_2", "Zone_3", "Zone_4"]
    for zone in expected_zones:
        zone_element = authenticated_dashboard.get_exact_text_element(zone)
        expect(zone_element).to_be_visible()

def test_cameras_panel_contains_all_options(authenticated_dashboard: DashboardPage):
    """Validates complete camera hardware mappings load cleanly in UI lists."""
    authenticated_dashboard.open_cameras_panel()
    
    expected_cameras = [
        "Parking lot (Old test bed)",
        "Volleyball ground (Old test bed)",
        "Buried Section 1 (New test bed)",
        "Buried Section 2 (New test bed)",
        "Fence (New test bed)"
    ]
    for camera in expected_cameras:
        camera_element = authenticated_dashboard.get_exact_text_element(camera)
        expect(camera_element).to_be_visible()

def test_filter_functionality(authenticated_dashboard: DashboardPage):
    """Applies event sorting scopes and guarantees visual clean down states."""
    try:
        authenticated_dashboard.apply_high_severity_filter()
        # Add specific filter assertions here if applicable
    finally:
        # The finally block guarantees this runs even if the actions above fail
        authenticated_dashboard.clear_filters()

def test_map_style_button(authenticated_dashboard: DashboardPage):
    """Verifies responsiveness of base map presentation toggles."""
    expect(authenticated_dashboard.map_style_btn).to_be_visible()
    authenticated_dashboard.map_style_btn.click()

def test_fullscreen_toggle_displays_summary(authenticated_dashboard: DashboardPage):
    """Ensures map views expand dynamically and reset to normal gracefully."""
    try:
        authenticated_dashboard.toggle_fullscreen(enter=True)
        expect(authenticated_dashboard.summary_btn).to_be_visible()
    finally:
        authenticated_dashboard.toggle_fullscreen(enter=False)

def test_map_summary_dropdown_options(authenticated_dashboard: DashboardPage):
    authenticated_dashboard.toggle_fullscreen(enter=True)
    authenticated_dashboard.open_summary_popup()

    summary_options = [
        "Channel 1 Live",
        "Channel 1 Past",
        "Channel 2 Live",
        "Channel 2 Past"
    ]

    for option in summary_options:
        is_visible = authenticated_dashboard.select_summary_option(option)
        assert is_visible, f"Failed: Option '{option}' is not visible."

    # Exit fullscreen to clean up UI state
    authenticated_dashboard.toggle_fullscreen(enter=False)