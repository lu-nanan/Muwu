package com.hnu.muwu.service;


import lombok.Getter;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import java.security.SecureRandom;
import java.time.Duration;
import java.util.Collections;
import java.util.concurrent.TimeUnit;

@Getter
@Service("emailService")
public class EmailServiceImpl implements EmailService {

    private static final String VERIFICATION_PREFIX = "verification:";
    private static final String LAST_SEND_TIME_PREFIX = "last_send_time:";
    private static final long SEND_INTERVAL_MINUTES = 1;

    private final RedisTemplate<String, String> redisTemplate;
    private final JavaMailSender mailSender;

    public EmailServiceImpl(RedisTemplate<String, String> redisTemplate, JavaMailSender mailSender) {
        this.redisTemplate = redisTemplate;
        this.mailSender = mailSender;
    }

    /**
     * 检查是否可以发送验证码，确保两次发送间隔大于一分钟
     */
    @Override
    public boolean canSendVerificationCode(String email) {
        String lastSendTimeKey = LAST_SEND_TIME_PREFIX + email;
        String lastSendTimeStr = redisTemplate.opsForValue().get(lastSendTimeKey);
        if (lastSendTimeStr != null) {
            long lastSendTime = Long.parseLong(lastSendTimeStr);
            long currentTime = System.currentTimeMillis();
            long minutesPassed = TimeUnit.MILLISECONDS.toMinutes(currentTime - lastSendTime);
            return minutesPassed >= SEND_INTERVAL_MINUTES;
        }
        return true; // 如果没有记录上次发送时间，允许发送
    }

    /**
     * 发送验证码，并在Redis中存储验证码和发送时间
     */
    @Override
    public void sendVerificationCode(String email) {
        if (!canSendVerificationCode(email)) {
            throw new RuntimeException("请等待一分钟后再发送验证码。");
        }

        String code = generateSecureCode(6);
        String verificationKey = VERIFICATION_PREFIX + email;
        String lastSendTimeKey = LAST_SEND_TIME_PREFIX + email;

        // 存储验证码，设置5分钟过期
        redisTemplate.opsForValue().set(verificationKey, code, Duration.ofMinutes(5));
        // 记录发送时间，同样设置5分钟过期
        redisTemplate.opsForValue().set(lastSendTimeKey, String.valueOf(System.currentTimeMillis()), Duration.ofMinutes(5));

        sendEmail(email, "验证码", "您的验证码是：" + code);
    }

    /**
     * 生成安全的6位验证码
     */
    private String generateSecureCode(int length) {
        SecureRandom random = new SecureRandom();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < length; i++) {
            sb.append(random.nextInt(10));
        }
        return sb.toString();
    }

    /**
     * 发送邮件
     */
    private void sendEmail(String to, String subject, String text) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom("lu_nanan@foxmail.com");
        message.setTo(to);
        message.setSubject(subject);
        message.setText(text);
        mailSender.send(message);
    }

    /**
     * 验证输入的验证码是否正确，正确时删除Redis中的验证码
     */
    @Override
    public boolean verifyCode(String email, String inputCode) {
        String key = VERIFICATION_PREFIX + email;
        // Lua脚本：原子性地验证并删除验证码
        String script =
                "if redis.call('get', KEYS[1]) == ARGV[1] then " +
                        "    return redis.call('del', KEYS[1]) " +
                        "else " +
                        "    return 0 " +
                        "end";
        Long result = redisTemplate.execute(
                new DefaultRedisScript<>(script, Long.class),
                Collections.singletonList(key),
                inputCode
        );
        return result > 0;
    }
}
