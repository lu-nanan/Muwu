package com.hnu.muwu.utiles;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

public class FileHelper {

    /**
     * 将文件从源路径移动到目标路径
     *
     * @param sourcePath 源文件的完整路径
     * @param targetPath 目标文件的完整路径
     * @return 移动成功返回true，失败返回false
     */
    public static boolean moveFile(String sourcePath, String targetPath) {
        try {
            // 创建Path对象
            Path source = Paths.get(sourcePath);
            Path target = Paths.get(targetPath);

            // 确保目标目录存在
            File targetDir = target.getParent().toFile();
            if (!targetDir.exists()) {
                if (!targetDir.mkdirs()) {
                    System.err.println("无法创建目标目录: " + targetDir.getAbsolutePath());
                    return false;
                }
            }

            // 检查源文件是否存在
            if (!Files.exists(source)) {
                System.err.println("源文件不存在: " + sourcePath);
                return false;
            }

            // 使用Files.move()方法移动文件，如果目标文件已存在则替换
            Files.move(source, target, StandardCopyOption.REPLACE_EXISTING);

            // 验证移动是否成功
            if (Files.exists(target) && !Files.exists(source)) {
                System.out.println("文件移动成功: " + sourcePath + " -> " + targetPath);
                return true;
            } else {
                System.err.println("文件移动后的状态异常，可能未完全移动");
                return false;
            }

        } catch (IOException e) {
            System.err.println("移动文件时发生错误: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
}