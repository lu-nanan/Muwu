package com.hnu.muwu.controller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VerifyCodeController {

    @Autowired
    private StringRedisTemplate redisTemplate;

    @GetMapping("/verifyVerificationCode")
    public String verifyVerificationCode(@RequestParam String phoneNumber, @RequestParam String inputCode) {
        // 从 Redis 中获取存储的验证码
        String storedCode = redisTemplate.opsForValue().get(phoneNumber);

        if (storedCode != null && storedCode.equals(inputCode)) {
            // 验证成功后删除 Redis 中的验证码
            redisTemplate.delete(phoneNumber);
            return "验证码验证成功";
        } else {
            return "验证码验证失败";
        }
    }
}

