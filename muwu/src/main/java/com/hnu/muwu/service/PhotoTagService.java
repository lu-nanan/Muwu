package com.hnu.muwu.service;

import java.util.List;

public interface PhotoTagService {

    List<String> getTagsByUserId(Integer userId);

}
