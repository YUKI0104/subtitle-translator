#!/usr/bin/env python3
"""Local dev server with CORS proxy for kuaipao.pro.

Serves static files AND proxies /proxy/kuaipao/* -> kuaipao.pro
so browsers bypass CORS restrictions.
"""

import http.server
import json
import urllib.request
import urllib.error
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
KUAIPAO_BASE = "https://kuaipao.pro/v1"


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self._send_cors()
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith("/proxy/kuaipao/"):
            self._proxy_request()
        else:
            super().do_POST()

    def _proxy_request(self):
        """Forward POST to kuaipao.pro and return response."""
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len)

        # Build target URL: /proxy/kuaipao/chat/completions → https://kuaipao.pro/v1/chat/completions
        path = self.path[len("/proxy/kuaipao/"):]
        target = f"{KUAIPAO_BASE}/{path}"

        # Forward auth header
        auth = self.headers.get("Authorization", "")
        req = urllib.request.Request(
            target,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": auth,
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self._send_cors()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self._send_cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(e.read())
        except urllib.error.URLError as e:
            self.send_response(502)
            self._send_cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": {"message": str(e.reason)}}).encode())
        except Exception as e:
            self.send_response(500)
            self._send_cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": {"message": str(e)}}).encode())

    def _send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def end_headers(self):
        super().end_headers()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = http.server.HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    print(f"🚀 Server at http://localhost:{PORT}")
    print(f"   Kuaipao proxy: http://localhost:{PORT}/proxy/kuaipao/chat/completions")
    server.serve_forever()
