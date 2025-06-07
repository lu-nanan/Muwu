package com.hnu.muwu.service;

import com.hnu.muwu.bean.PhotoTag;

import java.util.List;

public interface PhotoTagService {

    List<String> getTagsByUserId(Integer userId);

    String getTagByName(Integer userId, String name);
    List<String> getTagByUserId(Integer userId);
    int insert(PhotoTag photoTag);
    int update(String userId,String oldTag,String newTag,String newName);
    int delete(String userId,String tag);

    void DefaultTag(int userId);
}
