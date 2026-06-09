import pytest

pytestmark = pytest.mark.order(2) # Forces this entire file to run second

def test_branding_logo_is_visible(authenticated_dashboard):
    assert authenticated_dashboard.is_brand_logo_visible(), "Failed: Branding logo is not visible."

def test_sidebar_routes_are_accessible(authenticated_dashboard):
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

def test_map_overlay_components_are_visible(authenticated_dashboard):
    authenticated_dashboard.summary_btn.wait_for(state="visible")
    assert authenticated_dashboard.summary_btn.is_visible(), "Failed: Summary button missing."
    
    authenticated_dashboard.channel_plot.wait_for(state="visible")
    assert authenticated_dashboard.channel_plot.is_visible(), "Failed: Channel plot missing."
    
    authenticated_dashboard.alerts_btn.wait_for(state="visible")
    assert authenticated_dashboard.alerts_btn.is_visible(), "Failed: Alerts button missing."

def test_zones_panel_contains_all_options(authenticated_dashboard):
    authenticated_dashboard.open_zones_panel()
    
    expected_zones = ["TestZone", "Zone_1", "Zone_2", "Zone_3", "Zone_4"]
    for zone in expected_zones:
        zone_element = authenticated_dashboard.get_exact_text_element(zone)
        zone_element.wait_for(state="visible")
        assert zone_element.is_visible(), f"Failed: {zone} not found in panel."

def test_cameras_panel_contains_all_options(authenticated_dashboard):
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
        camera_element.wait_for(state="visible")
        assert camera_element.is_visible(), f"Failed: {camera} not found in panel."

def test_filter_functionality(authenticated_dashboard):
    # Apply filter
    authenticated_dashboard.apply_high_severity_filter()
    
    # Verify Apply was successful/exists
    #assert authenticated_dashboard.apply_btn.is_visible(), "Failed: Apply button not visible."
    
    # Reset state for next tests
    authenticated_dashboard.clear_filters()

def test_map_style_button(authenticated_dashboard):
    authenticated_dashboard.map_style_btn.wait_for(state="visible")
    assert authenticated_dashboard.map_style_btn.is_visible(), "Failed: Map Style button not found."
    authenticated_dashboard.map_style_btn.click()

def test_fullscreen_toggle_displays_summary(authenticated_dashboard):
    authenticated_dashboard.toggle_fullscreen(enter=True)
    
    authenticated_dashboard.summary_btn.wait_for(state="visible")
    assert authenticated_dashboard.summary_btn.is_visible(), "Failed: Summary button missing in fullscreen."
    
    authenticated_dashboard.toggle_fullscreen(enter=False)

def test_map_summary_dropdown_options(authenticated_dashboard):
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