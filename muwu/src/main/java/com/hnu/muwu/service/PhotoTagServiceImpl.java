package com.hnu.muwu.service;

import com.hnu.muwu.bean.PhotoTag;
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

    @Override
    public String getTagByName(Integer userId, String name) {
        return photoTagMapper.getTagByName(userId, name);
    }
    @Override
    public int insert(PhotoTag photoTag) {
        return photoTagMapper.insertPhotoTag(photoTag);}
    @Override
    public int update(String userId,String oldTag,String newTag,String newName){
        return photoTagMapper.updatePhotoTag(userId,oldTag,newTag,newName);
    };
    @Override
    public int delete(String userId,String tag){
        return photoTagMapper.deleteFileTagByUserIdAndTag(userId,tag);
    }
    @Override
    public List<String> getTagByUserId(Integer userId){
        return photoTagMapper.getTagByUserId(userId);
    }
    @Override
    public void DefaultTag(int userId){
        String[] photoTag={"动物","植物","风景","人像","其他","文件"};
        String[] photoTag2={"Animal","Plants","Scenery","Portrait","Others","Documents"};
        PhotoTag photoTag1=new PhotoTag();
        photoTag1.setUserId(userId);
        //PhotoTagServiceImpl photoTagService = new PhotoTagServiceImpl();
        int i=0;
        for(String tag:photoTag){
            photoTag1.setTag(tag);
            photoTag1.setName(photoTag2[i++]);
            this.insert(photoTag1);
        }
    }
}
