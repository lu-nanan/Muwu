import pdfplumber

def get_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() 
            print(text)

if __name__ == '__main__':
    pdf_path = r'F:\大三下学期\编译原理\chaper 2 - 词法分析2025.pdf'
    get_pdf_text(pdf_path)