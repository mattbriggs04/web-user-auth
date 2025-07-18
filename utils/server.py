from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class Router():
    def __init__(self):
        self.routes = {}
    
    def add_route(self, path: str, handler_fn):
        self.routes[path] = handler_fn

    def retrieve_route(self, path: str):
        return self.routes.get(path)
    
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"")

def start_server(ip: str='localhost', port: int=8020):
    server = HTTPServer((ip, port), RequestHandler, bind_and_activate=True)
    print(f"Server started on http://{ip}:{port}")
    server.serve_forever()