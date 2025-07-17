import http.server
import socketserver
import urllib.parse
import uuid
import json
import time
import http.cookies # <-- Add this import statement

# Server settings
HOST = '127.0.0.1'
PORT = 8000

# Session and user information managed in memory (simple)
# In a real application, a database would be used
sessions = {}  # {session_id: {'user_id': '...', 'last_active': timestamp}}
users = {}     # {user_id: {'password': '...', 'sample_info': '...'}}

# Session timeout (seconds)
SESSION_TIMEOUT = 300 # 5 minutes

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='text/html', cookies=None):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        if cookies:
            for name, value in cookies.items():
                self.send_header('Set-Cookie', f"{name}={value}; Path=/; HttpOnly; Max-Age={SESSION_TIMEOUT}")
        self.end_headers()

    def _get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        return urllib.parse.parse_qs(post_data)

    def _get_session_id(self):
        cookies_header = self.headers.get('Cookie')
        if cookies_header:
            cookies = http.cookies.SimpleCookie(cookies_header) # Now http.cookies will be available
            if 'session_id' in cookies:
                return cookies['session_id'].value
        return None

    def _validate_session(self):
        session_id = self._get_session_id()
        if session_id and session_id in sessions:
            session_data = sessions[session_id]
            # Session timeout check
            if (time.time() - session_data['last_active']) < SESSION_TIMEOUT:
                session_data['last_active'] = time.time() # Update active time
                return session_data['user_id']
            else:
                del sessions[session_id] # Delete expired session
        return None

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self._set_headers()
            self.wfile.write(b"<h1>Welcome to the Session Hijacking Demo Server!</h1>")
            self.wfile.write(b"<p>Go to <a href='/register'>/register</a> to create an account.</p>")
            self.wfile.write(b"<p>Go to <a href='/login'>/login</a> to log in.</p>")
            self.wfile.write(b"<p>Go to <a href='/dashboard'>/dashboard</a> to see your info (requires login).</p>")
        elif path == '/register':
            self._set_headers()
            self.wfile.write(b"<h1>Register</h1>")
            self.wfile.write(b"<form method='POST' action='/register'>")
            self.wfile.write(b"Username: <input type='text' name='username'><br>")
            self.wfile.write(b"Password: <input type='password' name='password'><br>")
            self.wfile.write(b"<input type='submit' value='Register'>")
            self.wfile.write(b"</form>")
        elif path == '/login':
            self._set_headers()
            self.wfile.write(b"<h1>Login</h1>")
            self.wfile.write(b"<form method='POST' action='/login'>")
            self.wfile.write(b"Username: <input type='text' name='username'><br>")
            self.wfile.write(b"Password: <input type='password' name='password'><br>")
            self.wfile.write(b"<input type='submit' value='Login'>")
            self.wfile.write(b"</form>")
        elif path == '/dashboard':
            user_id = self._validate_session()
            if user_id:
                user_data = users.get(user_id, {})
                self._set_headers()
                self.wfile.write(f"<h1>Welcome, {user_id}!</h1>".encode('utf-8'))
                self.wfile.write(b"<p>This is your confidential information:</p>")
                self.wfile.write(f"<pre>{json.dumps(user_data, indent=2)}</pre>".encode('utf-8'))
                self.wfile.write(b"<p><a href='/logout'>Logout</a></p>")
            else:
                self._set_headers(401)
                self.wfile.write(b"<h1>Unauthorized</h1>")
                self.wfile.write(b"<p>Please <a href='/login'>log in</a> to access the dashboard.</p>")
        elif path == '/logout':
            session_id = self._get_session_id()
            if session_id in sessions:
                del sessions[session_id]
            self._set_headers(cookies={'session_id': 'deleted; Expires=Thu, 01 Jan 1970 00:00:00 GMT'}) # Delete cookie
            self.wfile.write(b"<h1>Logged Out</h1>")
            self.wfile.write(b"<p>You have been logged out. <a href='/login'>Log in again</a></p>")
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        post_data = self._get_post_data()

        username = post_data.get('username', [''])[0]
        password = post_data.get('password', [''])[0]

        if path == '/register':
            if username and password:
                if username in users:
                    self._set_headers(409)
                    self.wfile.write(b"<h1>Registration Failed</h1>")
                    self.wfile.write(b"<p>Username already exists. <a href='/register'>Try again</a></p>")
                else:
                    # Save user data (here, sample information is also registered)
                    users[username] = {
                        'password': password,
                        'sample_info': f"This is confidential data for {username}.",
                        'email': f"{username}@example.com"
                    }
                    self._set_headers(201)
                    self.wfile.write(b"<h1>Registration Successful!</h1>")
                    self.wfile.write(b"<p>You can now <a href='/login'>log in</a>.</p>")
            else:
                self._set_headers(400)
                self.wfile.write(b"<h1>Registration Failed</h1>")
                self.wfile.write(b"<p>Username and password are required. <a href='/register'>Try again</a></p>")
        elif path == '/login':
            if username in users and users[username]['password'] == password:
                session_id = str(uuid.uuid4()) # Generate a unique session ID
                sessions[session_id] = {
                    'user_id': username,
                    'last_active': time.time()
                }
                self._set_headers(cookies={'session_id': session_id})
                self.wfile.write(b"<h1>Login Successful!</h1>")
                self.wfile.write(b"<p>Redirecting to <a href='/dashboard'>dashboard</a>...</p>")
                # In a real web app, a redirect header would be sent
            else:
                self._set_headers(401)
                self.wfile.write(b"<h1>Login Failed</h1>")
                self.wfile.write(b"<p>Invalid username or password. <a href='/login'>Try again</a></p>")
        else:
            self.send_error(404, "Not Found")

def run_server():
    with socketserver.TCPServer((HOST, PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Serving HTTP on {HOST}:{PORT}...")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer is shutting down...")
            httpd.server_close()

if __name__ == "__main__":
    run_server()
