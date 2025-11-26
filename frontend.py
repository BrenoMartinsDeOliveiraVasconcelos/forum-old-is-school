import http.server
import socketserver
from sys import argv
import os

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom request handler to block access to specific files and directories.
    """
    forbidden_endings = [".py", ".md", ".sql", ".json", ".sh"]
    forbidden_starts = ["/."]
    def do_GET(self):
        path_normalized = self.path[1:].removesuffix("/")
        print(path_normalized)
        starts_forbidden = any(self.path.startswith(s) for s in self.forbidden_starts)
        ends_forbidden = any(self.path.endswith(e) for e in self.forbidden_endings)
        normal_behaviour = False
        content = open("index.html", "rb").read()
        stcode = 200

        if starts_forbidden or ends_forbidden:
                content = open("error.html", "rb").read()
        elif path_normalized not in os.listdir("."):
            stcode = 404
            content = open("error404.html", "rb").read()
        else:
            normal_behaviour = True

        if not normal_behaviour:
            self.send_response(stcode) 
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            
            self.wfile.write(content)
            return
        else:
            return super().do_GET()
    

    def log_message(self, format, *args):
        log_text = f"[{self.client_address[0]}:{self.client_address[1]}] [{self.log_date_time_string()}] {format % args}"
        print(log_text)
        open("log.txt", "a").write(log_text + "\n")

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
