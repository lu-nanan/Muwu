package com.hnu.muwu.controller;


import com.hnu.muwu.bean.FileTag;
import com.hnu.muwu.bean.PhotoTag;
import com.hnu.muwu.service.FileTagServiceImpl;
import com.hnu.muwu.service.PhotoTagServiceImpl;
import com.hnu.muwu.utiles.TranslateHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/tag")
public class TagController {
    @Autowired
    TranslateHelper translateHelper = new TranslateHelper();
    @Autowired
    PhotoTagServiceImpl photoTagService;
    @Autowired
    FileTagServiceImpl fileTagService;
    @GetMapping("/get")
    public ResponseEntity<?> getTag(@RequestParam("userId") Integer userId) {
        List<String> photoTag=photoTagService.getTagByUserId(userId);
        List<String> FilesTag=fileTagService.getTagsByUserId(userId);
        Map<String, Object> response = new HashMap<>();
        response.put("PhotoTag", photoTag);
        response.put("FileTag", FilesTag);
        return ResponseEntity.ok(response);
    }
    @PostMapping("/add")
    public ResponseEntity<?> addTag(@RequestParam("userId") Integer userId, @RequestParam("tag") String tag,@RequestParam("type") String type) {
        System.out.println(tag);
        System.out.println(type);
        System.out.println(userId);
        if(tag.isEmpty()){
            Map<String, Object> response = new HashMap<>();
            response.put("Message", "tag为空");
            return ResponseEntity.badRequest().body(response);
        }
        try{
            if(type.equals("图片")){
                PhotoTag photoTag=new PhotoTag();
                photoTag.setUserId(userId);
                photoTag.setTag(tag);
                photoTag.setName(TranslateHelper.translateChinese(tag));
                photoTagService.insert(photoTag);
            }
            else{
                FileTag fileTag=new FileTag();
                fileTag.setUserId(userId);
                fileTag.setTag(tag);
                fileTagService.insert(fileTag);
            }
            Map<String, Object> response = new HashMap<>();
            response.put("Message", "ok");
            return ResponseEntity.ok(response);
        }
        catch (Exception e){
            System.out.println(e.getMessage());
            return ResponseEntity.badRequest().body("添加失败");
        }

    }
    @PostMapping("/update")
    public ResponseEntity<?> updateTag(@RequestParam("userId") String userId, @RequestParam("oldtag") String oldtag,@RequestParam("newtag") String newtag,@RequestParam("type") String type){
        System.out.println(oldtag);
        System.out.println(type);
        System.out.println(userId);
        System.out.println(newtag);
        try{
            if(type.equals("图片")){
                System.out.println("图片");
                photoTagService.update(userId,oldtag,newtag,TranslateHelper.translateChinese(newtag));
            }
            else {
                System.out.println("文件");
                fileTagService.update(userId,oldtag,newtag);
            }
            Map<String, Object> response = new HashMap<>();
            response.put("Message", "ok");
            return ResponseEntity.ok(response);
        }
        catch (Exception e){
            System.out.println(e.getMessage());
            return ResponseEntity.badRequest().body("更新失败");
        }

    }
    @PostMapping("/delete")
    public ResponseEntity<?> updateTag(@RequestParam("userId") String userId, @RequestParam("tag") String tag,@RequestParam("type") String type){
        try{
            if(type.equals("图片")){
                photoTagService.delete(userId,tag);
            }
            else {
                fileTagService.delete(userId,tag);
            }
            Map<String, Object> response = new HashMap<>();
            response.put("Message", "ok");
            return ResponseEntity.ok(response);
        }
        catch (Exception e){
            System.out.println(e.getMessage());
            return ResponseEntity.badRequest().body("删除失败");
        }

    }


}
