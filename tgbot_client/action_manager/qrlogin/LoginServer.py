"""
扫描二维码登录服务，供登录使用
"""
from http.server import BaseHTTPRequestHandler
from typing import Any
from tgbot_client.create_qr import tglogin_name


class LoginServer(BaseHTTPRequestHandler):
    """..."""

    def do_GET(self):
        """..."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes(
                    f"""
                    <html>
                        <head>
                            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
                            <title>TGuser登陆</title>
                        </head>
                        <body>
                            <p align="center"><img src="/tguserlogin.jpg">TGuser登录</p>
                        </body>
                    </html>
                """,
                    "utf8",
                )
            )
        elif self.path == "/tguserlogin.jpg":
            self.send_response(200)
            self.send_header("content-type", "image/jpg")
            self.end_headers()
            # noinspection PyUnresolvedReferences
            self.wfile.write(self.server.qrData)
        elif self.path == "/close":
            self.server.server_close()
        else:
            self.send_response(404)

    def log_message(self, _format: str, *args: Any) -> None:
        """..."""
        return
