package com.hnu.muwu.DTO;

public class RegisterRequest {
    private int userId;
    private String telephone;
    private String username;
    private String email;
    private String passwordHash;
    private Long storageQuota = 10737418240L; // 默认值 10GB（按需保留）
    private Long usedStorage = 0L;
    private int verificationCode;

    public RegisterRequest() {
    }

    public RegisterRequest(String count, String password, String username, String email, String telephone) {
        this.passwordHash = password;
        this.username = username;
        this.email = email;
        this.telephone = telephone;
    }
    public int getVerificationCode() {
        return verificationCode;
    }
    public void setVerificationCode(int verificationCode) {
        this.verificationCode=verificationCode;
    }


    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getTelephone() {
        return telephone;
    }

    public void setTelephone(String telephone) {
        this.telephone = telephone;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public void setPasswordHash(String passwordHash) {
        this.passwordHash = passwordHash;
    }

    public Long getStorageQuota() {
        return storageQuota;
    }

    public void setStorageQuota(Long storageQuota) {
        this.storageQuota = storageQuota;
    }

    public Long getUsedStorage() {
        return usedStorage;
    }

    public void setUsedStorage(Long usedStorage) {
        this.usedStorage = usedStorage;
    }
}
