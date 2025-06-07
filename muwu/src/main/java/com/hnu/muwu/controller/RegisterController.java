package com.hnu.muwu.controller;


import com.hnu.muwu.DTO.RegisterRequest;
import com.hnu.muwu.bean.PhotoTag;
import com.hnu.muwu.config.GlobalVariables;
import com.hnu.muwu.service.EmailServiceImpl;
import com.hnu.muwu.service.FileTagServiceImpl;
import com.hnu.muwu.service.PhotoTagServiceImpl;
import com.hnu.muwu.service.UserService;
import com.hnu.muwu.utiles.HashCodeHelper;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.File;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/auth" )
public class RegisterController {
    @Resource
    private UserService userService;
    @Resource
    private EmailServiceImpl emailService;
    @Resource
    private FileTagServiceImpl fileTagService;
    @Resource
    private PhotoTagServiceImpl photoTagServiceImpl;

    @PostMapping("/register")
    public ResponseEntity<?> Register(HttpServletRequest request, @RequestBody RegisterRequest registerRequest) {
        System.out.println(registerRequest);
        String username=registerRequest.getUsername();
        String password=registerRequest.getPasswordHash();
        String phone=registerRequest.getTelephone();
        String email=registerRequest.getEmail();
        System.out.println(username);
        System.out.println(password);
        System.out.println(phone);
        System.out.println(email);
        int verificationCode=registerRequest.getVerificationCode();
        // 验证输入信息是否为空
        if (username == null || username.isEmpty() ||
                password == null || password.isEmpty() ||
                phone == null || phone.isEmpty() ||
                email == null || email.isEmpty()) {
            return ResponseEntity.badRequest().body("注册失败，请输入完整信息");
        }
        if(userService.getUserIdByEmail(email) != -1){
            return ResponseEntity.badRequest().body("注册失败，邮箱已存在");
        }
        if(userService.getUserIdByPhone(phone) != -1){
            return ResponseEntity.badRequest().body("注册失败，手机号已存在");
        }
        if(!emailService.verifyCode(email,String.valueOf(verificationCode))){
            return ResponseEntity.badRequest().body("验证码错误");
        }

        try {
            String salt = HashCodeHelper.generateSalt();
            String hashPassword = HashCodeHelper.hashPassword(password, salt);
            registerRequest.setPasswordHash(salt + ":" + hashPassword);
        }catch (Exception e){return ResponseEntity.badRequest().body("系统错误");}
        // 调用服务层的注册方法
        try {
            if(userService.insertUser(registerRequest) == 1){
                System.out.println(userService.getUserIdByPhone(phone));
                int userId=userService.getUserIdByEmail(email);
                String path= GlobalVariables.rootPath + File.separator + userId;
                File directory = new File(path);
                directory.mkdirs();
                fileTagService.DefaultTag(userId);
                photoTagServiceImpl.DefaultTag(userId);
                System.out.println("5");

                return ResponseEntity.ok("注册成功");
            }
            else{
                return ResponseEntity.badRequest().body("服务器繁忙，注册失败");
            }
        }
        catch (Exception e){
            System.out.println(e.getMessage());
            return ResponseEntity.badRequest().body("服务器繁忙，注册失败");
        }



    }


}
