package com.hnu.muwu.bean;

import java.time.LocalDateTime;

public class ShareFileEntity {

    private Integer linkId;

    private Integer fileId;

    private Integer userId;

    private String accessPassword;

    private LocalDateTime expiresAt;

    private Integer maxDownloads = 0;

    private Permission permission;

    private LocalDateTime createdAt;

    private String token;

    // 新增字段

    private String sharePath;

    private String fileName;

    public enum Permission {
        VIEW, EDIT
    }

    // 构造函数
    public ShareFileEntity() {
    }

    // 全参构造函数（可选）
    public ShareFileEntity(Integer fileId, Integer userId, String sharePath,
                           String fileName, LocalDateTime expiresAt) {
        this.fileId = fileId;
        this.userId = userId;
        this.sharePath = sharePath;
        this.fileName = fileName;
        this.expiresAt = expiresAt;
    }

    public Integer getLinkId() {
        return linkId;
    }

    public void setLinkId(Integer linkId) {
        this.linkId = linkId;
    }

    public Integer getFileId() {
        return fileId;
    }

    public void setFileId(Integer fileId) {
        this.fileId = fileId;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public String getAccessPassword() {
        return accessPassword;
    }

    public void setAccessPassword(String accessPassword) {
        this.accessPassword = accessPassword;
    }

    public LocalDateTime getExpiresAt() {
        return expiresAt;
    }

    public void setExpiresAt(LocalDateTime expiresAt) {
        this.expiresAt = expiresAt;
    }

    public Integer getMaxDownloads() {
        return maxDownloads;
    }

    public void setMaxDownloads(Integer maxDownloads) {
        this.maxDownloads = maxDownloads;
    }

    public Permission getPermission() {
        return permission;
    }

    public void setPermission(Permission permission) {
        this.permission = permission;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public String getSharePath() {
        return sharePath;
    }

    public void setSharePath(String sharePath) {
        this.sharePath = sharePath;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getToken() {
        return token;
    }
    public void setToken(String token) {
        this.token = token;
    }

    // Getter/Setter 省略，建议使用Lombok @Data
    // 如果不用Lombok需要手动添加所有字段的getter/setter

    // toString() 省略
}
