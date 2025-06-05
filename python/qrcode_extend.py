import os
import socket
import threading
import qrcode
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

def get_local_ip():
    """获取本机IP地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def start_server(port, directory):
    """启动HTTP服务器"""
    # 切换到指定目录
    os.chdir(directory)
    
    # 创建服务器
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("", port), handler)
    
    print(f"服务器启动在 http://{get_local_ip()}:{port}")
    httpd.serve_forever()

def generate_qrcode(url, filename, output_dir="qrcodes"):
    """生成包含文件URL的二维码"""
    # 确保输出目录存在（使用绝对路径）
    output_dir = os.path.abspath(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成唯一的二维码文件名
    timestamp = int(time.time())
    # 移除文件名中可能包含的路径分隔符，只保留文件名部分
    safe_filename = os.path.basename(filename.replace('/', '_').replace('\\', '_'))
    qrcode_filename = f"{safe_filename}_{timestamp}.png"
    output_path = os.path.join(output_dir, qrcode_filename)
    
    file_url = f"{url}/{filename}"
    img = qrcode.make(file_url)
    img.save(output_path)
    print(f"二维码已生成: {output_path}")
    print(f"二维码内容: {file_url}")
    return output_path

def create_file_qrcode(file_path, base_url, server_directory=None, port=8000):
    try:
        # 如果未指定服务器目录，使用文件所在目录
        if server_directory is None:
            server_directory = os.path.dirname(os.path.abspath(file_path))
        else:
            server_directory = os.path.abspath(server_directory)
            
        # 检查文件是否存在
        abs_file_path = os.path.abspath(file_path)
        if not os.path.exists(abs_file_path):
            return {
                "status": "failure",
                "message": f"文件不存在: {file_path}"
            }
            
        # 检查文件是否在服务器根目录下
        if not abs_file_path.startswith(server_directory):
            return {
                "status": "failure",
                "message": f"文件不在服务器根目录 '{server_directory}' 下"
            }
            
        # 计算相对于服务器根目录的路径
        rel_path = os.path.relpath(abs_file_path, server_directory)
        # 统一使用正斜杠作为URL路径分隔符
        filename = rel_path.replace('\\', '/')
        
        # 检查服务器是否已经运行
        server_running = False
        for thread in threading.enumerate():
            if thread.name == "qrcode_server":
                server_running = True
                break
                
        # 如果服务器未运行，启动新的服务器
        if not server_running:
            server_thread = threading.Thread(
                target=start_server, 
                args=(port, server_directory),
                name="qrcode_server"
            )
            server_thread.daemon = True
            server_thread.start()
            time.sleep(1)
            
        # 生成二维码
        qrcode_dir = os.path.join(os.getcwd(), "qrcodes")
        qrcode_path = generate_qrcode(base_url, filename, qrcode_dir)
        
        return {
            "status": "success",
            "qrcode_path": qrcode_path,
            "url": f"{base_url}/{filename}",
            "server_address": f"{base_url}"
        }
        
    except Exception as e:
        return {
            "status": "failure",
            "message": f"生成二维码失败: {str(e)}"
        }