package com.hnu.muwu.service;

import com.hnu.muwu.bean.ShareFileEntity;
import com.hnu.muwu.mapper.ShareFileMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service("shareFileService")
public class ShareFileServiceImpl implements ShareFileService {
    @Autowired private ShareFileMapper shareFileMapper;
    @Override
    public int saveShare(ShareFileEntity share) {
        return shareFileMapper.insert(share);
    }
}
