package com.hnu.muwu.controller;

import com.hnu.muwu.bean.MyFile;
import com.hnu.muwu.config.GlobalVariables;
import com.hnu.muwu.utiles.FileHelper;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.*;
import java.net.URLEncoder;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/source")
public class FileDownloadController {

    // 文件扩展名到MIME类型的映射
    private static final Map<String, String> MIME_TYPE_MAP = new HashMap<>();
    static {
        MIME_TYPE_MAP.put("jpg", "image/jpeg");
        MIME_TYPE_MAP.put("jpeg", "image/jpeg");
        MIME_TYPE_MAP.put("png", "image/png");
        MIME_TYPE_MAP.put("gif", "image/gif");
        MIME_TYPE_MAP.put("pdf", "application/pdf");
        MIME_TYPE_MAP.put("txt", "text/plain");
        MIME_TYPE_MAP.put("csv", "text/csv");
        MIME_TYPE_MAP.put("doc", "application/msword");
        MIME_TYPE_MAP.put("docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document");
        MIME_TYPE_MAP.put("xls", "application/vnd.ms-excel");
        MIME_TYPE_MAP.put("xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        MIME_TYPE_MAP.put("ppt", "application/vnd.ms-powerpoint");
        MIME_TYPE_MAP.put("pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation");
        MIME_TYPE_MAP.put("zip", "application/zip");
        MIME_TYPE_MAP.put("rar", "application/x-rar-compressed");
        MIME_TYPE_MAP.put("mp3", "audio/mpeg");
        MIME_TYPE_MAP.put("mp4", "video/mp4");
        MIME_TYPE_MAP.put("html", "text/html");
        MIME_TYPE_MAP.put("js", "application/javascript");
        MIME_TYPE_MAP.put("css", "text/css");
        MIME_TYPE_MAP.put("json", "application/json");
    }

    @GetMapping("/preview")
    public ResponseEntity<?> downloadFile(
            @RequestParam("filePath") String filePath,
            @RequestParam("userId") Integer userId) throws IOException {
        System.out.println(filePath+userId);
        String oldPath = GlobalVariables.rootPath + File.separator + filePath;
        MyFile myFile = FileHelper.createMyFileFromPath(oldPath, userId);
        String newPath = GlobalVariables.downloadBasePath + File.separator + userId.toString();
        if(!Files.exists(Paths.get(newPath))){
            Files.createDirectories(Paths.get(newPath));
        }
        copyFile(oldPath,newPath);
        Path safePath = validateAndNormalizePath(newPath+File.separator+myFile.getFilename());
        if (!checkUserPermission(userId, safePath)) {
            return ResponseEntity.badRequest().body("文件路径非法");
        }

        System.out.println(safePath);
        String resource = GlobalVariables.downloadBaseUrl + "file/"  + userId + "/" + myFile.getFilename();
        System.out.println(resource);
        String fileName = safePath.getFileName().toString();
        String fileExtension = getFileExtension(fileName);

        if (fileExtension == null || fileExtension.isEmpty()) {
            return ResponseEntity.badRequest().body("文件扩展名无效");
        }

        // 6. 根据扩展名获取Content-Type
        String contentType = MIME_TYPE_MAP.getOrDefault(fileExtension.toLowerCase(),
                "application/octet-stream");

        HashMap<String, Object> response = new HashMap<>();
        response.put("url", resource);
        return ResponseEntity.ok(response);
    }

    /**
     * 文件下载接口
     * @param filePath 前端传入的文件路径
     * @param userId 前端传入的用户ID
     * @param response HTTP响应对象
     * @return 文件下载结果
     */
    @GetMapping("/download")
    public ResponseEntity<?> downloadFile(@RequestParam("filePath") String filePath,
                                          @RequestParam("userId") Integer userId,
                                          HttpServletResponse response) {
        // 拼接完整的文件路径
        String fullFilePath = GlobalVariables.rootPath + File.separator + filePath;
        File file = new File(fullFilePath);

        // 检查文件是否存在
        if (!file.exists()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("文件不存在");
        }

        // 设置响应头，指示文件作为附件下载
        response.setContentType("application/octet-stream");
        try {
            response.setHeader("Content-Disposition", "attachment;filename=" +
                    URLEncoder.encode(file.getName(), "UTF-8"));
        } catch (UnsupportedEncodingException e) {
            return ResponseEntity.internalServerError().body("文件名编码失败");
        }
        response.setHeader("Content-Length", String.valueOf(file.length()));

        // 读取文件并将其写入响应流
        try (FileInputStream fis = new FileInputStream(file);
             BufferedInputStream bis = new BufferedInputStream(fis);
             OutputStream os = response.getOutputStream()) {

            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = bis.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
            os.flush();
            return ResponseEntity.ok().build();

        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("文件下载失败: " + e.getMessage());
        }
    }

    private Path validateAndNormalizePath(String rawPath) {
        Path path = Paths.get(rawPath).normalize();

        // 定义安全基础目录
        Path baseDir = Paths.get("F:\\大三下学期\\移动应用开发\\仓库\\Muwu\\muwu\\src\\main\\resources\\static\\file")
                .toAbsolutePath().normalize();

        if (!path.startsWith(baseDir)) {
            throw new SecurityException("Attempted directory traversal attack");
        }
        return path;
    }

    private boolean checkUserPermission(Integer userId, Path filePath) {
        return true;
    }

    // 从文件名中获取扩展名
    private String getFileExtension(String fileName) {
        int dotIndex = fileName.lastIndexOf('.');
        if (dotIndex > 0 && dotIndex < fileName.length() - 1) {
            return fileName.substring(dotIndex + 1);
        }
        return null;
    }
    public static String copyFile(String sourceFilePath, String targetFolderPath) {
        try {
            // 检查源文件是否存在
            Path sourcePath = Paths.get(sourceFilePath);
            if (!Files.exists(sourcePath)) {
                System.err.println("错误：源文件不存在 - " + sourceFilePath);
                return null;
            }

            // 确保目标文件夹存在
            Path targetFolder = Paths.get(targetFolderPath);
            Files.createDirectories(targetFolder);

            // 构建目标文件路径（保持原文件名）
            String fileName = sourcePath.getFileName().toString();
            Path targetPath = targetFolder.resolve(fileName);

            // 执行文件拷贝（使用标准的NIO API）
            Files.copy(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);

            System.out.println("文件已成功拷贝至: " + targetPath);
            return targetPath.toString();

        } catch (IOException e) {
            System.err.println("文件拷贝失败: " + e.getMessage());
            return null;
        }
    }
}