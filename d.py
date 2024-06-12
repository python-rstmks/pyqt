from http.server import BaseHTTPRequestHandler, HTTPServer

# リクエストを処理するハンドラクラスを定義
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # リクエストの情報を表示
        print(f"Received request from {self.client_address[0]} for URL: {self.path}")

        # レスポンスのステータスコードを設定
        self.send_response(200)
        # レスポンスヘッダーを設定
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # レスポンスボディを設定（ここでは単純にリクエスト情報を表示）
        self.wfile.write(f"Hello from the server! You requested: {self.path}".encode())

# サーバーの情報
host = 'localhost'  # ホスト名を変更して必要に応じて公開
port = 8000  # 使用するポート番号を指定

# サーバーを作成してリクエストを待ち受ける
server = HTTPServer((host, port), SimpleHTTPRequestHandler)
print(f"Server started on {host}:{port}")

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
print("Server stopped.")
