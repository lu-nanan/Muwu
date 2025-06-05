package com.hnu.muwu.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.hnu.muwu.bean.FinalFile;
import com.hnu.muwu.bean.MyFile;
import com.hnu.muwu.bean.ShareFileEntity;
import com.hnu.muwu.config.GlobalVariables;
import com.hnu.muwu.service.FileServiceImpl;
import com.hnu.muwu.service.PhotoTagService;
import com.hnu.muwu.service.ShareFileService;
import com.hnu.muwu.utiles.FileHelper;
import com.hnu.muwu.utiles.MessageQueueHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.TimeoutException;

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

    @Autowired
    private ShareFileService  shareFileService;
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

            String tag = fileService.getTag(filePath, userId, fileType);

            String text = fileService.getText(filePath, fileType);

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


    /**
     * 文件处理接口
     * @param userId 用户id
     * @param tag 文件标签
     * @param path 文件路径
     * @return 处理结果
     */
    @PostMapping("/check")
    public ResponseEntity<?> checkFile(@RequestParam("userId") int userId,  @RequestParam("tag") String tag, @RequestParam("path") String path) {

        MyFile myFile = fileService.getAndDeleteMyFile(userId);
        System.out.println(myFile);

        if (myFile == null) {
            return ResponseEntity.badRequest().body("数据解析失败");
        }

        String description = fileService.getText(myFile.getFilePath(), myFile.getFileType());

        FinalFile finalFile = new FinalFile(myFile, tag, description);

        finalFile.setFilePath(path);

        Path destinationPath = Paths.get(GlobalVariables.rootPath, finalFile.getFilePath());
        String destinationPathStr = destinationPath.toString();

        System.out.println(destinationPathStr);

        if (fileService.insertFile(finalFile) == 1 && FileHelper.moveFile(myFile.getFilePath(), destinationPathStr)) {
            String suggest = fileService.fileOperatorExtend(destinationPathStr, finalFile.getFileType());
            Map<String, Object> response = new HashMap<>();
            response.put("suggest", suggest);
            response.put("message", "文件处理成功");
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body("文件信息添加到数据库失败或提取建议失败");
        }
    }


    /**
     *
     * @param accept 是否接受建议
     *    true:接受建议并删除缓存
     *    false:拒绝建议并删除缓存
     * @param path 文件路径
     * @Param userId 用户id
     * @return 处理结果
     *
     * */
    @GetMapping("/suggest")
    public ResponseEntity<?> suggestCheck (@RequestParam("accept") Boolean accept, @RequestParam("filePath") String path, @RequestParam("userId") int userId) {
        if (accept) {
            Path destinationPath = Paths.get(GlobalVariables.rootPath, path);
            String destinationPathStr = destinationPath.toString();
            System.out.println(destinationPathStr);
            String suggest = redisTemplate.opsForValue().get(destinationPathStr);
            System.out.println(suggest);
            assert suggest != null;
            if (suggest.equals("OCR")) {
                Map<String, Object> re = fileService.photoOCR(destinationPathStr, userId);
                if (re != null) {
                    re.put("message", "OCR处理成功");
                    return ResponseEntity.ok(re);
                } else {
                    return ResponseEntity.badRequest().body("OCR处理失败");
                }
            } else if (suggest.equals("Generate_mindmap")) {
                String resulPath = fileService.generateMindmapFromMd(destinationPathStr, userId);
                if (resulPath != null) {
                    Map<String, Object> response = new HashMap<>();
                    response.put("message", "Mindmap处理成功");
                    response.put("filePath", resulPath);
                    return ResponseEntity.ok(response);
                }  else {
                    return ResponseEntity.badRequest().body("Mindmap处理失败");
                }
            } else if (suggest.equals("convert_word_to_pdf")){
                String resulPath = fileService.convertWordToPdf(destinationPathStr, userId);
                if (resulPath != null) {
                    Map<String, Object> response = new HashMap<>();
                    response.put("message", "文件处理成功");
                    response.put("filePath", resulPath);
                    return ResponseEntity.ok(response);
                } else {
                    return ResponseEntity.badRequest().body("文件处理失败");
                }
            }
        } else {
            redisTemplate.delete(path);
            return ResponseEntity.badRequest().body("缓存建议删除成功");
        }
        return null;
    }


    /**
     * 获取文件夹内容
     * @param path 文件夹路径
     * @param userId 用户id
     * @return 文件夹内容列表
     */
    @GetMapping("/list")
    public ResponseEntity<?> listFilesAndFolders(@RequestParam("path") String path, @RequestParam("userId") int userId) {

        String fullPath = GlobalVariables.rootPath + File.separator + path;
        File directory = new File(fullPath);

        System.out.println(fullPath);

        try {
            if (!directory.exists() || !directory.isDirectory()) {
                return ResponseEntity.badRequest().body("指定的路径不存在或不是一个目录");
            }

            File[] filesAndDirs = directory.listFiles();
            if (filesAndDirs == null) {
                return ResponseEntity.badRequest().body("无法读取目录内容");
            }

            List<Map<String, Object>> resultList = new ArrayList<>();

            for (File fileOrDir : filesAndDirs) {
                Map<String, Object> item = new HashMap<>();
                if (fileOrDir.isDirectory()) {
                    item.put("type", "directory");
                    item.put("name", fileOrDir.getName());
                } else {
                    item.put("type", "file");
                    item.put("name", fileOrDir.getName());
                    FinalFile myFile = fileService.getFileByName(fileOrDir.getName(), userId);
                    item.put("file_path", myFile.getFilename());
                    item.put("uploadTime", myFile.getUploadTime());
                    item.put("size", myFile.getSize());
                    item.put("tag", myFile.getTag());
                }
                resultList.add(item);
            }
            // 返回成功响应
            return ResponseEntity.ok(resultList);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * 文件搜索接口
     * @param userId 用户id
     * @param keyword 搜索关键词
     * @return 搜索结果列表
     */
    @GetMapping("/search")
    public ResponseEntity<?> searchFiles(@RequestParam("userId") int userId, @RequestParam("keyword") String keyword) {
        try {
            if (keyword == null || keyword.trim().isEmpty()) {
                return ResponseEntity.badRequest().body("搜索关键词不能为空");
            }

            String searchKeyword = "%" + keyword + "%";

            List<FinalFile> foundFiles = fileService.searchFilesByNameLike(searchKeyword, userId);

            if (foundFiles == null || foundFiles.isEmpty()) {
                foundFiles = fileService.searchFilesByQianwen(keyword, userId);
                if (foundFiles == null || foundFiles.isEmpty()) {
                    return ResponseEntity.badRequest().body("没有找到与关键词匹配的文件");
                }
            }

            List<Map<String, Object>> resultList = new ArrayList<>();
            for (FinalFile file : foundFiles) {
                Map<String, Object> item = new HashMap<>();
                item.put("type", "file");
                item.put("name", file.getFilename());
                item.put("filePath", file.getFilePath());
                item.put("uploadTime", file.getUploadTime());
                item.put("size", file.getSize());
                item.put("tag", file.getTag());
                resultList.add(item);
            }
            return ResponseEntity.ok(resultList);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("搜索文件失败: " + e.getMessage());
        }
    }

    @GetMapping("/share")
    public ResponseEntity<?> shareFiles(@RequestParam("path") String path, @RequestParam("userId") int userId) {
        String fullPath = GlobalVariables.rootPath + File.separator + path;
        File file = new File(fullPath);
        try {
            // 检查文件是否存在
            if (!file.exists()) {
                return ResponseEntity.badRequest().body("文件不存在");
            }
            // 检查是否是文件
            if (!file.isFile()) {
                return ResponseEntity.badRequest().body("指定路径不是一个文件");
            }
            // 检查文件所有权
            FinalFile myFile = fileService.getFileByName(file.getName(), userId);
            if (myFile == null) {
                return ResponseEntity.badRequest().body("用户无权操作该文件");
            }

            String token = UUID.randomUUID().toString();

            // 保存分享记录
            ShareFileEntity record = new ShareFileEntity();
            record.setToken(token);
            record.setUserId(userId);
            record.setSharePath(path);
            record.setFileName(file.getName());
            record.setExpiresAt(LocalDateTime.now().plusDays(7));
            if(shareFileService.saveShare(record)!=1){
                return ResponseEntity.internalServerError().body("服务器出差了");
            }
            try {
                HashMap<String, Object> message = new HashMap<>();
                message.put("server_directory", GlobalVariables.rootPath);
                message.put("file_path", GlobalVariables.rootPath+File.separator+path);
                message.put("operation", "create_file_qrcode");
                message.put("port", 8000);
                Map<String, Object> result = MessageQueueHelper.sendMessageAndGetResult(message);
                if (result != null) {
                    Map<String, Object> response = new HashMap<>();
                    response.put("status", (String) result.get("status"));

                    String qrcodePath = (String) result.get("qrcode_path");
                    byte[] qrcodeBytes = Files.readAllBytes(Paths.get(qrcodePath));
                    String base64QRCode = Base64.getEncoder().encodeToString(qrcodeBytes);
                    response.put("qrcode", base64QRCode);

                    response.put("url", (String) result.get("url"));
                    return ResponseEntity.ok(response);
                } else {
                    System.out.println("未收到处理结果或处理超时");
                    return ResponseEntity.internalServerError().body("生成分享链接失败");
                }
            } catch (IOException | TimeoutException | InterruptedException e) {
                throw new RuntimeException(e);
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
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