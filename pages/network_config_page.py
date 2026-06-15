class NetworkConfigPage:
    def __init__(self, page):
        self.page = page
        # Using the robust locators we discussed earlier
        self.network_config_tab = page.get_by_role("radio", name="Network Config")
        self.edit_button = page.get_by_role("button", name="Edit")
        self.save_button = page.get_by_role("button", name=" Save Changes ")
        self.chassis_input = page.get_by_placeholder("Enter Chassis Name")
        self.hostname_input = page.get_by_placeholder("Enter hostname (e.g., myserver)")
        self.domain_input = page.get_by_placeholder("Enter domain (e.g., example.com)")

    def open_network_config(self):
        self.network_config_tab.click()

    def click_edit(self):
        self.edit_button.click()

    def is_save_button_visible(self):
        return self.save_button.is_visible()

    def update_chassis_name(self, new_name):
        self.chassis_input.click()
        self.chassis_input.clear()
        self.chassis_input.fill(new_name)

    def save_changes(self):
        self.save_button.click()

    def get_chassis_name_value(self):
        return self.chassis_input.input_value()
    
    def update_hostname(self, new_hostname):
        self.hostname_input.click()
        self.hostname_input.clear()
        self.hostname_input.fill(new_hostname)

    def get_hostname_value(self):
        # Using the robust wait we learned to prevent Timeouts!
        self.hostname_input.wait_for(state="attached", timeout=10000)
        return self.hostname_input.input_value()

    def update_domain_name(self, new_domain):
        self.domain_input.click()
        self.domain_input.clear()
        self.domain_input.fill(new_domain)

    def get_domain_value(self):
        self.domain_input.wait_for(state="attached", timeout=10000)
        return self.domain_input.input_value()