package com.hnu.muwu.bean;

public class PhotoTag {

    private Integer userId;
    private String tagName;

    public PhotoTag() {
    }

    public PhotoTag(Integer userId, String tagName) {
        this.userId = userId;
        this.tagName = tagName;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public String getTagName() {
        return tagName;
    }

    public void setTagName(String tagName) {
        this.tagName = tagName;
    }

    @Override
    public String toString() {
        return "PhotoTag{" +
                "userId=" + userId +
                ", tagName='" + tagName + '\'' +
                '}';
    }
}
