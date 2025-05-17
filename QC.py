import os
import qrcode
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser
import time

def get_local_ip():
    """获取本机IP地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要真正连接
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

def main():
    # 配置
    port = 8000
    
    # 获取服务器根目录
    server_directory = input("请输入服务器根目录路径: ")
    server_directory = os.path.abspath(server_directory)
    
    # 在新线程中启动服务器
    server_thread = threading.Thread(target=start_server, args=(port, server_directory))
    server_thread.daemon = True
    server_thread.start()
    
    # 生成URL基础部分
    local_ip = get_local_ip()
    base_url = f"http://{local_ip}:{port}"
    
    # 循环生成二维码
    while True:
        print("\n选项:")
        print("1. 生成新的文件二维码")
        print("2. 退出")
        
        choice = input("请选择操作 (1/2): ")
        
        if choice == '1':
            # 获取文件路径
            file_path = input("请输入要共享的文件路径: ")
            
            # 检查文件是否在服务器根目录下
            abs_file_path = os.path.abspath(file_path)
            if not abs_file_path.startswith(server_directory):
                # 如果不在服务器根目录下，计算相对路径或提示错误
                print(f"警告: 文件不在服务器根目录 '{server_directory}' 下")
                print("请确保文件位于服务器根目录或其子目录中")
                continue
            
            # 计算相对于服务器根目录的路径
            rel_path = os.path.relpath(abs_file_path, server_directory)
            # 统一使用正斜杠作为URL路径分隔符
            filename = rel_path.replace('\\', '/')
            
            # 生成二维码（使用当前工作目录下的qrcodes文件夹）
            current_dir = os.getcwd()
            qrcode_dir = os.path.join(current_dir, "qrcodes")
            qrcode_path = generate_qrcode(base_url, filename, qrcode_dir)
            
            # 打开二维码
            webbrowser.open(qrcode_path)
            
        elif choice == '2':
            print("服务器已停止")
            break
        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main()