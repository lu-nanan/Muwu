package com.hnu.muwu.DTO;


public class LoginRequest {
    private String account;
    private String password;

    public LoginRequest() {}

    public LoginRequest(String count, String password) {
        this.account = count;
        this.password = password;
    }

    public String getAccount() {
        return account;
    }

    public void setAccount(String account) {
        this.account = account;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public String toString() {
        return "LoginRequest{" +
                "count='" + account + '\'' +
                ", password=' " + password + '\'' +
                '}';
    }
}
