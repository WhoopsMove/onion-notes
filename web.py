import asyncio
from flask import (Flask, g, render_template)

class Web:
    def __init__(self):
        self.message = None
        self.app = Flask(__name__)
        self.define_routes()

    security_headers = [
            # Blocks page from being displayed in an iframe
            ("X-Frame-Options", "DENY"),
            # Stops page loading if XSS detected (on some browsers)
            # CSP takes care of this better if supported
            ("X-Xss-Protection", "1; mode=block"),
            # MIME Type (e.g. Content-Type header) should be followed and not changed
            ("X-Content-Type-Options", "nosniff"),
            # Controles how much information is passed in Referer header
            # In this case, Referer header is omitted with no-referrer directive
            ("Referrer-Policy", "no-referrer"),
            # An "User Agent" of sorts for the server
            # Describes the software that handled the request
            ("Server", "Onion-Notes"),
        ]

    def define_routes(self):
        @self.app.after_request
        def add_security_headers(res):
            default_csp = "default-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'; img-src 'self' data:;"
            for header, value in self.security_headers:
                res.headers.set(header, value)
            res.headers.set("Content-Security-Policy", default_csp)
            return res

        @self.app.route('/')
        def index():
            return render_template("default.html", message=self.get_message())

    def get_message(self):
        return self.message

    def run(self):
        self.app.run()

    def set_msg(self, msg):
        self.message = msg