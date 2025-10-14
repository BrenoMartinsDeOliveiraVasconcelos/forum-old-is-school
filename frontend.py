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
    forbidden_endings = [".py", ".md", ".sql", ".json", ".txt", ".sh"]
    forbidden_starts = ["/."]
    def do_GET(self):
        error = False

        for ending in self.forbidden_endings:
            if self.path.endswith(ending):
                error = True
                break

        for start in self.forbidden_starts:
            if self.path.startswith(start):
                error = True
                break

        if error:
            self.send_error(403, "Forbidden")
            return

        return super().do_GET()

Handler = MyHttpRequestHandler
with socketserver.TCPServer((HOST, int(PORT)), Handler) as httpd:
    print(f"Serving at http://{HOST}:{PORT}")
    httpd.serve_forever()