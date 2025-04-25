package com.hnu.muwu.controller;


import com.hnu.muwu.DTO.RegisterRequest;
import com.hnu.muwu.service.EmailServiceImpl;
import com.hnu.muwu.service.UserService;
import com.hnu.muwu.utiles.HashCodeHelper;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/auth" )
public class RegisterController {
    @Resource
    private UserService userService;
    @Resource
    private EmailServiceImpl emailService;
    private HashCodeHelper hashCodeHelper = new HashCodeHelper();


    @PostMapping("/register")
    public ResponseEntity<?> Register(HttpServletRequest request, @RequestBody RegisterRequest registerRequest) {
        String username=registerRequest.getUsername();
        String password=registerRequest.getPasswordHash();
        String phone=registerRequest.getTelephone();
        String email=registerRequest.getEmail();
        int verificationCode=registerRequest.getVerificationCode();
        // 验证输入信息是否为空
        if (username == null || username.isEmpty() ||
                password == null || password.isEmpty() ||
                phone == null || phone.isEmpty() ||
                email == null || email.isEmpty()) {
            return ResponseEntity.badRequest().body("注册失败，请输入完整信息");
        }
        if(userService.isEmailExists(email)){
            return ResponseEntity.badRequest().body("注册失败，邮箱已存在");
        }
        if(userService.isPhoneExists(phone)){
            return ResponseEntity.badRequest().body("注册失败，手机号已存在");
        }
        if(!emailService.verifyCode(email,String.valueOf(verificationCode))){
            return ResponseEntity.badRequest().body("验证码错误");
        }

        try {
            registerRequest.setPasswordHash(HashCodeHelper.hashPassword(password,HashCodeHelper.generateSalt()));
        }catch (Exception e){return ResponseEntity.badRequest().body("系统错误");}
        // 调用服务层的注册方法
        if(userService.insertUser(registerRequest)==1){
            return ResponseEntity.ok("注册成功");
        }
        else{
            return ResponseEntity.badRequest().body("服务器繁忙，注册失败");
        }


    }
}
