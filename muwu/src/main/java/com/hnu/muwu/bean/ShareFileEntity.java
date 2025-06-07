package com.hnu.muwu.bean;

import java.sql.Timestamp;
import java.time.LocalDateTime;

public class ShareFileEntity {

    private Integer linkId;


    private Integer userId;


    private Timestamp created_at;

    // 新增字段
    private String sharePath;

    private String fileName;
    private String url;
    private String qrcodePath;



    // 构造函数
    public ShareFileEntity() {
    }

    // 全参构造函数（可选）
    public ShareFileEntity(Integer fileId, Integer userId, String sharePath,
                           String fileName, Timestamp expiresAt) {
        this.userId = userId;
        this.sharePath = sharePath;
        this.fileName = fileName;
    }
    public String getUrl() {return url;}
    public String getQrcodePath(){return qrcodePath;}
    public void setUrl(String url) {this.url = url;}
    public void setQrcodePath(String qrcodePath) {this.qrcodePath = qrcodePath;}

    public Integer getLinkId() {
        return linkId;
    }
    public void setLinkId(Integer linkId) {
        this.linkId = linkId;
    }


    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }


    public Timestamp getCreatedAt() {
        return created_at;
    }

    public void setCreatedAt(Timestamp createdAt) {
        this.created_at = createdAt;
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


    // Getter/Setter 省略，建议使用Lombok @Data
    // 如果不用Lombok需要手动添加所有字段的getter/setter

    // toString() 省略
}
