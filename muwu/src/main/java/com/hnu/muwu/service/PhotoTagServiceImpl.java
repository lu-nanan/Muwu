package com.hnu.muwu.service;

import com.hnu.muwu.mapper.PhotoTagMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service("photoTagService")
public class PhotoTagServiceImpl implements PhotoTagService{

    @Autowired
    private PhotoTagMapper photoTagMapper;

    @Override
    public List<String> getTagsByUserId(Integer userId) {
        return photoTagMapper.getTagsByUserId(userId);
    }
}
