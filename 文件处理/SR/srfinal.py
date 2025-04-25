import os
import torch
import numpy as np
from PIL import Image
from torchvision.transforms import ToTensor, Compose
import argparse

class ESRGAN_Generator(torch.nn.Module):
    """与训练代码完全一致的生成器架构"""
    def __init__(self, in_channels=3, out_channels=3, num_features=64, num_rrdb=23):
        super(ESRGAN_Generator, self).__init__()
        self.conv_first = torch.nn.Conv2d(in_channels, num_features, 3, 1, 1)
        self.body = torch.nn.Sequential(
            torch.nn.Conv2d(num_features, num_features, 3, 1, 1),
            torch.nn.LeakyReLU(0.2, inplace=True))
        self.upsample = torch.nn.Sequential(
            torch.nn.Conv2d(num_features, num_features*4, 3, 1, 1),
            torch.nn.PixelShuffle(2),
            torch.nn.LeakyReLU(0.2, inplace=True))
        self.conv_last = torch.nn.Conv2d(num_features, out_channels, 3, 1, 1)

    def forward(self, x):
        x = self.conv_first(x)
        x = self.body(x)
        x = self.upsample(x)
        return self.conv_last(x)

def pad_image(img_tensor, multiple=8):
    """智能填充图像到指定倍数"""
    b, c, h, w = img_tensor.shape
    pad_h = (multiple - h % multiple) % multiple
    pad_w = (multiple - w % multiple) % multiple
    return torch.nn.functional.pad(img_tensor, (0, pad_w, 0, pad_h), mode='reflect')

def super_resolve(args):
    # 设备配置
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 初始化生成器
    generator = ESRGAN_Generator().to(device)
    
    # 加载训练好的权重
    if os.path.exists(args.model):
        state_dict = torch.load(args.model, map_location=device)
        generator.load_state_dict(state_dict)
        generator.eval()
        print(f"成功加载生成器模型: {args.model}")
    else:
        raise FileNotFoundError(f"模型文件不存在: {args.model}")

    # 图像预处理流水线
    transform = Compose([
        ToTensor(),
        torch.nn.InstanceNorm2d(3)  # 与训练时一致
    ])

    # 处理输入图像
    img = Image.open(args.input).convert('RGB')
    original_size = img.size
    
    # 转换并填充张量
    lr_tensor = transform(img).unsqueeze(0).to(device)
    lr_tensor = pad_image(lr_tensor)
    
    # 执行超分辨率
    with torch.no_grad():
        sr_tensor = generator(lr_tensor).clamp(-1, 1)
    
    # 后处理
    sr_tensor = (sr_tensor + 1) / 2  # 从[-1,1]转换到[0,1]
    sr_array = sr_tensor.squeeze(0).cpu().numpy().transpose(1, 2, 0)
    sr_array = np.clip(sr_array * 255, 0, 255).astype(np.uint8)
    
    # 裁剪回原始比例
    sr_img = Image.fromarray(sr_array).resize(
        (original_size[0]*2, original_size[1]*2),  # 假设scale_factor=2
        resample=Image.BICUBIC
    )
    
    # 保存结果
    sr_img.save(args.output)
    print(f"超分辨率完成！结果保存至: {args.output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ESRGAN超分辨率推理')
    parser.add_argument('--input', type=str, required=True, help='输入图像路径')
    parser.add_argument('--output', type=str, default='sr_result.png', help='输出路径')
    parser.add_argument('--model', type=str, default='generator_epoch_11.pth',
                       help='生成器模型路径')
    args = parser.parse_args()
    
    super_resolve(args)