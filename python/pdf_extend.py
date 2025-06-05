import os
import pdfplumber
from spire.pdf import PdfDocument
from spire.pdf import FileFormat

def extract_pdf_text(pdf_path):
    """提取PDF文本并写入文件"""
    try:
        base_name = os.path.splitext(pdf_path)[0]
        output_path = f"{base_name}_extracted.txt"

        with pdfplumber.open(pdf_path) as pdf, \
             open(output_path, 'w', encoding='utf-8') as f:
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    f.write(f"=== 第 {page_num} 页内容 ===\n")
                    f.write(text + "\n\n")
                else:
                    f.write(f"=== 第 {page_num} 页无文本内容 ===\n\n")
            
            print(f"PDF文本已提取到：{output_path}")
            return output_path
    except Exception as e:
        print(f"提取PDF文本失败：{e}")
        return None

def pdf_to_word(pdf_file_path):
    try:
        pdf = PdfDocument()
        pdf.LoadFromFile(pdf_file_path)
        output_path = os.path.splitext(pdf_file_path)[0] + '.docx'
        pdf.SaveToFile(output_path, FileFormat.DOCX)
        return output_path
    except Exception as e:
        print(f"PDF转换失败：{e}")
        return None

if __name__ == "__main__":
    pdf_file_path = r"F:\大三下学期\移动应用开发\仓库\Muwu\处理图片检索.pdf"
    output_path = extract_pdf_text(pdf_file_path)
    if output_path:
        word_file_path = pdf_to_word(output_path)
        if word_file_path:
            print(f"PDF转换Word成功：{word_file_path}")