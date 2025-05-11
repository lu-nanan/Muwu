package com.hnu.muwu.controller;


import com.hnu.muwu.DTO.SendVerificationCodeRequest;
import com.hnu.muwu.service.EmailService;
import com.hnu.muwu.service.UserService;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/verification")
public class VerificationCodeController {

    @Resource
    private UserService userService;

    @Resource
    private EmailService emailHelper;

    /**
     * 发送验证码
     *
     * @param email 邮箱地址
     * @return ResponseEntity 返回发送结果
     */
    @PostMapping("/send")
    public ResponseEntity<?> sendVerificationCode(@RequestParam String email) {
        try {
            if (userService.getUserIdByEmail(email) == -1) {
                return ResponseEntity.badRequest().body("当前邮箱未注册，请先注册");
            }
            emailHelper.sendVerificationCode(email);
            return ResponseEntity.ok("验证码发送成功。");
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
    @PostMapping("/sendRegisterVerificationCode")
    public ResponseEntity<?> sendRegisterVerificationCode(HttpServletRequest request, @RequestBody SendVerificationCodeRequest sendVerificationCodeRequest) {
        String email = sendVerificationCodeRequest.getEmail();
        try {
            emailHelper.sendVerificationCode(email);
            return ResponseEntity.ok("验证码发送成功。");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("发送失败，稍后再试");
        }
    }

    /**
     * 验证验证码
     *
     * @param email 邮箱地址
     * @param code  用户输入的验证码
     * @return ResponseEntity 返回验证结果
     */
    @PostMapping("/verify")
    public ResponseEntity<?> verifyCode(@RequestParam String email, @RequestParam String code) {
        boolean isValid = emailHelper.verifyCode(email, code);
        if (isValid) {
            return ResponseEntity.ok("验证码验证成功。");
        } else {
            return ResponseEntity.badRequest().body("验证码无效或已过期。");
        }
    }
}
