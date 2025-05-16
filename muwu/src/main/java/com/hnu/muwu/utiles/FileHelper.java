package com.hnu.muwu.utiles;

import com.hnu.muwu.bean.MyFile;
import com.hnu.muwu.config.GlobalVariables;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.sql.Timestamp;

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

    /**
     * 根据绝对路径和用户ID生成MyFile对象
     * @param absolutePath 文件的绝对路径
     * @param userId 用户ID
     * @return 包含文件信息的MyFile对象
     */
    public static MyFile createMyFileFromPath(String absolutePath, int userId) {
        // 创建文件对象获取文件信息
        File file = new File(absolutePath);

        // 检查文件是否存在
        if (!file.exists() || !file.isFile()) {
            return null;
        }

        // 获取文件名
        String filename = file.getName();

        // 获取文件类型（文件扩展名）
        String fileType = "";
        int lastDotIndex = filename.lastIndexOf('.');
        if (lastDotIndex > 0) {
            fileType = filename.substring(lastDotIndex + 1).toLowerCase();
        }

        // 获取文件大小
        long fileSize = file.length();

        // 设置当前时间为上传时间
        Timestamp uploadTime = new Timestamp(System.currentTimeMillis());

        // 处理文件路径：从绝对路径中移除GlobalVariables.rootPath前缀
        String rootPath = GlobalVariables.rootPath;
        String relativePath = absolutePath;

        if (absolutePath.startsWith(rootPath)) {
            // 计算相对路径，确保分隔符一致性
            relativePath = absolutePath.substring(rootPath.length());

            // 如果relativePath开头有文件分隔符，则移除它
            if (relativePath.startsWith(File.separator)) {
                relativePath = relativePath.substring(File.separator.length());
            }
        }

        // 创建并返回MyFile对象
        return new MyFile(userId, filename, relativePath, fileType, uploadTime, fileSize);
    }

    public static String readFileContent(String absolutePath) {
        StringBuilder content = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(absolutePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append(System.lineSeparator());
            }
        } catch (IOException e) {
            System.err.println("无法读取文件: " + absolutePath);
            e.printStackTrace();
            return null; // 或者抛出异常
        }
        return content.toString();
    }
}