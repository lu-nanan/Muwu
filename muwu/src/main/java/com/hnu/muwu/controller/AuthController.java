package com.hnu.muwu.controller;

import com.hnu.muwu.DTO.LoginRequest;
import com.hnu.muwu.service.UserService;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/auth" )
public class AuthController {

    @Resource
    private UserService userService;

    /*
    * 账密登录验证
    *
    * @param loginRequest 包含用户名和密码的请求体
    * @return
    *
    * */
    @PostMapping("/login")
    public ResponseEntity<?> login(HttpServletRequest request, @RequestBody LoginRequest loginRequest) {
        String count = loginRequest.getCount();
        String password = loginRequest.getPassword();
        if (count == null || password == null) {
            return ResponseEntity.badRequest().body("Invalid username or password");
        }
        boolean isValid;
        int userId;
        //判断其为手机号、账号还是邮箱
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
}


