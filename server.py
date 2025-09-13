#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
import socket
import sys

class SimpleHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        print(f"GET请求来自客户端: {client_ip} -> {self.path}")
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Python HTTP 测试页面</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .api-test { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #005a87; }
        .result { background: white; border: 1px solid #ddd; padding: 10px; margin-top: 10px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Python HTTP 服务器测试页面</h1>
        <p>服务器运行时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        
        <div class="api-test">
            <h2>API 测试</h2>
            <button onclick="testAPI('/api/hello')">测试 Hello API</button>
            <button onclick="testAPI('/api/time')">获取服务器时间</button>
            <button onclick="testAPI('/api/status')">服务器状态</button>
            <div id="result" class="result" style="display:none;"></div>
        </div>
        
        <div class="api-test">
            <h2>POST 测试</h2>
            <input type="text" id="nameInput" placeholder="输入你的名字" style="padding: 8px; margin-right: 10px;">
            <button onclick="testPOST()">发送 POST 请求</button>
            <div id="postResult" class="result" style="display:none;"></div>
        </div>
    </div>

    <script>
        function testAPI(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').innerHTML = '<strong>响应:</strong><br>' + JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').innerHTML = '<strong>错误:</strong> ' + error;
                });
        }
        
        function testPOST() {
            const name = document.getElementById('nameInput').value;
            fetch('/api/greet', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('postResult').style.display = 'block';
                document.getElementById('postResult').innerHTML = '<strong>响应:</strong><br>' + JSON.stringify(data, null, 2);
            })
            .catch(error => {
                document.getElementById('postResult').style.display = 'block';
                document.getElementById('postResult').innerHTML = '<strong>错误:</strong> ' + error;
            });
        }
    </script>
</body>
</html>
            """
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == '/api/hello':
            self.send_json_response({'message': 'Hello, World!', 'status': 'success'})
            
        elif self.path == '/api/time':
            self.send_json_response({
                'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': datetime.now().timestamp()
            })
            
        elif self.path == '/api/status':
            self.send_json_response({
                'server': 'Python HTTP Server',
                'status': 'running',
                'version': '1.0.0'
            })
            
        else:
            self.send_error(404, 'Page not found')
    
    def do_POST(self):
        client_ip = self.client_address[0]
        print(f"POST请求来自客户端: {client_ip} -> {self.path}")
        if self.path == '/api/greet':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                name = data.get('name', 'Anonymous')
                
                response = {
                    'greeting': f'你好, {name}!',
                    'received_data': data,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.send_json_response(response)
                
            except json.JSONDecodeError:
                self.send_json_response({'error': 'Invalid JSON'}, status=400)
        else:
            self.send_error(404, 'API endpoint not found')
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

class DualStackHTTPServer(HTTPServer):
    address_family = socket.AF_INET6

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=False)

        # 启用双栈模式 (IPv4 + IPv6)
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except Exception as e:
                self.server_close()
                raise e

def run_server(port=8000):
    try:
        # 尝试IPv6双栈服务器
        server_address = ('::', port)
        httpd = DualStackHTTPServer(server_address, SimpleHTTPHandler)
        print(f'服务器启动在所有网络接口 (IPv4 + IPv6)，端口 {port}')
        print(f'本地访问:')
        print(f'  IPv4: http://localhost:{port}/')
        print(f'  IPv6: http://[::1]:{port}/')
        print(f'局域网访问:')
        print(f'  IPv4: http://192.168.3.214:{port}/')
        print(f'  IPv6: http://[您的IPv6地址]:{port}/')

    except Exception as e:
        # 如果IPv6失败，回退到IPv4
        print(f'IPv6启动失败: {e}')
        print('回退到IPv4模式...')
        server_address = ('0.0.0.0', port)
        httpd = HTTPServer(server_address, SimpleHTTPHandler)
        print(f'服务器启动在所有IPv4接口，端口 {port}')
        print(f'本地访问: http://localhost:{port}/')
        print(f'局域网访问: http://192.168.3.214:{port}/')

    print('按 Ctrl+C 停止服务器')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已停止')
        httpd.server_close()

if __name__ == '__main__':
    run_server()