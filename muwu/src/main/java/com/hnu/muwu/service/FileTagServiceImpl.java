package com.hnu.muwu.service;

import com.hnu.muwu.bean.FileTag;
import com.hnu.muwu.bean.PhotoTag;
import com.hnu.muwu.mapper.FileTagMapper;
import com.hnu.muwu.utiles.QianwenHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service("fileTagService")
public class FileTagServiceImpl implements FileTagService {

    @Autowired
    private FileTagMapper fileTagMapper;

    @Override
    public List<String> getTagsByUserId(Integer userId) {
        return fileTagMapper.getTagsByUserId(userId);
    }

    @Override
    public String getTagByContent(Integer userId, String filePath, String content) {
        List<String> tags = this.getTagsByUserId(userId);
        String question = "请根据文件的内容，从下面的tags字符串列表中选择一个最合适的tag返回，直接回答最合适的tag，如：工作，不可包含其他任何内容。\n" + tags.toString() + "\n" + content;
        System.out.println(question.length());
        try {
            return QianwenHelper.processMessage(question);
        } catch (Exception e) {
            System.out.println(e.getMessage());
            return null;
        }
    }
    @Override
    public int insert(FileTag fileTag) {return fileTagMapper.insertFileTag(fileTag);}
    @Override
    public int update(String userId,String oldTag,String newTag){
        return fileTagMapper.updateFileTag(userId,oldTag,newTag);
    }
    @Override
    public int delete(String userId,String tag){
        return fileTagMapper.deleteFileTagByUserIdAndTag(userId,tag);
    }
    @Override
    public void DefaultTag(int userId){

        String[] fileTag={"工作","学习","生活","其他"};
        FileTag fileTag1=new FileTag();
        fileTag1.setUserId(userId);
        FileTagServiceImpl fileTagService = new FileTagServiceImpl();
        for(String tag:fileTag){
            fileTag1.setTag(tag);
            this.insert(fileTag1);
        }
    }
}
