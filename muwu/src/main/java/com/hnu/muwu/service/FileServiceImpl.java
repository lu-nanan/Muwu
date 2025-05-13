package com.hnu.muwu.service;

import com.hnu.muwu.bean.MyFile;
import com.hnu.muwu.mapper.FileMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service("fileService")
public class FileServiceImpl {

    @Autowired
    private FileMapper fileMapper;
    public int insertFile(MyFile file) {
        return fileMapper.insertFile(file.getUserId(), file.getFilename(), file.getFilePath(), file.getFileType(), file.getUploadTime(), file.getSize());
    }
}
