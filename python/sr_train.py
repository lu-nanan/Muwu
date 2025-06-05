import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from torchvision.models import vgg19

# 设备配置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# 数据集类
class RealSRDataset(Dataset):
    def __init__(self, data_dir, lr_size=32, hr_size=128, transform=None):
        self.data_dir = data_dir
        self.lr_size = lr_size
        self.hr_size = hr_size
        self.transform = transform
        
        # 获取所有HR和LR图片对
        self.hr_files = sorted(glob.glob(os.path.join(data_dir, '*_HR.png')))
        self.lr_files = sorted(glob.glob(os.path.join(data_dir, '*_LR4.png')))
        
        # 确保HR和LR文件数量匹配
        assert len(self.hr_files) == len(self.lr_files), "HR和LR文件数量不匹配"
        
    def __len__(self):
        return len(self.hr_files)
    
    def __getitem__(self, idx):
        hr_path = self.hr_files[idx]
        lr_path = self.lr_files[idx]
        
        # 加载图片
        hr_image = Image.open(hr_path).convert('RGB')
        lr_image = Image.open(lr_path).convert('RGB')
        
        # 调整图像大小以确保正确的比例关系
        lr_transform = transforms.Compose([
            transforms.Resize((self.lr_size, self.lr_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        
        hr_transform = transforms.Compose([
            transforms.Resize((self.hr_size, self.hr_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        
        lr_image = lr_transform(lr_image)
        hr_image = hr_transform(hr_image)
            
        return lr_image, hr_image

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

# 上采样块
class UpsampleBlock(nn.Module):
    def __init__(self, in_channels, up_scale):
        super(UpsampleBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, in_channels * (up_scale ** 2), 3, padding=1)
        self.pixel_shuffle = nn.PixelShuffle(up_scale)
        self.relu = nn.ReLU(inplace=True)
        
    def forward(self, x):
        return self.relu(self.pixel_shuffle(self.conv(x)))

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

# 判别器 (Discriminator)
class Discriminator(nn.Module):
    def __init__(self, input_size=128):
        super(Discriminator, self).__init__()
        
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(64, 64, 3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(128, 128, 3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(256, 256, 3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(256, 512, 3, padding=1),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(512, 512, 3, stride=2, padding=1),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.AdaptiveAvgPool2d(1),
        )
        
        self.classifier = nn.Sequential(
            nn.Linear(512, 1024),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(1024, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# VGG感知损失
class VGGLoss(nn.Module):
    def __init__(self):
        super(VGGLoss, self).__init__()
        vgg = vgg19(pretrained=True)
        self.features = nn.Sequential(*list(vgg.features)[:36]).eval()
        for param in self.features.parameters():
            param.requires_grad = False
        self.mse_loss = nn.MSELoss()
        
    def forward(self, output, target):
        output_features = self.features(output)
        target_features = self.features(target)
        return self.mse_loss(output_features, target_features)

# 训练函数
def train_srgan():
    # 超参数
    batch_size = 8
    num_epochs = 100
    lr_g = 1e-4
    lr_d = 1e-4
    
    # 图像尺寸设置 (确保4倍上采样关系)
    lr_size = 32  # 低分辨率图像尺寸
    hr_size = 128  # 高分辨率图像尺寸 (4倍于lr_size)
    
    # 数据加载
    train_dataset = RealSRDataset(
        data_dir=r'/root/cs/sr/dataset/train',
        lr_size=lr_size,
        hr_size=hr_size
    )
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    
    test_dataset = RealSRDataset(
        data_dir=r'/root/cs/sr/dataset/test',
        lr_size=lr_size,
        hr_size=hr_size
    )
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    
    # 模型初始化
    generator = Generator().to(device)
    discriminator = Discriminator(input_size=hr_size).to(device)
    
    # 损失函数
    criterion_gan = nn.BCELoss()
    criterion_mse = nn.MSELoss()
    vgg_loss = VGGLoss().to(device)
    
    # 优化器
    optimizer_g = optim.Adam(generator.parameters(), lr=lr_g, betas=(0.9, 0.999))
    optimizer_d = optim.Adam(discriminator.parameters(), lr=lr_d, betas=(0.9, 0.999))
    
    print(f"训练数据集大小: {len(train_dataset)}")
    print(f"测试数据集大小: {len(test_dataset)}")
    print(f"输入图像尺寸: {lr_size}x{lr_size}")
    print(f"输出图像尺寸: {hr_size}x{hr_size}")
    
    # 训练循环
    for epoch in range(num_epochs):
        generator.train()
        discriminator.train()
        
        g_losses = []
        d_losses = []
        
        for i, (lr_imgs, hr_imgs) in enumerate(train_loader):
            lr_imgs = lr_imgs.to(device)
            hr_imgs = hr_imgs.to(device)
            
            batch_size_current = lr_imgs.size(0)
            
            # 真实和虚假标签
            real_labels = torch.ones(batch_size_current, 1).to(device)
            fake_labels = torch.zeros(batch_size_current, 1).to(device)
            
            # 生成超分辨率图像
            fake_imgs = generator(lr_imgs)
            
            # 验证尺寸匹配
            print(f"LR shape: {lr_imgs.shape}, HR shape: {hr_imgs.shape}, Fake shape: {fake_imgs.shape}")
            
            # ================== 训练判别器 ==================
            optimizer_d.zero_grad()
            
            # 真实图像损失
            real_output = discriminator(hr_imgs)
            d_loss_real = criterion_gan(real_output, real_labels)
            
            # 生成图像损失
            fake_output = discriminator(fake_imgs.detach())
            d_loss_fake = criterion_gan(fake_output, fake_labels)
            
            d_loss = d_loss_real + d_loss_fake
            d_loss.backward()
            optimizer_d.step()
            
            # ================== 训练生成器 ==================
            optimizer_g.zero_grad()
            
            # 对抗损失
            fake_output = discriminator(fake_imgs)
            g_loss_gan = criterion_gan(fake_output, real_labels)
            
            # 内容损失 (MSE + VGG)
            g_loss_mse = criterion_mse(fake_imgs, hr_imgs)
            g_loss_vgg = vgg_loss(fake_imgs, hr_imgs)
            
            # 总生成器损失
            g_loss = g_loss_gan + 100 * g_loss_mse + 0.006 * g_loss_vgg
            g_loss.backward()
            optimizer_g.step()
            
            g_losses.append(g_loss.item())
            d_losses.append(d_loss.item())
            
            if i % 50 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_loader)}], '
                      f'G_Loss: {g_loss.item():.4f}, D_Loss: {d_loss.item():.4f}')
        
        # 每个epoch结束后的统计
        avg_g_loss = np.mean(g_losses)
        avg_d_loss = np.mean(d_losses)
        print(f'Epoch [{epoch+1}/{num_epochs}] 完成 - Avg G_Loss: {avg_g_loss:.4f}, Avg D_Loss: {avg_d_loss:.4f}')
        
        # 保存模型
        if (epoch + 1) % 10 == 0:
            torch.save({
                'generator_state_dict': generator.state_dict(),
                'discriminator_state_dict': discriminator.state_dict(),
                'optimizer_g_state_dict': optimizer_g.state_dict(),
                'optimizer_d_state_dict': optimizer_d.state_dict(),
                'epoch': epoch + 1,
            }, f'srgan_checkpoint_epoch_{epoch+1}.pth')
            print(f'模型已保存: srgan_checkpoint_epoch_{epoch+1}.pth')
    
    # 保存最终模型
    torch.save(generator.state_dict(), 'srgan_generator_final.pth')
    torch.save(discriminator.state_dict(), 'srgan_discriminator_final.pth')
    print('训练完成！最终模型已保存。')

# 测试函数
def test_srgan(model_path):
    # 图像尺寸设置
    lr_size = 32
    hr_size = 128
    
    # 加载模型
    generator = Generator().to(device)
    generator.load_state_dict(torch.load(model_path, map_location=device))
    generator.eval()
    
    test_dataset = RealSRDataset(
        data_dir=r'/root/cs/sr/dataset/test',
        lr_size=lr_size,
        hr_size=hr_size
    )
    test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)
    
    with torch.no_grad():
        for i, (lr_img, hr_img) in enumerate(test_loader):
            if i >= 5:  # 只测试前5张图片
                break
                
            lr_img = lr_img.to(device)
            sr_img = generator(lr_img)
            
            # 反归一化
            lr_img = (lr_img + 1) / 2
            sr_img = (sr_img + 1) / 2
            hr_img = (hr_img + 1) / 2
            
            # 显示结果
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            axes[0].imshow(lr_img.cpu().squeeze().permute(1, 2, 0))
            axes[0].set_title(f'Low Resolution ({lr_size}x{lr_size})')
            axes[0].axis('off')
            
            axes[1].imshow(sr_img.cpu().squeeze().permute(1, 2, 0))
            axes[1].set_title(f'Super Resolution ({hr_size}x{hr_size})')
            axes[1].axis('off')
            
            axes[2].imshow(hr_img.squeeze().permute(1, 2, 0))
            axes[2].set_title(f'High Resolution ({hr_size}x{hr_size})')
            axes[2].axis('off')
            
            plt.tight_layout()
            plt.savefig(f'test_result_{i+1}.png')
            plt.show()

if __name__ == "__main__":
    # 开始训练
    print("开始SRGAN训练...")
    train_srgan()
    
    # 测试模型 (训练完成后取消注释)
    # print("开始测试模型...")
    # test_srgan('srgan_generator_final.pth')