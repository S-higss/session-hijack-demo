# session-hijack-demo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Japanese version](README_ja.md)

## Overview

`Simple-Session-Hijack-Demo` is a demonstration repository designed to illustrate the basic operation of session management using HTTP cookies and one of its vulnerabilities: session hijacking attacks. The purpose of this repository is to help users understand the importance of session security for educational purposes.

**Warning**: This code is provided for educational and research purposes only. Unauthorized use or use for malicious purposes on actual systems is **strictly prohibited**.

## Purpose

This repository was developed with the following objectives:

1. **Understanding HTTP Session Management**: Learn the mechanisms of server-side session management using HTTP cookies.
2. **Principle of Session Hijacking**: Understand how an attacker can steal a valid session cookie and impersonate a legitimate user to access authenticated resources.
3. **Enhancing Security Awareness**: Recognize the importance of session security in web applications and the necessity of cookie protection.

## Features

* **`http_server.py`**:
  * A simple HTTP server implementing cookie-based session management.
  * Provides user registration (`/register`) and login (`/login`) functionalities.
  * Offers a protected resource (`/dashboard`) accessible only by logged-in users.
  * Issues session IDs as HTTP cookies named `session_id`.
* **`login_client.py`**:
  * A client simulating a legitimate user who registers and then logs into `http_server.py`.
  * Upon successful login, it reads the session cookie issued by the server and saves it to a file named `session_cookie.txt`.
  * Uses the saved cookie to access the protected resource (`/dashboard`) and verifies that its own information is displayed.
* **`attack_client.py`**:
  * A client simulating an attacker.
  * Illegally reads the session ID from the `session_cookie.txt` file saved by `login_client.py`.
  * Includes the read session ID as a cookie in its HTTP requests to access the protected resource (`/dashboard`) on `http_server.py`.
  * This demonstrates that the attacker can hijack the user's session and obtain information without being legitimately authenticated.

## File Structure

```tree
.
├── README.md
├── README_ja.md
└── session-hijack-demo
    ├── http_server.py
    ├── login_client.py
    └── attack_client.md
    ├── session_cookie.txt  # Generated when login_client.py is executed
```

## Setup

### Prerequisites

* Python 3.6+ must be installed.
* `pip` package manager must be available.

### Installing Required Libraries

`login_client.py` and `attack_client.py` use the `requests` library. Install it using the following command:

```bash
pip install requests
```

## How to Use Each Tool

### Session Hijacking Scenario Reproduction Steps

Follow these steps to execute each script sequentially and reproduce a session hijacking attack.

1. **Start the HTTP Server (`http_server.py`)**
    * Open your first terminal and run the following command:

        ```bash
        python3 http_server.py
        ```

    * The server will start listening on `127.0.0.1:8000`.
    * *Server Output Example:*

        ```bash
        Serving HTTP on 127.0.0.1:8000...
        Press Ctrl+C to stop the server.
        ```

2. **Execute the Login Client (`login_client.py`)**
    * While the server is running, open **another terminal** and run the following command:

        ```bash
        python3 login_client.py
        ```

    * This script will register a user (`testuser`), log in, and then access the dashboard.
    * Upon successful login, the session ID received from the server will be saved to the `session_cookie.txt` file.
    * *Login Client Output Example:* (Session ID will vary per execution)

        ```bash
        Attempting to register user: testuser
        Registration response status: 201
        ...
        Login successful.
        Session ID obtained: [UNIQUE_SESSION_ID]
        Session ID saved to session_cookie.txt
        ...
        Successfully accessed dashboard.
        Login Client operations completed.
        Please check 'session_cookie.txt' for the saved session ID.
        ```

3. **Execute the Attack Client (`attack_client.py`)**
    * While the server and login client are running (or immediately after the login client has completed and `session_cookie.txt` exists), open **yet another terminal** and run the following command:

        ```bash
        python3 attack_client.py
        ```

    * This script will read the session ID from `session_cookie.txt` and use it to access the server's protected resource.
    * *Attack Client Output Example:*

        ```bash
        --- Attempting Session Hijack ---
        Successfully read session ID from file: [UNIQUE_SESSION_ID]
        Accessing dashboard with hijacked session ID: [UNIQUE_SESSION_ID]
        Hijacked session access status: 200
        Hijacked session content:
        <h1>Welcome, testuser!</h1><p>This is your confidential information:</p><pre>{...}</pre><p><a href='/logout'>Logout</a></p>

        --- Session Hijack SUCCESSFUL! ---
        Successfully accessed the dashboard using the hijacked session ID.
        The attacker has gained access to 'testuser's confidential information.
        Attack Client operations completed.
        ```

### Verifying Session Hijack Success

* If the `attack_client.py` output displays the message " `--- Session Hijack SUCCESSFUL! ---` " and the dashboard content containing the legitimate user's (`testuser`) information, then the session hijack was successful.

## Disclaimer

The code in this repository is developed **solely for educational and demonstration purposes**.

* Unauthorized use or use for malicious purposes on actual systems or networks is **strictly prohibited**.
* The developer is not responsible for any damages caused by the misuse or unauthorized use of this code.
* This repository is intended to contribute to understanding the threat of session hijacking and improving knowledge for developing more secure web applications.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
