#!/usr/bin/env python3
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        resp = {
            "status": "ok",
            "service": "app",
            "env": os.getenv("ENV_NAME", "local")
        }
        self.wfile.write(json.dumps(resp).encode())


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads."""


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    server = ThreadedHTTPServer(('', port), Handler)
    server.serve_forever()
