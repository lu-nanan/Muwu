import paddlehub as hub
import cv2

img_path = r'F:\android\image.png'

# 初始化OCR模型
ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)

# 执行OCR识别
result = ocr.recognize_text(images=[cv2.imread(img_path)])

# 提取所有text字段
extracted_texts = [item['text'] for item in result[0]['data']]

# 打印提取结果
print("提取的文本内容：")
for text in extracted_texts:
    print(text)