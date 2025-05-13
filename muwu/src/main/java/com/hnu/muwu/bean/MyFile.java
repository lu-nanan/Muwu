package com.hnu.muwu.bean;

import java.sql.Timestamp;

public class MyFile {

    // Getters and Setters
    private int userId;
    private String filename;
    private String filePath;
    private String fileType;
    private Timestamp uploadTime;
    private long size;

    public MyFile() {}

    public MyFile(int userId, String filename, String filePath, String fileType, Timestamp uploadTime, long size) {
        this.userId = userId;
        this.filename = filename;
        this.filePath = filePath;
        this.fileType = fileType;
        this.uploadTime = uploadTime;
        this.size = size;
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

    @Override
    public String toString() {
        return "File{" +
                ", userId=" + userId +
                ", filename='" + filename + '\'' +
                ", filePath='" + filePath + '\'' +
                ", fileType='" + fileType + '\'' +
                ", uploadTime=" + uploadTime +
                ", size=" + size +
                '}';
    }
}