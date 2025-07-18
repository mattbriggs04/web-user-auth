from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import os

class Router():
    _instance = None

    def __init__(self):
        self.routes = {}
    
    def add_get_route(self, path: str, route_fn):
        self.routes[path] = route_fn

    def add_route(self, path: str, handler_fn):
        self.routes[path] = handler_fn

    def retrieve_route_fn(self, path: str):
        return self.routes.get(path)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Router, cls).__new__(cls)
        return cls._instance
    
class RequestHandler(BaseHTTPRequestHandler):
    router = Router()

    def do_GET(self):
        route_fn = self.router.retrieve_route_fn(self.path)
        if not route_fn:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(route_fn().encode("utf-8"))

class AppServer():
    def __init__(self, ip: str='localhost', port: int=8020):
        self.ip = ip
        self.port = port

    def start_server(self):
        server = HTTPServer((self.ip, self.port), RequestHandler, bind_and_activate=True)
        print(f"Server started on http://{self.ip}:{self.port}")
        server.serve_forever()
