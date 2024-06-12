

import http.server
import socketserver

PROXY_PORT = 8080
TARGET_HOST = "localhost"  # プロキシ先のホストを指定
TARGET_PORT = 8000  # プロキシ先のポート番号を指定


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # リクエストの情報を表示
        print(f"Received request from {self.client_address[0]} for URL: {self.path}")

        # リクエストをプロキシ先に転送
        self.send_proxy_request()

        # プロキシ先からのレスポンスをクライアントに転送
        self.send_proxy_response()

    def send_proxy_request(self):
        # プロキシ先のホストとポート番号を指定
        target_host = TARGET_HOST
        target_port = TARGET_PORT

        # プロキシ先への新しいリクエストを作成
        target_request = self.requestline
        target_request += f"Host: {target_host}\r\n"
        for header, value in self.headers.items():
            if header.lower() != "host":
                target_request += f"{header}: {value}\r\n"
        target_request += "\r\n"

        # プロキシ先にリクエストを送信
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_socket:
            target_socket.connect((target_host, target_port))
            target_socket.sendall(target_request.encode())

            # プロキシ先からのレスポンスを受信
            self.target_response = target_socket.recv(4096)

    def send_proxy_response(self):
        # プロキシ先からのレスポンスをクライアントに転送
        self.send_response(200)
        for header, value in self.headers.items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(self.target_response)

# プロキシサーバーを起動
with socketserver.ThreadingTCPServer(("", PROXY_PORT), ProxyHandler) as server:
    print(f"Proxy server started on port {PROXY_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Proxy server stopped.")