#!/usr/bin/python3

import os
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
# concatenate the URL to login and api paths
WOFFU_URL = os.getenv("WOFFU_URL") + "/v2/login"
API_URL = os.getenv("WOFFU_URL") + "/api/svc/signs/signs"
EMAIL = os.getenv("WOFFU_EMAIL")
PASSWORD = os.getenv("WOFFU_PASSWORD")

SELECTORS = {
    "email_input": (By.NAME, "email"),
    "continue_button": (By.CSS_SELECTOR, '[data-qa="auth-login-next-button"]'),
    "password_input": (By.NAME, "password"),
    "final_login_button": (By.CSS_SELECTOR, '[data-qa="auth-login-button"]'),
}

def _initialize_driver():
    print("Initializing WebDriver...")
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Uncomment to run in headless mode
    chrome_options.add_argument("--window-size=1920,1080")

    # Auto-accept Geolocation
    prefs = {"profile.default_content_setting_values.geolocation": 1}
    chrome_options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(options=chrome_options)

def _login(driver, wait):
    print(f"Navigating to login page: {WOFFU_URL}")
    driver.get(WOFFU_URL)
    try:
        wait.until(EC.presence_of_element_located(SELECTORS["email_input"])).send_keys(EMAIL)
        wait.until(EC.element_to_be_clickable(SELECTORS["continue_button"])).click()

        pwd = wait.until(EC.presence_of_element_located(SELECTORS["password_input"]))
        pwd.send_keys(PASSWORD)
        wait.until(EC.element_to_be_clickable(SELECTORS["final_login_button"])).click()

        # Wait for dashboard to ensure cookies are set
        wait.until(EC.url_contains("dashboard"))
        print("Login successful.")
        return True
    except Exception as e:
        print(f"Login Failed: {e}")
        return False

def _perform_clock_action(driver, wait):
    print(f"Preparing to perform action")

    # 1. Extract the JWT Token from Selenium Cookies
    cookies = driver.get_cookies()
    token = None
    for cookie in cookies:
        if cookie.get('name') == 'woffu.token':
            token = cookie.get('value')
            break

    if not token:
        print("Error: Could not retrieve 'woffu.token' from cookies. Cannot proceed with API call.")
        return

    # 2. Construct Headers (replicating the cURL)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': driver.execute_script("return navigator.userAgent;") # Use same UA as Selenium
    }

    # 3. Construct Payload
    payload = {
        "agreementEventId": None,
        "requestId": None,
        "deviceId": "WebApp",
        "latitude": None,
        "longitude": None,
        "timezoneOffset": -60
    }

    # 4. Send POST Request
    try:
        print(f"Sending POST request to {API_URL}...")
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            print(f"✅ Success!")
            print(f"Server Response: {response.text}")
        else:
            print(f"❌ Failed to perform action.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"An error occurred during the request: {e}")

# --- MAIN ---
if __name__ == "__main__":
    if not EMAIL or not PASSWORD or WOFFU_URL.strip() == "/v2/login":
        print("Set WOFFU_EMAIL, WOFFU_PASSWORD and WOFFU_URL environment variables.")
        sys.exit(1)

    driver = _initialize_driver()
    wait = WebDriverWait(driver, 15) # Increased wait time slightly

    if _login(driver, wait):
        _perform_clock_action(driver, wait)

    print("Closing browser.")
    driver.quit()
