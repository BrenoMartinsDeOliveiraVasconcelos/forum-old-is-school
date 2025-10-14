import http.server
import socketserver

PORT = 8000

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
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("Blocked files: *.py, /.*")
    httpd.serve_forever()