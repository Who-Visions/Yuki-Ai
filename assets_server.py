
import http.server
import socketserver
import os
import sys

# Configuration
PORT = 8083
DIRECTORY = r"C:\Yuki_Local\Cosplay_Lab\Renders"

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def translate_path(self, path):
        # Ensure we serve from the specific DIRECTORY
        # SimpleHTTPRequestHandler uses os.getcwd() by default or we can override
        path = super().translate_path(path)
        rel_path = os.path.relpath(path, os.getcwd())
        return os.path.join(DIRECTORY, rel_path)

# Change working directory so SimpleHTTPRequestHandler serves from there
# This is easier than overriding translate_path complexly
try:
    os.chdir(DIRECTORY)
except FileNotFoundError:
    print(f"Error: Directory not found: {DIRECTORY}")
    sys.exit(1)

Handler = CORSRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving assets at http://localhost:{PORT}")
    print(f"Root Directory: {DIRECTORY}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
