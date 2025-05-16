package com.hnu.muwu.service;

import java.util.List;

public interface FileTagService {
    List<String> getTagsByUserId(Integer userId);

    String getTag(Integer userId, String filePath);
}
