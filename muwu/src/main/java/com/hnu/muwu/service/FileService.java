package com.hnu.muwu.service;

import com.hnu.muwu.bean.FinalFile;
import com.hnu.muwu.bean.MyFile;

import java.util.List;
import java.util.Map;

public interface FileService {

    int insertFile(FinalFile file);

    MyFile getAndDeleteMyFile(Integer userId);

    FinalFile getFileByName(String name, Integer userId);

    List<FinalFile> searchFilesByNameLike(String keyword, Integer userId);

    List<FinalFile> searchFilesByQianwen(String keyword, Integer userId);

    String fileOperatorExtend(String filePath, String type);

    String getTag (String filePath, Integer userId, String fileType);

    String getText (String filePath, String fileType);

    String getPath (Integer userId, String tag , MyFile file, String text);

    String generateMindmapFromMd(String filePath, Integer userId);

    String generateMindmapFromMdS(String filePath, Integer userId);

    Map<String, Object> photoOCR(String filePath, Integer userId);

    String getFileDescription(String filePath, String content);

    String convertWordToPdf(String filePath, int userId);

    String getPdfText(String filePath);
}
