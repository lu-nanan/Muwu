import os
import glob
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. 定义数据集类
class RealSRDataset(Dataset):
    def __init__(self, root_dir, transform=None, target_size=(512, 512), scale_factor=2):
        """
        初始化数据集
        :param root_dir: 数据集文件夹路径（train或test）
        :param transform: 图像预处理变换
        :param target_size: HR图像的目标尺寸
        :param scale_factor: LR图像与HR图像的缩放因子
        """
        self.root_dir = root_dir
        self.transform = transform
        self.target_size = target_size
        self.scale_factor = scale_factor
        self.hr_images = sorted(glob.glob(os.path.join(root_dir, '*_HR.png')))
        self.lr_images = sorted(glob.glob(os.path.join(root_dir, '*_LR2.png')))
        assert len(self.hr_images) == len(self.lr_images), "HR和LR图片数量不匹配"

    def __len__(self):
        return len(self.hr_images)

    def __getitem__(self, idx):
        hr_image = Image.open(self.hr_images[idx]).convert('RGB')
        lr_image = Image.open(self.lr_images[idx]).convert('RGB')

        # 缩放HR图像到目标尺寸
        hr_image = hr_image.resize(self.target_size, Image.BICUBIC)

        # 计算LR图像的目标尺寸
        lr_target_size = (self.target_size[0] // self.scale_factor, self.target_size[1] // self.scale_factor)
        lr_image = lr_image.resize(lr_target_size, Image.BICUBIC)

        if self.transform:
            hr_image = self.transform(hr_image)
            lr_image = self.transform(lr_image)

        return lr_image, hr_image

# 2. 定义ESRGAN生成器（2倍超分）
class Generator(nn.Module):
    def __init__(self, in_channels=3, out_channels=3, num_features=64, num_rrdb=23):
        super(Generator, self).__init__()
        
        # 输入卷积层
        self.conv_first = nn.Conv2d(in_channels, num_features, 3, 1, 1)
        
        # RRDB主干网络（简化为示例层）
        self.body = nn.Sequential(
            nn.Conv2d(num_features, num_features, 3, 1, 1),
            nn.LeakyReLU(0.2, inplace=True)
        )
        
        # 上采样层（2倍超分）
        self.upsample = nn.Sequential(
            nn.Conv2d(num_features, num_features * 4, 3, 1, 1),
            nn.PixelShuffle(2),
            nn.LeakyReLU(0.2, inplace=True)
        )
        
        # 输出层
        self.conv_last = nn.Conv2d(num_features, out_channels, 3, 1, 1)

    def forward(self, x):
        out = self.conv_first(x)
        out = self.body(out)
        out = self.upsample(out)
        out = self.conv_last(out)
        return out

# 3. 定义ESRGAN判别器
class Discriminator(nn.Module):
    def __init__(self, in_channels=3):
        super(Discriminator, self).__init__()
        
        self.model = nn.Sequential(
            nn.Conv2d(in_channels, 64, 3, 1, 1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 64, 3, 2, 1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 3, 1, 1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 128, 3, 2, 1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(128, 1024, 1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(1024, 1, 1)
        )

    def forward(self, x):
        return self.model(x)

# 4. 定义损失函数
class Losses:
    def __init__(self):
        self.content_criterion = nn.L1Loss()
        self.adversarial_criterion = nn.BCEWithLogitsLoss()

    def content_loss(self, y_true, y_pred):
        return self.content_criterion(y_true, y_pred)

    def adversarial_loss(self, real_output, fake_output):
        real_loss = self.adversarial_criterion(real_output, torch.ones_like(real_output))
        fake_loss = self.adversarial_criterion(fake_output, torch.zeros_like(fake_output))
        return (real_loss + fake_loss) / 2

# 5. 训练函数
def train(generator, discriminator, train_loader, optimizer_g, optimizer_d, losses, num_epochs):
    generator.train()
    discriminator.train()
    
    for epoch in range(num_epochs):
        for i, (lr, hr) in enumerate(train_loader):
            lr, hr = lr.to(device), hr.to(device)
            
            # 训练判别器
            optimizer_d.zero_grad()
            fake_hr = generator(lr)
            real_output = discriminator(hr)
            fake_output = discriminator(fake_hr.detach())
            d_loss = losses.adversarial_loss(real_output, fake_output)
            d_loss.backward()
            optimizer_d.step()
            
            # 训练生成器
            optimizer_g.zero_grad()
            fake_output = discriminator(fake_hr)
            g_content_loss = losses.content_loss(hr, fake_hr)
            g_adv_loss = losses.adversarial_criterion(fake_output, torch.ones_like(fake_output))
            g_loss = g_content_loss + 0.01 * g_adv_loss
            g_loss.backward()
            optimizer_g.step()
            
            if i % 10 == 0:
                print(f"Epoch [{epoch}/{num_epochs}] Batch [{i}/{len(train_loader)}] "
                      f"D Loss: {d_loss.item():.4f} G Loss: {g_loss.item():.4f}")

        # 保存模型
        torch.save(generator.state_dict(), f"generator_epoch_{epoch}.pth")
        torch.save(discriminator.state_dict(), f"discriminator_epoch_{epoch}.pth")

# 6. 测试函数
def test(generator, test_loader):
    generator.eval()
    with torch.no_grad():
        for i, (lr, hr) in enumerate(test_loader):
            lr, hr = lr.to(device), hr.to(device)
            sr = generator(lr)
            print(f"Batch {i}: 测试完成，可保存SR图像或计算指标")

# 7. 主函数
if __name__ == "__main__":

    print(device)
    # 超参数
    batch_size = 16
    num_epochs = 10
    learning_rate = 0.0001
    target_size = (512, 512)  # 假设用户设置为512x512
    scale_factor = 2

    # 数据预处理
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # 加载数据集
    train_dataset = RealSRDataset('G:\\BaiduNetdiskDownload\\RealSR(V3)\\RealSR(V3)\\train', 
                                  transform=transform, target_size=target_size, scale_factor=scale_factor)
    test_dataset = RealSRDataset('G:\\BaiduNetdiskDownload\\RealSR(V3)\\RealSR(V3)\\test', 
                                 transform=transform, target_size=target_size, scale_factor=scale_factor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # 初始化模型
    generator = Generator().to(device)
    discriminator = Discriminator().to(device)
    optimizer_g = optim.Adam(generator.parameters(), lr=learning_rate)
    optimizer_d = optim.Adam(discriminator.parameters(), lr=learning_rate)
    losses = Losses()

    # 训练和测试
    train(generator, discriminator, train_loader, optimizer_g, optimizer_d, losses, num_epochs)
    test(generator, test_loader)