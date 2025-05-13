package com.hnu.muwu.controller;

import com.hnu.muwu.bean.MyFile;
import com.hnu.muwu.config.GlobalVariables;
import com.hnu.muwu.service.FileServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/file")
public class FileController {

    @Autowired
    private FileServiceImpl fileService;

    /**
     * 文件上传解析接口
     * @param file 前端上传的文件
     * @return 上传处理结果
     */
    @PostMapping("/upload")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file) {
        int userId = 100000;

        // 检查文件是否为空
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("上传文件不能为空");
        }

        // 获取文件信息
        String originalFilename = file.getOriginalFilename();
        String fileType = getFileExtension(originalFilename);
        long fileSize = file.getSize();

        // 创建目录
        String dirPath = GlobalVariables.rootPath + File.separator + userId;
        File dir = new File(dirPath);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        // 构建文件路径
        String filePath = dirPath + File.separator + originalFilename;
        File destFile = new File(filePath);

        try {
            // 保存文件到目标路径
            file.transferTo(destFile);

            // 创建文件记录并保存到数据库
            MyFile myFile = new MyFile(userId, originalFilename, filePath, fileType, Timestamp.valueOf(LocalDateTime.now()), fileSize);

            System.out.println(myFile);

            // 保存到数据库
            int result = fileService.insertFile(myFile);

            if (result > 0) {
                Map<String, Object> response = new HashMap<>();
                response.put("message", "文件上传成功");
                response.put("filename", originalFilename);
                response.put("filePath", filePath);
                return ResponseEntity.ok(response);
            } else {
                // 如果数据库插入失败，删除已上传的文件
                destFile.delete();
                return ResponseEntity.internalServerError().body("文件信息保存到数据库失败");
            }
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("文件上传失败: " + e.getMessage());
        }
    }

    /**
     * 获取文件扩展名
     * @param filename 文件名
     * @return 文件扩展名
     */
    private String getFileExtension(String filename) {
        if (filename == null || filename.isEmpty()) {
            return "";
        }
        int dotIndex = filename.lastIndexOf(".");
        if (dotIndex < 0) {
            return "";
        }
        return filename.substring(dotIndex + 1);
    }
}