package com.hnu.muwu.service;

import com.hnu.muwu.bean.ShareFileEntity;
import com.hnu.muwu.mapper.ShareFileMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service("shareFileService")
public class ShareFileServiceImpl implements ShareFileService {
    @Autowired private ShareFileMapper shareFileMapper;
    @Override
    public int saveShare(ShareFileEntity share) {
        return shareFileMapper.insertShareFile(share);
    }
    /**
     * 根据用户ID获取该用户的所有文件分享记录
     * @param userId 用户ID
     * @return 该用户的文件分享列表，按创建时间降序排列
     */
    @Override
    public List<ShareFileEntity> getShareFilesByUserId(Integer userId) {

        try {
            // 2. 调用Mapper查询数据
            List<ShareFileEntity> shareFiles = shareFileMapper.getShareFilesByUserId(userId);


            // 按创建时间降序排序
            shareFiles.sort((f1, f2) -> f2.getCreatedAt().compareTo(f1.getCreatedAt()));

            return shareFiles;

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return null;
    }
}
