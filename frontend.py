import http.server
import socketserver
from sys import argv

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom request handler to block access to specific files and directories.
    """
    forbidden_endings = [".py", ".md", ".sql", ".json", ".txt", ".sh"]
    forbidden_starts = ["/."]
    def do_GET(self):
        starts_forbidden = any(self.path.startswith(s) for s in self.forbidden_starts)
        ends_forbidden = any(self.path.endswith(e) for e in self.forbidden_endings)

        if starts_forbidden or ends_forbidden:
            self.send_error(403, "Forbidden")
            return
        
        return super().do_GET()

if __name__ == "__main__":
    HOST = "localhost"
    PORT = "8080"

    if len(argv) > 2:
        HOST = argv[1]
        PORT = argv[2]
    else:
        print(f"Usage: {argv[0]} <host> <port>")
        exit(1) 

    Handler = MyHttpRequestHandler
    with socketserver.TCPServer((HOST, int(PORT)), Handler) as httpd:
        print(f"Serving at http://{HOST}:{PORT}")
        httpd.serve_forever()
