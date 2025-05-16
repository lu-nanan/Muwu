package com.hnu.muwu.service;

import com.hnu.muwu.bean.FinalFile;
import com.hnu.muwu.bean.MyFile;

public interface FileService {

    int insertFile(FinalFile file);

    MyFile getAndDeleteMyFile(Integer userId);

    FinalFile getFileByName(String name, Integer userId);

    String fileOperatorExtend(String filePath, String type);

    String getTag (String filePath, Integer userId);

    String getText (String filePath);

    String getPath (Integer userId, String tag , MyFile file, String text);

    String getFileDescription(String filePath);

}
