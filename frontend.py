import http.server
import socketserver
from sys import argv

HOST = "localhost"
PORT = "8080"

if len(argv) > 2:
    HOST = argv[1]
    PORT = argv[2]
else:
    print(f"Usage: {argv[0]} <host> <port>")
    exit(1) 

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom request handler to block access to specific files and directories.
    """
    def do_GET(self):
        if not self.path.endswith(".html"):
            self.send_error(404, 'Not found')
            return

        return super().do_GET()

Handler = MyHttpRequestHandler
with socketserver.TCPServer((HOST, int(PORT)), Handler) as httpd:
    print(f"Serving at http://{HOST}:{PORT}")
    print("Blocked files: *.py, /.*")
    httpd.serve_forever()