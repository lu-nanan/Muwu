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
    
import os
import qrcode
from urllib.parse import urlparse

def generate_qr_code(userId, root_path, url):
    """
    生成二维码并保存至指定路径。

    参数:
        userId (int or str): 用户ID，用于创建对应的文件夹。
        root_path (str): 根路径，用于存放二维码。
        url (str): 可访问的URL，用于生成二维码。

    功能:
        1. 从URL中提取文件名，去除扩展名后作为二维码图片的文件名，后缀为.png。
        2. 生成URL的二维码。
        3. 将二维码保存至 root_path/userId/ 文件夹内。

    示例:
        输入:
            userId = 100000
            root_path = "F:/qc"
            url = "http://localhost:8082/file/100000/123.txt"
        结果:
            生成的二维码保存为 "F:/qc/100000/123.png"
    """
    try:
        # 解析URL，获取路径部分
        parsed_url = urlparse(url)
        path = parsed_url.path
        # 获取文件名（含扩展名）
        filename_with_ext = os.path.basename(path)
        # 分离文件名和扩展名
        filename, _ = os.path.splitext(filename_with_ext)
        # 定义二维码图片的文件名
        qr_filename = f"{filename}.png"
        
        # 创建目标文件夹路径
        target_dir = os.path.join(root_path, str(userId))
        os.makedirs(target_dir, exist_ok=True)
        
        # 定义二维码图片的完整路径
        qr_path = os.path.join(target_dir, qr_filename)
        
        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 保存二维码图片
        img.save(qr_path)
        
        print(f"二维码已成功保存至: {qr_path}")

        return {
            "status": "success",
            "qrcode_path": qr_path,
        }
        
    except Exception as e:
        print(f"生成二维码时出错: {e}")
        return {
            "status": "failure",
            "message": f"生成二维码时出错: {e}"
        }

# 示例调用
if __name__ == "__main__":
    user_id = 100000
    root_directory = "F:\大三下学期\移动应用开发\仓库\Muwu\python\qrcode"
    file_url = "https://63793dfe.r21.cpolar.top/file/100000/123.png"
    generate_qr_code(user_id, root_directory, file_url)