# MIT License

# Copyright (c) 2022 Alessandro Salerno

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from leftshift.structures import LeftShiftResponse
from http.server          import BaseHTTPRequestHandler, ThreadingHTTPServer

import threading
import json


class LeftShiftHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers['Content-length'])))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = self.server.leftshift_server.handle(req['content_type'], req['content'])
        if not isinstance(response, LeftShiftResponse):
            raise TypeError(f"Request handler for LeftShift Request '{req['content_type']}' should always return an instance of LeftShiftResponse")

        message = json.dumps(response.to_dict())
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
