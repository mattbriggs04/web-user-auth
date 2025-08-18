from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import os
import mimetypes
import json 

class Router():
    _instance = None
    routes = { "GET": {}, "POST": {}}

    def add_route(self, method: str, path: str, handler_fn):
        method = method.upper()
        if method in self.routes:
            self.routes[method][path] = handler_fn
        else:
            raise ValueError(f"add_route error: invalid method '{method}'")

    def add_get_route(self, path: str, handler_fn):
        self.add_route("GET", path, handler_fn)

    def add_post_route(self, path: str, handler_fn):
        self.add_route("POST", path, handler_fn)

    def retrieve_route_fn(self, method: str, path: str):
        method = method.upper()
        return self.routes.get(method, {}).get(path)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Router, cls).__new__(cls)
        return cls._instance
    
class RequestHandler(BaseHTTPRequestHandler):
    router = Router() # stores all of the functions for methods

    def do_GET(self):
        handler_fn = self.router.retrieve_route_fn("GET", self.path)
        if not handler_fn:
            self.send_error(HTTPStatus.NOT_FOUND, f"{self.path} route not found")
            return
        
        if self.path == '/':
            # special case: a request for the root dir is looking for an html file (index.html)
            mime_type = "text/html"
        else:
            # handle files based on file extension
            mime_type, encoding = mimetypes.guess_type(self.path)
            if mime_type is None:
                mime_type = "application/octet-stream"
        
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime_type)
        self.end_headers()

        # get content from handler function and write out as bytes
        content: str = handler_fn()
        self.wfile.write(content.encode("utf-8"))

    def do_POST(self):
        handler_fn = self.router.retrieve_route_fn("POST", self.path)
        if handler_fn is None:
            self.send_error(HTTPStatus.NOT_FOUND, f"{self.path} route not found")
            return

        try:
            # read length bytes to get body
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")

            # pass in the body to the handler function
            res = handler_fn(body)
            
            # handle the results of the handler function
            if isinstance(res, dict):
                content = json.dumps(res)
                mime_type = "application/json"
            else:
                content = res
                mime_type = "text/plain"

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", mime_type)
            self.end_headers()

            # output the return value of the handler function
            self.wfile.write(content.encode("utf-8"))
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))



class AppServer():
    def __init__(self, ip: str='localhost', port: int=8020):
        self.ip = ip
        self.port = port

    def start_server(self):
        server = HTTPServer((self.ip, self.port), RequestHandler, bind_and_activate=True)
        print(f"Server started on http://{self.ip}:{self.port}")
        server.serve_forever()
