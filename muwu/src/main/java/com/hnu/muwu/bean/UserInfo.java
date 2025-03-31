package com.hnu.muwu.bean;


public class UserInfo {
    private Integer userId;
    private String telephone;
    private String username;
    private String email;
    private String passwordHash;
    private Long storageQuota = 10737418240L; // 默认值 10GB（按需保留）
    private Long usedStorage = 0L;           // 默认值 0（按需保留）

    // 无参构造
    public UserInfo() {
    }

    // 全参构造（可选）
    public UserInfo(
            Integer userId,
            String telephone,
            String username,
            String email,
            String passwordHash,
            Long storageQuota,
            Long usedStorage
    ) {
        this.userId = userId;
        this.telephone = telephone;
        this.username = username;
        this.email = email;
        this.passwordHash = passwordHash;
        this.storageQuota = storageQuota;
        this.usedStorage = usedStorage;
    }

    // Getters & Setters
    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
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


    // 可选：toString() 方法
    @Override
    public String toString() {
        return "User{" +
                "userId=" + userId +
                ", telephone='" + telephone + '\'' +
                ", username='" + username + '\'' +
                ", email='" + email + '\'' +
                ", passwordHash='" + passwordHash + '\'' +
                ", storageQuota=" + storageQuota +
                ", usedStorage=" + usedStorage +
                '}';
    }
}