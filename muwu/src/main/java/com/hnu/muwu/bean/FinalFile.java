package com.hnu.muwu.bean;

import java.sql.Timestamp;

public class FinalFile {
    private int userId;
    private String filename;
    private String filePath;
    private String fileType;
    private Timestamp uploadTime;
    private long size;
    private String tag;
    private String description;

    public FinalFile() {}

    public FinalFile(int userId, String filename, String filePath, String fileType, Timestamp uploadTime, long size, String tag, String description) {
        this.userId = userId;
        this.filename = filename;
        this.filePath = filePath;
        this.fileType = fileType;
        this.uploadTime = uploadTime;
        this.size = size;
        this.tag = tag;
        this.description = description;
    }

    public FinalFile(MyFile myFile, String tag, String description) {
        this.userId = myFile.getUserId();
        this.filename = myFile.getFilename();
        this.filePath = myFile.getFilePath();
        this.fileType = myFile.getFileType();
        this.uploadTime = myFile.getUploadTime();
        this.size = myFile.getSize();
        this.tag = tag;
        this.description = description;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getFilename() {
        return filename;
    }

    public void setFilename(String filename) {
        this.filename = filename;
    }

    public String getFilePath() {
        return filePath;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public Timestamp getUploadTime() {
        return uploadTime;
    }

    public void setUploadTime(Timestamp uploadTime) {
        this.uploadTime = uploadTime;
    }

    public long getSize() {
        return size;
    }

    public void setSize(long size) {
        this.size = size;
    }

    public String getTag() {
        return tag;
    }

    public void setTag(String tag) {
        this.tag = tag;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    @Override
    public String toString() {
        return "File{" +
                ", userId=" + userId +
                ", filename='" + filename + '\'' +
                ", filePath='" + filePath + '\'' +
                ", fileType='" + fileType + '\'' +
                ", uploadTime=" + uploadTime +
                ", size=" + size +
                ", tag='" + tag + '\'' +
                ", description='" + description + '\'' +
                '}';
    }
}
