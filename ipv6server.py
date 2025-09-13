#!/usr/bin/env python3
import socket
import threading
import time
from datetime import datetime

def get_client_ip(client_socket):
    """获取客户端IP地址"""
    try:
        peer = client_socket.getpeername()
        return peer[0]
    except:
        return "unknown"

def handle_request(client_socket, client_address):
    """处理单个HTTP请求"""
    try:
        # 接收请求数据
        request_data = client_socket.recv(4096).decode('utf-8')
        if not request_data:
            return
        
        # 解析请求行
        lines = request_data.split('\n')
        if not lines:
            return
            
        request_line = lines[0].strip()
        parts = request_line.split()
        if len(parts) < 2:
            return
            
        method = parts[0]
        path = parts[1]
        
        # 获取客户端IP和当前时间
        client_ip = get_client_ip(client_socket)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 记录访问日志
        print(f"[{current_time}] {method} {path} from {client_ip}")
        
        # 生成响应内容
        if path == '/' or path == '':
            content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Python HTTP Server</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>Welcome to Python HTTP Server!</p>
    <p>当前时间: {current_time}</p>
    <p>您的IP地址: {client_ip}</p>
    <p>请求路径: {path}</p>
    <p>请求方法: {method}</p>
</body>
</html>"""
            content_type = "text/html; charset=utf-8"
            
        elif path == '/api/time':
            content = f'{{"time": "{current_time}", "client_ip": "{client_ip}", "timestamp": {time.time()}}}'
            content_type = "application/json; charset=utf-8"
            
        elif path == '/api/hello':
            content = f'{{"message": "Hello from Python!", "client_ip": "{client_ip}", "server_time": "{current_time}"}}'
            content_type = "application/json; charset=utf-8"
            
        else:
            content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - 页面未找到</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #e74c3c; text-align: center; margin-bottom: 30px; }}
        .error-card {{ background: #fdf2f2; padding: 15px; margin: 15px 0; border-radius: 6px; border-left: 4px solid #e74c3c; }}
        .home-link {{ display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-top: 20px; }}
        .home-link:hover {{ background: #2980b9; }}
        .footer {{ text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚫 404 - 页面未找到</h1>
        
        <div class="error-card">
            <h3>❌ 错误信息</h3>
            <p><strong>请求页面:</strong> {path}</p>
            <p><strong>错误时间:</strong> {current_time}</p>
            <p><strong>您的IP:</strong> {client_ip}</p>
        </div>
        
        <div style="text-align: center;">
            <a href="/" class="home-link">🏠 返回首页</a>
        </div>
        
        <div class="footer">
            Python Socket Server - 404 Error
        </div>
    </div>
</body>
</html>"""
            content_type = "text/html; charset=utf-8"
        
        # 编码内容
        content_bytes = content.encode('utf-8')
        content_length = len(content_bytes)
        
        # 构建HTTP响应
        if path.startswith('/api/') and path not in ['/api/time', '/api/hello']:
            status_line = "HTTP/1.1 404 Not Found\r\n"
        elif path not in ['/', '', '/api/time', '/api/hello']:
            status_line = "HTTP/1.1 404 Not Found\r\n"
        else:
            status_line = "HTTP/1.1 200 OK\r\n"
            
        headers = f"""Content-Type: {content_type}\r
Content-Length: {content_length}\r
Connection: close\r
Server: Python-Simple-Server\r
\r
"""
        
        # 发送响应
        response = (status_line + headers).encode('utf-8') + content_bytes
        client_socket.sendall(response)
        
    except Exception as e:
        print(f"处理请求时出错: {e}")
        try:
            error_response = b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
            client_socket.sendall(error_response)
        except:
            pass
    finally:
        try:
            client_socket.close()
        except:
            pass

def start_server(host, port):
    """启动HTTP服务器"""
    # 确定地址族
    if ':' in host:
        family = socket.AF_INET6
        print(f"启动IPv6服务器在 [{host}]:{port}")
    else:
        family = socket.AF_INET
        print(f"启动IPv4服务器在 {host}:{port}")
    
    # 创建socket
    server_socket = socket.socket(family, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # IPv6双栈支持
    if family == socket.AF_INET6:
        try:
            server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            print("启用IPv6双栈支持")
        except:
            print("IPv6双栈支持失败，仅IPv6")
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"服务器启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("按 Ctrl+C 停止服务器")
        
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                # 为每个连接创建新线程
                client_thread = threading.Thread(
                    target=handle_request,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"接受连接时出错: {e}")
                continue
                
    except Exception as e:
        print(f"服务器启动失败: {e}")
    finally:
        server_socket.close()
        print("\n服务器已停止")

def main():
    port = 8000
    
    try:
        # 尝试IPv6双栈
        start_server('::', port)
    except Exception as e:
        print(f"IPv6启动失败: {e}")
        print("回退到IPv4...")
        try:
            start_server('0.0.0.0', port)
        except Exception as e2:
            print(f"IPv4启动也失败: {e2}")

if __name__ == '__main__':
    main()
