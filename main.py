#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import requests
import os


class AuthLoopbackServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        parsed_path = urlparse(self.path)
        queries = parsed_path.query.split("?")

        pomerium_query = [query for query in queries if "pomerium_jwt" in query]

        if len(pomerium_query) == 1 and parsed_path.path == "/jwt":
            token = pomerium_query[0].split("=")[1]
            fs = open(f"{os.path.expanduser('~/.pomerium_jwt')}", "w+")
            fs.seek(0)
            fs.write(token)
            fs.truncate()
            print("JWT written to ~/.pomerium_jwt")
            quit()
        else:
            print("An error has occured")
            quit()


if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8000), AuthLoopbackServer)

    resp = requests.get(
        "https://{{VAULT_ADDR}}/.pomerium/api/v1/login?pomerium_redirect_uri=http://localhost:8000/jwt"
    )

    print(f"Visit the following URL in your browser: \n\n {resp.text}\n")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
