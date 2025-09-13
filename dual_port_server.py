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
            content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python HTTP Server</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 { 
            color: #333; 
            text-align: center; 
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .info-card { 
            background: #f8f9ff; 
            padding: 20px; 
            margin: 20px 0; 
            border-radius: 10px; 
            border-left: 5px solid #667eea;
        }
        .api-section { 
            background: #f0fff4; 
            padding: 20px; 
            margin: 20px 0; 
            border-radius: 10px; 
            text-align: center;
        }
        .btn { 
            background: #667eea; 
            color: white; 
            padding: 12px 20px; 
            text-decoration: none; 
            border-radius: 25px; 
            margin: 10px; 
            display: inline-block;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        .btn:hover { 
            background: #5a67d8; 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .status-item {
            background: #e6fffa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #81e6d9;
        }
        .port-info {
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        @media (max-width: 600px) {
            .container { 
                margin: 10px; 
                padding: 20px; 
            }
            h1 { 
                font-size: 2em; 
            }
            .btn { 
                display: block; 
                margin: 10px 0; 
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Python HTTP Server 🚀</h1>
        
        <div class="port-info">
            <h3>🚀 多端口服务</h3>
            <p><strong>同时监听端口:</strong> 80 (HTTP标准) + 8000 (开发)</p>
            <p>可通过 <code>http://localhost</code> 或 <code>http://localhost:8000</code> 访问</p>
        </div>
        
        <div class="info-card">
            <h3>📊 连接信息</h3>
            <p><strong>⏰ 当前时间:</strong> """ + current_time + """</p>
            <p><strong>🌐 您的IP地址:</strong> """ + client_ip + """</p>
            <p><strong>📍 请求路径:</strong> """ + path + """</p>
            <p><strong>🔧 请求方法:</strong> """ + method + """</p>
        </div>
        
        <div class="api-section">
            <h3>🛠️ API 测试接口</h3>
            <a href="/api/time" class="btn">⏱️ 获取服务器时间</a>
            <a href="/api/hello" class="btn">👋 Hello API</a>
            <a href="/api/status" class="btn">📊 服务器状态</a>
        </div>
        
        <div class="status-grid">
            <div class="status-item">
                <h4>✅ 服务状态</h4>
                <p>运行正常</p>
            </div>
            <div class="status-item">
                <h4>⚡ 响应速度</h4>
                <p>极速</p>
            </div>
            <div class="status-item">
                <h4>🔧 协议版本</h4>
                <p>HTTP/1.1</p>
            </div>
            <div class="status-item">
                <h4>📝 编码</h4>
                <p>UTF-8</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>Powered by Python Socket Server ⚡</p>
        </div>
    </div>
</body>
</html>"""
            content_type = "text/html; charset=utf-8"
            
        elif path == '/api/time':
            content = '{"time": "' + current_time + '", "client_ip": "' + client_ip + '", "timestamp": ' + str(time.time()) + '}'
            content_type = "application/json; charset=utf-8"
            
        elif path == '/api/hello':
            content = '{"message": "Hello from Python! 👋", "client_ip": "' + client_ip + '", "server_time": "' + current_time + '"}'
            content_type = "application/json; charset=utf-8"
            
        elif path == '/api/status':
            content = '{"server": "Python Socket Server", "status": "running", "version": "1.0.0", "ports": [80, 8000], "client_ip": "' + client_ip + '", "server_time": "' + current_time + '"}'
            content_type = "application/json; charset=utf-8"
            
        else:
            content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - 页面未找到</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 600px; 
            margin: 50px auto; 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 { 
            color: #d63031; 
            font-size: 3em; 
            margin-bottom: 20px;
        }
        .error-info { 
            background: #ffe0e0; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
            border-left: 5px solid #d63031;
        }
        .btn { 
            background: #0984e3; 
            color: white; 
            padding: 15px 30px; 
            text-decoration: none; 
            border-radius: 25px; 
            display: inline-block;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        .btn:hover { 
            background: #74b9ff; 
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚫 404</h1>
        <h2>页面未找到</h2>
        
        <div class="error-info">
            <p><strong>请求页面:</strong> """ + path + """</p>
            <p><strong>错误时间:</strong> """ + current_time + """</p>
            <p><strong>您的IP:</strong> """ + client_ip + """</p>
        </div>
        
        <a href="/" class="btn">🏠 返回首页</a>
        
        <div style="margin-top: 30px; color: #666;">
            <small>Python Socket Server - 404 Error</small>
        </div>
    </div>
</body>
</html>"""
            content_type = "text/html; charset=utf-8"
        
        # 编码内容
        content_bytes = content.encode('utf-8')
        content_length = len(content_bytes)
        
        # 构建HTTP响应
        if path.startswith('/api/') and path not in ['/api/time', '/api/hello', '/api/status']:
            status_line = "HTTP/1.1 404 Not Found\r\n"
        elif path not in ['/', '', '/api/time', '/api/hello', '/api/status']:
            status_line = "HTTP/1.1 404 Not Found\r\n"
        else:
            status_line = "HTTP/1.1 200 OK\r\n"
            
        headers = f"""Content-Type: {content_type}\r
Content-Length: {content_length}\r
Connection: close\r
Server: Python-Dual-Port-Server\r
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
    """启动单个端口的HTTP服务器"""
    # 确定地址族
    if ':' in host:
        family = socket.AF_INET6
        print(f"[端口 {port}] 启动IPv6服务器在 [{host}]:{port}")
    else:
        family = socket.AF_INET
        print(f"[端口 {port}] 启动IPv4服务器在 {host}:{port}")
    
    # 创建socket
    server_socket = socket.socket(family, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # IPv6双栈支持
    if family == socket.AF_INET6:
        try:
            server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            print(f"[端口 {port}] 启用IPv6双栈支持")
        except:
            print(f"[端口 {port}] IPv6双栈支持失败，仅IPv6")
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"[端口 {port}] 绑定成功，开始监听连接...")
        
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
                
            except Exception as e:
                if "interrupted" not in str(e).lower():
                    print(f"[端口 {port}] 接受连接时出错: {e}")
                break
                
    except Exception as e:
        print(f"[端口 {port}] 服务器启动失败: {e}")
        if port == 80:
            print("提示：监听80端口需要管理员权限，请使用 sudo python3 script.py")
        raise e
    finally:
        try:
            server_socket.close()
        except:
            pass
        print(f"[端口 {port}] 服务器已停止")

def start_server_thread(host, port):
    """在独立线程中启动服务器"""
    try:
        start_server(host, port)
    except Exception as e:
        print(f"[端口 {port}] 服务器线程异常: {e}")

def main():
    ports = [80, 8000]  # 监听80和8000端口
    threads = []
    
    print("=== Python双端口HTTP服务器 ===")
    print(f"准备启动端口: {ports}")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for port in ports:
        try:
            # 为每个端口创建独立线程
            server_thread = threading.Thread(
                target=start_server_thread,
                args=('::', port),
                daemon=True
            )
            server_thread.start()
            threads.append(server_thread)
            print(f"✅ 端口 {port} 线程启动成功")
            time.sleep(0.1)  # 稍微延迟避免日志混乱
        except Exception as e:
            print(f"❌ 端口 {port} 启动失败: {e}")
            # 如果IPv6失败，尝试IPv4
            try:
                server_thread = threading.Thread(
                    target=start_server_thread,
                    args=('0.0.0.0', port),
                    daemon=True
                )
                server_thread.start()
                threads.append(server_thread)
                print(f"✅ 端口 {port} IPv4模式启动成功")
            except Exception as e2:
                print(f"❌ 端口 {port} IPv4也失败: {e2}")
    
    if threads:
        print()
        print("🚀 服务器启动完成！")
        print("📡 监听端口:", ports)
        print("🌐 访问地址:")
        print("   http://localhost        (端口80)")
        print("   http://localhost:8000   (端口8000)")
        print()
        print("⭐ 提示:")
        print("   - 如果80端口启动失败，请使用: sudo python3 script.py")
        print("   - 按 Ctrl+C 停止所有服务器")
        print()
        
        try:
            # 保持主线程运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  正在停止所有服务器...")
            print("👋 服务器已停止")
    else:
        print("❌ 所有端口启动失败！")

if __name__ == '__main__':
    main()
