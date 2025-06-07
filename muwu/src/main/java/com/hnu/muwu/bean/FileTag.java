package com.hnu.muwu.bean;

public class FileTag {
    private Integer  id;
    private Integer userId;

    private String tag;

    public FileTag() {
    }

    public FileTag(Integer userId, String tag ) {
        this.userId = userId;
        this.tag = tag;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public String getTag() {return tag;}
    public void setTag(String tag) {this.tag=tag;}
    public Integer getId() {
        return id;
    }
    public void setId(Integer id) {this.id = id;}

    @Override
    public String toString() {
        return "PhotoTag{" +
                "userId=" + userId +
                ", tagName='" + tag + '\'' +
                '}';
    }
}

