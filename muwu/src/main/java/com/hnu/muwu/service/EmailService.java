package com.hnu.muwu.service;

public interface EmailService {

    boolean canSendVerificationCode(String email);

    void sendVerificationCode(String email);

    boolean verifyCode(String email, String inputCode);
}
