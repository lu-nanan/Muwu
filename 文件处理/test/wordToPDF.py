# # from docx2pdf import convert

# # convert("F:\大三下学期\编译原理\实验\信息科学与工程学院实验报告模版.docx", "output.pdf")


# import os
# import comtypes.client
# # 设置word和pdf文件类型常量
# wdFormatPDF = 17
# wdFormatDoc = 0
# wdFormatDocx = 12
# # 获取当前目录
# folder_path = os.getcwd()
# # 遍历目录中的所有文件
# for file_name in os.listdir(folder_path):
#     # 判断文件类型是否为doc/docx
#     if file_name.endswith('.doc') or file_name.endswith('.docx'):
#         # 创建word应用程序对象
#         word_app = comtypes.client.CreateObject('Word.Application')
#         word_app.Visible = False
#         # 打开文件
#         doc_file = os.path.join(folder_path, file_name)
#         doc = word_app.Documents.Open(doc_file)
#         # 将文件另存为pdf格式
#         pdf_file = os.path.splitext(doc_file)[0] + '.pdf'
#         doc.SaveAs(pdf_file, FileFormat=wdFormatPDF)
#         # 关闭文件和应用程序
#         doc.Close()
#         word_app.Quit()
#         print(file_name)
# print("All finish!")

import os
import comtypes.client

def convert_word_to_pdf(word_file_path):
    # 定义Word保存为PDF的格式常量
    wdFormatPDF = 17

    # 检查文件是否存在
    if not os.path.exists(word_file_path):
        print(f"文件不存在: {word_file_path}")
        return

    # 检查文件扩展名是否为.doc或.docx
    if not word_file_path.endswith(('.doc', '.docx')):
        print("仅支持.doc或.docx格式文件")
        return

    # 创建输出PDF文件路径（替换扩展名为.pdf）
    pdf_file_path = os.path.splitext(word_file_path)[0] + '.pdf'

    try:
        # 创建Word应用程序对象
        word_app = comtypes.client.CreateObject('Word.Application')
        word_app.Visible = False  # 隐藏Word界面

        # 打开Word文档
        doc = word_app.Documents.Open(word_file_path)
        
        # 保存为PDF格式
        doc.SaveAs(pdf_file_path, FileFormat=wdFormatPDF)
        
        # 关闭文档和应用程序
        doc.Close()
        word_app.Quit()

        print(f"转换成功: {word_file_path} -> {pdf_file_path}")
        return pdf_file_path  # 返回生成的PDF路径

    except Exception as e:
        print(f"转换失败: {e}")
        # 确保异常时关闭Word进程（即使出错也要尝试退出）
        try:
            word_app.Quit()
        except:
            pass
        return None

# 使用示例：
convert_word_to_pdf(r"F:\大三下学期\编译原理\实验\信息科学与工程学院实验报告模版.docx")