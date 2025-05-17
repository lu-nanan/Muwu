package com.hnu.muwu.controller;

import com.hnu.muwu.service.UserService;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.apache.tomcat.jni.FileInfo;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/auth")
public class FilesController {

//    @Resource
//    private UserService userService;
//
//    /**
//     * 文件上传接口
//     *
//     * @param request        HTTP请求对象
//     * @param file           上传的文件
//     * @param userId         用户ID
//     * @param encrypt        是否加密（默认false）
//     * @param encryptionKey  加密密钥（可选）
//     * @return ResponseEntity 返回上传结果
//     */
//    @PostMapping(value = "/upload", consumes = "multipart/form-data")
//    public ResponseEntity<?> uploadFile(
//            HttpServletRequest request,
//            @RequestPart("file") MultipartFile file,
//            @RequestParam String userId,
//            @RequestParam(defaultValue = "false") boolean encrypt,
//            @RequestParam(required = false) String encryptionKey) {
//
//        try {
//            // 验证用户ID是否存在
//            if (!userService.checkUserAccount(userId)) {
//                return ResponseEntity.badRequest().body("用户不存在");
//            }
//
//            // 验证文件是否为空
//            if (file.isEmpty()) {
//                return ResponseEntity.badRequest().body("文件不能为空");
//            }
//
//            // 调用服务层处理文件上传
//            //String result = userService.handleFileUpload(file, userId, encrypt, encryptionKey);
//
//            // 获取session并设置属性
//            HttpSession session = request.getSession();
//            session.setAttribute("lastUploadTime", System.currentTimeMillis());
//
//            return ResponseEntity.ok(result);
//        } catch (IOException e) {
//            return ResponseEntity.internalServerError().body("文件上传失败：" + e.getMessage());
//        } catch (Exception e) {
//            return ResponseEntity.badRequest().body("请求参数错误：" + e.getMessage());
//        }
//    }
//
//    /**
//     * 获取用户文件列表
//     *
//     * @param request HTTP请求对象
//     * @param userId  用户ID
//     * @return ResponseEntity 返回文件列表
//     */
//    @GetMapping("/files/{userId}")
//    public ResponseEntity<?> getUserFiles(
//            HttpServletRequest request,
//            @PathVariable String userId) {
//
//        // 验证用户ID是否存在
//        if (!userService.checkUserAccount(userId)) {
//            return ResponseEntity.badRequest().body("用户不存在");
//        }
//
//        // 检查session中的用户是否匹配
//        HttpSession session = request.getSession();
//        Integer sessionUserId = (Integer) session.getAttribute("user");
//        if (sessionUserId == null || !sessionUserId.equals(userId)) {
//            return ResponseEntity.status(401).body("未授权访问");
//        }
//
//        try {
//            List<FileInfo> fileList = userService.getUserFiles(userId);
//            return ResponseEntity.ok(fileList);
//        } catch (Exception e) {
//            return ResponseEntity.internalServerError().body("获取文件列表失败：" + e.getMessage());
//        }
//    }
}
