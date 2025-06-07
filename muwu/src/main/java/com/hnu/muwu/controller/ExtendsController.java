package com.hnu.muwu.controller;

import com.hnu.muwu.config.GlobalVariables;
import com.hnu.muwu.service.FileServiceImpl;
import com.hnu.muwu.service.PhotoTagService;
import com.hnu.muwu.service.ShareFileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;


@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/extends")
public class ExtendsController {

    @Autowired
    private FileServiceImpl fileService;

    @Autowired
    private PhotoTagService photoTagService;

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @Autowired
    private ShareFileService shareFileService;


    @PostMapping("/ocr")
    public ResponseEntity<?> ocr(@RequestParam("filePath") String filePath, @RequestParam("userId") int userId) {
        String fullPath = GlobalVariables.rootPath + filePath;
        Map<String, Object> result = fileService.photoOCR(fullPath, userId);
        if (result != null) {
            result.put("message", "OCR处理成功");
            return ResponseEntity.ok(result);
        } else {
            return ResponseEntity.badRequest().body("OCR处理失败");
        }
    }

    @PostMapping("SR")
    public ResponseEntity<?> SR(@RequestParam("filePath") String filePath, @RequestParam("userId") int userId) {
        String fullPath = GlobalVariables.rootPath + filePath;
        String result = fileService.SR(fullPath);
        if (result != null) {
            Map<String, Object> message = new HashMap<>();
            message.put("message", "SR处理成功");
            message.put("result", result);
            return ResponseEntity.ok(message);
        } else {
            return ResponseEntity.badRequest().body("SR处理失败");
        }
    }

    @PostMapping("/Topdf")
    public ResponseEntity<?> convertWordToPdf(@RequestParam("filePath") String filePath, @RequestParam("userId") int userId) {
        String fullPath = GlobalVariables.rootPath + filePath;
        String result = fileService.convertWordToPdf(fullPath, userId);
        if (result != null) {
            Map<String, Object> message = new HashMap<>();
            message.put("message", "转换成功");
            message.put("result", result);
            return ResponseEntity.ok(message);
        } else {
            return ResponseEntity.badRequest().body("转换失败");
        }
    }

    @PostMapping("/GetPdfText")
    public ResponseEntity<?> getPdfText(@RequestParam("filePath") String filePath, @RequestParam("userId") int userId) {
        String fullPath = GlobalVariables.rootPath + filePath;
        String result = fileService.getPdfText(filePath);
        if (result != null) {
            Map<String, Object> message = new HashMap<>();
            message.put("message", "获取pdf成功");
            message.put("result", result);
            return ResponseEntity.ok(message);
        } else {
            return ResponseEntity.badRequest().body("提取pdf文本失败");
        }
    }

    @PostMapping("/mind")
    public ResponseEntity<?> getMind(@RequestParam("filePath") String filePath, @RequestParam("userId") int userId) {
        String fullPath = GlobalVariables.rootPath + filePath;
        String result = fileService.generateMindmapFromMdS(filePath, userId);
        if (result != null) {
            Map<String, Object> message = new HashMap<>();
            message.put("message", "Mindmap处理成功");
            message.put("result", result);
            return ResponseEntity.ok(message);
        } else {
            return ResponseEntity.badRequest().body("Mindmap处理失败");
        }
    }

    @PostMapping("/subtitles")
    public ResponseEntity<?> getTag(@RequestParam("filePath") String filePath, @RequestParam("userId") int userId) {
        String fullPath = GlobalVariables.rootPath + filePath;
        String result = fileService.getText(fullPath, "png");
        if (result != null) {
            Map<String, Object> message = new HashMap<>();
            message.put("message", "获取图片字幕成功");
            message.put("result", result);
            return ResponseEntity.ok(message);
        } else {
            return ResponseEntity.badRequest().body("获取标签失败");
        }
    }
}
