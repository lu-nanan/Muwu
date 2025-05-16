package com.hnu.muwu.service;

import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.hnu.muwu.bean.FinalFile;
import com.hnu.muwu.bean.MyFile;
import com.hnu.muwu.config.GlobalVariables;
import com.hnu.muwu.mapper.FileMapper;
import com.hnu.muwu.utiles.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.data.redis.core.RedisTemplate;


import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeoutException;

@Service("fileService")
public class FileServiceImpl implements FileService {

    @Autowired
    private FileMapper fileMapper;

    @Autowired
    private PhotoTagService photoTagService;

    @Autowired
    private FileTagService fileTagService;

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @Override
    public int insertFile(FinalFile file) {
        return fileMapper.insertFile(file.getUserId(), file.getFilename(), file.getFilePath(), file.getFileType(), file.getUploadTime(), file.getSize(), file.getTag(), file.getDescription());
    }

    @Override
    public String getTag (String filePath, Integer userId) {
        List<String> tags = photoTagService.getTagsByUserId(userId);
        HashMap<String, Object> message = new HashMap<>();
        message.put("file_path", filePath);
        message.put("operation", "get_photo_tag");
        message.put("text_descriptions", tags);
        try {
            Map<String, Object> result = MessageQueueHelper.sendMessageAndGetResult(message);
            if (result != null) {
                return photoTagService.getTagByName(userId, (String) result.get("result"));
            }
        } catch (IOException | TimeoutException | InterruptedException e) {
            throw new RuntimeException(e);
        }
        return null;
    }

    @Override
    public String getText (String filePath) {
        HashMap<String, Object> message = new HashMap<>();
        message.put("file_path", filePath);
        message.put("operation", "generate_caption");
        try {
            Map<String, Object> result = MessageQueueHelper.sendMessageAndGetResult(message);
            if (result != null) {
                return TranslateHelper.translate((String) result.get("result"));
            }
        } catch (IOException | TimeoutException | InterruptedException e) {
            throw new RuntimeException(e);
        }
        return null;
    }

    @Override
    public String getPath(Integer userId, String tag, MyFile file, String text){
        String fileTree = FileTreeHelper.generateFileTree(GlobalVariables.rootPath + File.separator + userId);
        HashMap<String, Object> message = new HashMap<>();
        message.put("file-infomation", file);
        message.put("text-descriptions", text);
        message.put("file-tree", fileTree);
        message.put("tag", tag);
        String question = "请根据下面的文件信息，结合用户已有的文件结构和文件存放习惯，综合考虑用户习惯和查找检索方便等因素，直接给出此文件合适的存放路径(路径需包含文件名，从用户文件起始，如：100000/images/image.png),回答不要包含其他任何的内容" + message.toString();
        try {
            return QianwenHelper.processMessage(question);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return null;
    }

    @Override
    public MyFile getAndDeleteMyFile(Integer userId) {
        String key = userId.toString();
        String json = redisTemplate.opsForValue().get(key);
        System.out.println("json: " + json);
        if (json != null) {
            try {
                redisTemplate.delete(key);
                ObjectMapper mapper = new ObjectMapper();
                return mapper.readValue(json, MyFile.class);
            } catch (IOException e) {
                throw new RuntimeException("反序列化 MyFile 失败", e);
            }
        }
        return null;
    }

    @Override
    public String fileOperatorExtend(String filePath, String type) {
        if (type.equals("png") || type.equals("jpg")) {
            return photoExtend(filePath);
        }
        return null;
    }

    public String photoExtend(String filePath) {
        try {
            HashMap<String, Object> message = new HashMap<>();
            message.put("file_path", filePath);
            message.put("operation", "is_rich_text");
            Map<String, Object> result = MessageQueueHelper.sendMessageAndGetResult(message);
            if (result != null) {
                String status = (String) result.get("status");
                Boolean re = (Boolean) result.get("result");
                if (status.equals("success")) {
                    if (re) {
                        redisTemplate.opsForValue().set(filePath, "OCR");
                        return "检测到图片为富文本图片，是否提取图片文本";
                    } else {
                        return null;
                    }
                } else {
                    System.out.println("文件处理失败，错误信息: " + re);
                    return null;
                }
            } else {
                System.out.println("未收到处理结果或处理超时");
            }
        } catch (IOException | TimeoutException | InterruptedException e) {
            throw new RuntimeException(e);
        }
        return null;
    }

    public Map<String, Object> photoOCR (String filePath,  Integer userId) {
        try {
            HashMap<String, Object> message = new HashMap<>();
            message.put("file_path", filePath);
            message.put("operation", "OCR");
            Map<String, Object> result = MessageQueueHelper.sendMessageAndGetResult(message);
            if (result != null) {
                String status = (String) result.get("status");
                if (status.equals("success")) {
                    Map<String, Object> re = new HashMap<>();
                    re.put("text", (String) result.get("result"));
                    re.put("path", (String) result.get("file_path"));
                    System.out.println("读取的文件路径" + result.get("file_path"));
                    MyFile OCRResult = FileHelper.createMyFileFromPath((String) result.get("file_path"), userId);
                    String tag = fileTagService.getTag(userId, (String) result.get("file_path"));
                    String description = this.getFileDescription((String) result.get("file_path"));
                    assert OCRResult != null;
                    this.insertFile(new FinalFile(OCRResult, tag, description));
                    return re;
                } else {
                    return null;
                }
            }
        } catch (IOException | TimeoutException | InterruptedException e) {
            throw new RuntimeException(e);
        }
        return null;
    }

    @Override
    public String getFileDescription(String filePath) {
        try {
            String content = FileHelper.readFileContent(filePath);
            String question = "请根据下面的文件内容，生成一个50字左右的概述，回答应只包含概述内容，不可包含任何其他内容\n" + content;
            System.out.println(question);
            return QianwenHelper.processMessage(question);
        } catch (NoApiKeyException | InputRequiredException e) {
            throw new RuntimeException(e);
        }
    }
}
