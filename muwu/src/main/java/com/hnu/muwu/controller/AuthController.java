package com.hnu.muwu.controller;

import ch.qos.logback.classic.util.LogbackMDCAdapter;
import com.hnu.muwu.DTO.LoginRequest;
import com.hnu.muwu.service.UserService;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/auth")
public class AuthController {

    @Resource
    private UserService userService;


    /**
     * 账密登录验证
     *
     * @param request      HTTP请求对象，用于获取Session
     * @param loginRequest 包含用户名和密码的请求体
     * @return ResponseEntity 返回登录结果
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(HttpServletRequest request, @RequestBody LoginRequest loginRequest) {
        String account = loginRequest.getAccount();
        String password = loginRequest.getPassword();
        System.out.println(account);
        System.out.println(password);
        Map<String, Object> response = new HashMap<>();
        if (account == null || password == null) {
            response.put("message", "Invalid username or password");
            return ResponseEntity.badRequest().body(response);
        }
        boolean isValid;
        Integer userId;
        // 判断其为手机号、账号还是邮箱
        if (account.contains("@")) {
            userId = userService.getUserIdByEmail(account);
            if (userId == -1) {
                response.put("message", "当前邮箱未注册，请先注册");
                return ResponseEntity.badRequest().body(response);
            }
        } else if (account.length() == 11) {
            userId = userService.getUserIdByPhone(account);
            if (userId == -1) {
                response.put("message", "当前手机号未注册，请先注册");
                return ResponseEntity.badRequest().body(response);
            }
        } else {
            userId = Integer.parseInt(account);
            if (!userService.checkUserAccount(account)) {
                response.put("message", "账号输入错误");
                return ResponseEntity.badRequest().body(response);
            }
        }
        System.out.println(userId);
        isValid = userService.checkCredentialsWithUserId(userId, password);
        if (isValid) {
            response.put("message", "登录成功");
            response.put("userId", userId);
            return ResponseEntity.ok(response);
        } else {
            response.put("message", "登录失败");
            return ResponseEntity.badRequest().body(response);
        }
    }
}