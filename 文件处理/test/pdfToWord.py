from spire.pdf import PdfDocument
from spire.pdf import FileFormat

# 创建PdfDocument类的实例
pdf = PdfDocument()

# 载入PDF文件
pdf.LoadFromFile(r'F:\大三下学期\移动应用开发\仓库\Muwu\文件处理\信息科学与工程学院实验报告模版.pdf')

# 将PDF文件直接转换为Doc文件并保存
pdf.SaveToFile("output/PDF转DOC", FileFormat.DOC)

# 将PDF文件直接转换为Docx文件并保存
pdf.SaveToFile("output/PDF转DOCX", FileFormat.DOCX)

# 关闭实例
pdf.Close()