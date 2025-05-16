package com.hnu.muwu.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.hnu.muwu.bean.FinalFile;
import com.hnu.muwu.bean.MyFile;
import com.hnu.muwu.config.GlobalVariables;
import com.hnu.muwu.service.FileServiceImpl;
import com.hnu.muwu.service.PhotoTagService;
import com.hnu.muwu.utiles.FileHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
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

    @Autowired
    private PhotoTagService photoTagService;

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    /**
     * 文件上传解析接口
     * @param file 前端上传的文件
     * @return 上传处理结果
     */
    @PostMapping("/upload")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file, @RequestParam("userId") Integer userId) {
        //Integer userId = 100000;

        // 检查文件是否为空
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("上传文件不能为空");
        }

        // 获取文件基本信息
        String originalFilename = file.getOriginalFilename();
        String fileType = getFileExtension(originalFilename);
        long fileSize = file.getSize();

        // 定义文件存储路径
        String dirPath = GlobalVariables.rootPath + File.separator + "temp";
        String filePath = dirPath + File.separator + originalFilename;
        File destFile = new File(filePath);

        try {
            file.transferTo(destFile);
            MyFile myFile = new MyFile(userId, originalFilename, filePath, fileType, Timestamp.valueOf(LocalDateTime.now()), fileSize);

            ObjectMapper mapper = new ObjectMapper();
            mapper.registerModule(new JavaTimeModule());
            String json = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(myFile);

            System.out.println(json);

            redisTemplate.opsForValue().set(userId.toString(), json);

            String tag = fileService.getTag(filePath, userId);

            String text = fileService.getText(filePath);

            String sPath = fileService.getPath(userId, tag, myFile, text);

            // 构造成功响应
            Map<String, Object> response = new HashMap<>();
            response.put("message", "文件处理成功");
            response.put("filename", myFile.getFilename());
            response.put("filePath", sPath);
            response.put("tag", tag);
            return ResponseEntity.ok(response);

        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("文件处理失败: " + e.getMessage());
        }
    }

    @PostMapping("/check")
    public ResponseEntity<?> checkFile(@RequestParam("userId") int userId,  @RequestParam("tag") String tag, @RequestParam("path") String path) {

        MyFile myFile = fileService.getAndDeleteMyFile(userId);
        System.out.println(myFile);

        if (myFile == null) {
            return ResponseEntity.badRequest().body("数据解析失败");
        }

        String description = fileService.getText(myFile.getFilePath());

        FinalFile finalFile = new FinalFile(myFile, tag, description);

        finalFile.setFilePath(path);

        Path destinationPath = Paths.get(GlobalVariables.rootPath, finalFile.getFilePath());
        String destinationPathStr = destinationPath.toString();

        System.out.println(destinationPathStr);

        if (fileService.insertFile(finalFile) == 1 && FileHelper.moveFile(myFile.getFilePath(), destinationPathStr)) {
            String suggest = fileService.fileOperatorExtend(destinationPathStr, finalFile.getFileType());
            Map<String, Object> response = new HashMap<>();
            response.put("message", "文件处理成功");
            response.put("suggest", suggest);
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body("文件信息添加到数据库失败或提取建议失败");
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