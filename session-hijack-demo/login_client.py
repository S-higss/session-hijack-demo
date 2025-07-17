import requests
import json
import os

# Server settings
SERVER_URL = "http://127.0.0.1:8000"
SESSION_COOKIE_FILE = "session_cookie.txt"  # File to save the session cookie

def register_user(username, password):
    print(f"Attempting to register user: {username}")
    register_url = f"{SERVER_URL}/register"
    payload = {'username': username, 'password': password}
    
    try:
        response = requests.post(register_url, data=payload)
        print(f"Registration response status: {response.status_code}")
        print(f"Registration response body: {response.text.strip()}")
        if response.status_code == 201:
            print("User registered successfully.")
            return True
        else:
            print("User registration failed.")
            return False
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the server at {SERVER_URL}. Is the server running?")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during registration: {e}")
        return False

def login_user(username, password):
    print(f"\nAttempting to log in user: {username}")
    login_url = f"{SERVER_URL}/login"
    payload = {'username': username, 'password': password}
    
    try:
        session = requests.Session()  # Create a session object to automatically manage cookies
        response = session.post(login_url, data=payload)
        print(f"Login response status: {response.status_code}")
        print(f"Login response body: {response.text.strip()}")

        if response.status_code == 200:
            print("Login successful.")
            # Get the session cookie
            session_id = session.cookies.get('session_id')
            if session_id:
                print(f"Session ID obtained: {session_id}")
                # Save the session cookie to a file
                with open(SESSION_COOKIE_FILE, 'w') as f:
                    f.write(session_id)
                print(f"Session ID saved to {SESSION_COOKIE_FILE}")
                return session
            else:
                print("Error: No session_id cookie received after login.")
                return None
        else:
            print("Login failed.")
            return None
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the server at {SERVER_URL}. Is the server running?")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        return None

def access_dashboard(session):
    if not session:
        print("Cannot access dashboard: No active session.")
        return

    print("\nAccessing dashboard with obtained session...")
    dashboard_url = f"{SERVER_URL}/dashboard"
    try:
        response = session.get(dashboard_url)
        print(f"Dashboard access status: {response.status_code}")
        print(f"Dashboard content:\n{response.text.strip()}")
        if response.status_code == 200:
            print("Successfully accessed dashboard.")
        else:
            print("Failed to access dashboard.")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the server at {SERVER_URL}. Is the server running?")
    except Exception as e:
        print(f"An unexpected error occurred during dashboard access: {e}")

if __name__ == "__main__":
    # User information to register
    TEST_USERNAME = "testuser"
    TEST_PASSWORD = "testpass"

    # 1. Register user
    if register_user(TEST_USERNAME, TEST_PASSWORD):
        # 2. Log in
        logged_in_session = login_user(TEST_USERNAME, TEST_PASSWORD)
        
        # 3. Attempt to access the dashboard (accessed by the login client itself)
        if logged_in_session:
            access_dashboard(logged_in_session)
        else:
            print("Login failed, cannot access dashboard.")
    else:
        print("Registration failed, cannot proceed with login.")

    print("\nLogin Client operations completed.")
    print(f"Please check '{SESSION_COOKIE_FILE}' for the saved session ID.")
