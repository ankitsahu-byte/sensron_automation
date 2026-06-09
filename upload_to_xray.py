import sys
import requests
from utils.config_reader import Config

# --- Configuration ---
# Loading our secure credentials from the Config class
CLIENT_ID = Config.XRAY_CLIENT_ID
CLIENT_SECRET = Config.XRAY_CLIENT_SECRET
PROJECT_KEY = Config.JIRA_PROJECT_KEY
XML_FILE_PATH = "reports/xml/results.xml"

def upload_results():
    # 1. Validate Credentials
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Error: XRAY_CLIENT_ID or XRAY_CLIENT_SECRET is missing.")
        print("Make sure they are defined in your .env file and loaded in config_reader.py.")
        sys.exit(1)

    # 2. Authenticate with Xray
    print("🔄 Authenticating with Jira Xray Cloud...")
    auth_url = "https://xray.cloud.getxray.app/api/v2/authenticate"
    
    auth_response = requests.post(auth_url, json={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    
    if auth_response.status_code != 200:
        print(f"❌ Authentication failed: {auth_response.text}")
        sys.exit(1)
        
    token = auth_response.json()
    print("✅ Authentication successful.")

    # 3. Read the generated test report
    try:
        with open(XML_FILE_PATH, 'r', encoding='utf-8') as file:
            xml_data = file.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{XML_FILE_PATH}'.")
        print("Did you remember to run your tests first using: pytest --junitxml=results.xml ?")
        sys.exit(1)

    # 4. Upload the report to Jira
    print(f"🔄 Uploading test results to Jira project: {PROJECT_KEY}...")
    upload_url = f"https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey={PROJECT_KEY}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "text/xml"
    }

    # Encode data to utf-8 to safely handle any special characters in the test logs
    upload_response = requests.post(upload_url, headers=headers, data=xml_data.encode('utf-8'))

    # 5. Output the result
    if upload_response.status_code == 200:
        print("🎉 Successfully uploaded the report to Jira Xray!")
        print("Jira Ticket Info:", upload_response.json())
    else:
        print(f"❌ Upload failed with status code: {upload_response.status_code}")
        print("Response:", upload_response.text)

if __name__ == "__main__":
    upload_results()