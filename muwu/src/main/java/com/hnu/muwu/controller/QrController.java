package com.hnu.muwu.controller;

import com.hnu.muwu.config.GlobalVariables;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/qr")
public class QrController {
    @GetMapping("/get")
    public ResponseEntity<?> getQr(@RequestParam("userId") int userId, @RequestParam("qrPath") String path) {
       System.out.println(path);
        Map<String, Object> response = new HashMap<>();
        try {
            // 获取文件
            File file = new File(path);
            if (!file.exists()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("File not found");
            }

            byte[] qrcodeBytes = Files.readAllBytes(Paths.get(path));
            String base64QRCode = Base64.getEncoder().encodeToString(qrcodeBytes);
            response.put("qrcode", base64QRCode);
//            // 读取文件数据
//            byte[] fileContent = Files.readAllBytes(file.toPath());
//
//            // 设置响应头
//            HttpHeaders headers = new HttpHeaders();
//            // 设置内容类型为图片
//            headers.setContentType(MediaType.IMAGE_PNG); // 如果是其他格式的图片可以相应调整
//            // 设置文件名
//            headers.setContentDispositionFormData("attachment", file.getName());
//            // 设置文件大小
//            headers.setContentLength(fileContent.length);
//
//            // 返回文件数据
//            return new ResponseEntity<>(fileContent, headers, HttpStatus.OK);
            return ResponseEntity.ok(response);
        } catch (IOException e) {
            System.out.println(e.getMessage());
            return ResponseEntity.badRequest().body("读取文件失败");
        }
    }
}
