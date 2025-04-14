package com.hnu.muwu.controller;

import com.hnu.muwu.DTO.LoginRequest;
import com.hnu.muwu.service.UserService;
import com.hnu.muwu.service.EmailService;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/auth")
public class AuthController {

    @Resource
    private UserService userService;

    @Resource
    private EmailService emailHelper;

    /**
     * 账密登录验证
     *
     * @param request      HTTP请求对象，用于获取Session
     * @param loginRequest 包含用户名和密码的请求体
     * @return ResponseEntity 返回登录结果
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(HttpServletRequest request, @RequestBody LoginRequest loginRequest) {
        String count = loginRequest.getCount();
        String password = loginRequest.getPassword();
        if (count == null || password == null) {
            return ResponseEntity.badRequest().body("Invalid username or password");
        }
        boolean isValid;
        int userId;
        // 判断其为手机号、账号还是邮箱
        if (count.contains("@")) {
            userId = userService.getUserIdByEmail(count);
        } else if (count.length() == 11) {
            userId = userService.getUserIdByPhone(count);
        } else {
            userId = Integer.parseInt(count);
        }
        isValid = userService.checkCredentialsWithUserId(userId, password);
        if (isValid) {
            HttpSession session = request.getSession();
            session.setAttribute("user", userId);
            return ResponseEntity.ok("登录成功");
        } else {
            return ResponseEntity.badRequest().body("Invalid username or password");
        }
    }

    /**
     * 发送验证码
     *
     * @param email 邮箱地址
     * @return ResponseEntity 返回发送结果
     */
    @PostMapping("/sendVerificationCode")
    public ResponseEntity<?> sendVerificationCode(@RequestParam String email) {
        try {
            emailHelper.sendVerificationCode(email);
            return ResponseEntity.ok("验证码发送成功。");
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * 验证验证码
     *
     * @param email 邮箱地址
     * @param code  用户输入的验证码
     * @return ResponseEntity 返回验证结果
     */
    @PostMapping("/verifyCode")
    public ResponseEntity<?> verifyCode(@RequestParam String email, @RequestParam String code) {
        boolean isValid = emailHelper.verifyCode(email, code);
        if (isValid) {
            return ResponseEntity.ok("验证码验证成功。");
        } else {
            return ResponseEntity.badRequest().body("验证码无效或已过期。");
        }
    }
}