package com.hnu.muwu.service;

import com.hnu.muwu.bean.FileTag;

import java.util.List;

public interface FileTagService {
    List<String> getTagsByUserId(Integer userId);

    String getTagByContent(Integer userId, String filePath, String content);
    //String getTag(Integer userId, String filePath);
    int insert(FileTag fileTag);
    int update(String userId,String oldTag,String newTag);
    int delete(String userId,String tag);

    void DefaultTag(int userId);
}
