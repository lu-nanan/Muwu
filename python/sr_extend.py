import torch
import torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms
import os

class UpsampleBlock(nn.Module):
    def __init__(self, in_channels, up_scale):
        super(UpsampleBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, in_channels * (up_scale ** 2), 3, padding=1)
        self.pixel_shuffle = nn.PixelShuffle(up_scale)
        self.relu = nn.ReLU(inplace=True)
        
    def forward(self, x):
        return self.relu(self.pixel_shuffle(self.conv(x)))

# 残差块
class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)
        
    def forward(self, x):
        residual = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        return out

# 生成器 (Generator)
class Generator(nn.Module):
    def __init__(self, scale_factor=4, num_residual_blocks=16):
        super(Generator, self).__init__()
        
        # 第一层卷积
        self.conv1 = nn.Conv2d(3, 64, 9, padding=4)
        self.relu = nn.ReLU(inplace=True)
        
        # 残差块
        self.residual_blocks = nn.Sequential(
            *[ResidualBlock(64) for _ in range(num_residual_blocks)]
        )
        
        # 后残差卷积
        self.conv2 = nn.Conv2d(64, 64, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        
        # 上采样层
        if scale_factor == 4:
            self.upsample = nn.Sequential(
                UpsampleBlock(64, 2),
                UpsampleBlock(64, 2)
            )
        elif scale_factor == 2:
            self.upsample = UpsampleBlock(64, 2)
        
        # 最后一层
        self.conv3 = nn.Conv2d(64, 3, 9, padding=4)
        self.tanh = nn.Tanh()
        
    def forward(self, x):
        out1 = self.relu(self.conv1(x))
        
        out = self.residual_blocks(out1)
        out2 = self.bn2(self.conv2(out))
        out = torch.add(out1, out2)
        
        out = self.upsample(out)
        out = self.tanh(self.conv3(out))
        
        return out

def SR(input_path, model_path):
    try:     
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # 加载模型
        model = Generator().to(device)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        
        # 加载并预处理输入图像
        image = Image.open(input_path).convert('RGB')
        
        # 保存原始尺寸以便后续恢复
        original_width, original_height = image.size
        target_height, target_width = original_height * 4, original_width * 4
        
        # 预处理图像
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        # 使用模型生成超分辨率图像
        with torch.no_grad():
            output = model(input_tensor)
        
        # 反归一化
        output = output.squeeze().cpu()
        output = (output + 1) / 2
        output = output.clamp(0, 1)
        
        # 转换回PIL图像
        output_image = transforms.ToPILImage()(output)
        
        # 调整到目标尺寸
        output_image = output_image.resize((target_width, target_width), Image.BICUBIC)
        
        # 生成输出路径
        dir_name = os.path.dirname(input_path)
        base_name = os.path.basename(input_path)
        file_name, ext = os.path.splitext(base_name)
        output_path = os.path.join(dir_name, f"{file_name}_sr{ext}")
        
        # 保存输出图像
        output_image.save(output_path)
        print(f"超分辨率图像已保存至: {output_path}")
        return {
            "status" : "success",
            "result" : output_path
        }
    except Exception as e:
        return {
            "status" : "failure",
            "result" : e
        }
    

if __name__ == "__main__":
    input = r'F:\大三下学期\移动应用开发\仓库\Muwu\Canon_022_LR4.png'
    model = r'F:\大三下学期\移动应用开发\仓库\srgan_generator_final.pth'
    SR(input, model)