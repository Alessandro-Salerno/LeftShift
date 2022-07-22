from leftshift.structures import LeftShiftRequest, LeftShiftResponse
from http.server          import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import json


class LeftShiftHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers['Content-length'])))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        message = json.dumps(self.server.leftshift_server.handle(req['content_type'], req['content']).__dict__)
        self.wfile.write(bytes(message, 'utf8'))

    def do_GET(self):
        self.send_response(501)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>LeftShift makeshift page</title>
            </head>
            <body>
                <h1>LeftShift</h1> 
                You're trying to visit content hosted on a LeftShift Server. <br>
                LeftShift does not support traditional HTTP Requests such as those issued by your browser, please use a LeftShift client. <br> <br>

                LeftShift GitHub: <a href="https://github.com/Alessandro-Salerno/LeftShift">https://github.com/Alessandro-Salerno/LeftShift</a>
            </body>
            </html>
        """, 'utf8'))


class LeftShiftBackend(ThreadingHTTPServer):
    def __init__(self, leftshift_server, *args, **kwargs):
        self.leftshift_server = leftshift_server
        super().__init__(*args, **kwargs)


class LeftShiftServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.handlers = {}

        def default_leftshift_ok_handler(content):
            return LeftShiftResponse(
                content_type='leftshift-ok',
                content='Hello, world!'
            )

        self.add_handler('leftshift-ping', default_leftshift_ok_handler)

    def run(self):
        server_thread = threading.Thread(target=self._run)
        server_thread.start()

    def add_handler(self, content_type, request_handler):
        self.handlers.__setitem__(content_type, request_handler)

    def handler(self, content_type):
        def inner(request_handler):
            self.add_handler(content_type, request_handler)

        return inner

    def handler_not_found(self, content_type, content):
        return LeftShiftResponse(
            content_type='leftshift-error',
            content=f'leftshift-invalid-type {content_type}'
        )

    def handle(self, content_type, content):
        return self._handle(content_type, content)

    def _handle(self, content_type, content):
        if content_type in self.handlers.keys():
            return self.handlers[content_type](content)

        return self.handler_not_found(content_type, content)

    def _run(self):
        with LeftShiftBackend(self, (self.host, self.port), LeftShiftHandler) as self.http_server:
            self.http_server.serve_forever()
