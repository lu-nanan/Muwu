package com.hnu.muwu.service;

import com.hnu.muwu.bean.MyFile;
import com.hnu.muwu.mapper.FileMapper;
import com.hnu.muwu.utiles.MessageQueueHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.TimeoutException;

@Service("fileService")
public class FileServiceImpl implements FileService {

    @Autowired
    private FileMapper fileMapper;

    @Override
    public int insertFile(MyFile file) {
        return fileMapper.insertFile(file.getUserId(), file.getFilename(), file.getFilePath(), file.getFileType(), file.getUploadTime(), file.getSize());
    }

    @Override
    public Boolean fileOperatorExtend(String filePath, String type) {
        if (type.equals("png") || type.equals("jpg")) {
            try {
                Map<String, Object> result = MessageQueueHelper.sendMessageAndGetResult(filePath, "is_rich_text");
                if (result != null) {
                    String status = (String) result.get("status");
                    String resultPath = (String) result.get("result");
                    if (status.equals("success")) {
                        return resultPath.equals("True");
                    } else {
                        System.out.println("文件处理失败，错误信息: " + resultPath);
                    }
                } else {
                    System.out.println("未收到处理结果或处理超时");
                }
            } catch (IOException | TimeoutException | InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
        return null;
    }
}
