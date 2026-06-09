import os
from dotenv import load_dotenv
# This function finds the .env file and loads its contents into the environment
load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    EMAIL = os.getenv("TEST_EMAIL")
    PASSWORD = os.getenv("TEST_PASSWORD")

    # --- Jira Xray Configuration ---
    XRAY_CLIENT_ID = os.getenv("XRAY_CLIENT_ID")
    XRAY_CLIENT_SECRET = os.getenv("XRAY_CLIENT_SECRET")
    JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "IU")