import paddlehub as hub
import shutil
import cv2
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import clip
import cv2
import os
import pytesseract
import torch
def OCR(image_path):
    """执行OCR识别并写入文件"""
    
    dist_path = r'F:\image.png'

    try:
        shutil.copy(image_path, dist_path) 

        ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)
        result = ocr.recognize_text(images=[cv2.imread(dist_path)])

        # 生成输出路径
        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}_ocr.txt"

        extracted_texts = [item['text'] for item in result[0]['data']]
        text_content = '\n'.join(extracted_texts)  # 用换行符连接成字符串
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"OCR结果已保存到：{output_path}")

        results = {
            "text": text_content,
            "output_path": output_path
        }

        print(results)

        return results
    
    except Exception as e:
        print(f"OCR处理失败：{e}")
        return None
    
def generate_caption(image_path, blip_path, condition_text="a photography of"):

    processor = BlipProcessor.from_pretrained(blip_path)
    model = BlipForConditionalGeneration.from_pretrained(blip_path)

    try:
        # 验证文件存在性
        if not os.path.exists(image_path):
            return f"错误：文件不存在 - {image_path}"
            
        # 加载并转换图像
        raw_image = Image.open(image_path).convert('RGB')
        
        # 图像描述生成
        inputs = processor(raw_image, condition_text, return_tensors="pt")
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
        
    except (IOError, OSError) as e:
        return f"图像处理失败: {str(e)}"
    except Exception as e:
        return f"未知错误: {str(e)}"
    
def is_rich_text(image_path):
    """判断图片是否为富文本"""
    try:
        with Image.open(image_path) as img:
            # 图像预处理（灰度 + 二值化）
            img = img.convert('L').point(lambda x: 0 if x < 180 else 255)
            
            # 执行OCR识别
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')

            text_length = len(text.replace(' ', '').replace('\n', ''))

            if text_length > 100:
                return True
            else:
                return False
            
    except Exception as e:
        print(f"判断图片是否为富文本失败：{e}")
        return False

# 将图像与文本描述进行匹配，返回最匹配的描述及其概率
def match_image_to_text(text_descriptions, image_path, vit_b_path):
    
    # 加载设备配置
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 加载模型和预处理函数
    model, preprocess = clip.load("ViT-B/32", device=device, jit=False)

    # 尝试加载自定义权重（可选）
    try:
        model.load_state_dict(torch.load(vit_b_path, map_location=device))
        print("成功加载自定义权重文件 'vit-b-32.pth'")
    except Exception as e:
        print(f"加载 'vit-b-32.pth' 失败: {e}，将使用默认预训练权重")

    print(image_path)

    # 加载和预处理图像
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    # 生成文本token并移动到设备
    text_inputs = torch.cat([clip.tokenize(desc) for desc in text_descriptions]).to(device)
    
    # 计算特征相似度
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
        top_prob, top_idx = similarity[0].topk(1)
    
    return text_descriptions[top_idx.item()], top_prob.item()