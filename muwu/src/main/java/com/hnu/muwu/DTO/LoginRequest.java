package com.hnu.muwu.DTO;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;


public class LoginRequest {
    private String count;
    private String password;

    public LoginRequest() {}

    public LoginRequest(String count, String password) {
        this.count = count;
        this.password = password;
    }

    public String getCount() {
        return count;
    }

    public void setCount(String count) {
        this.count = count;
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
                "count='" + count + '\'' +
                ", password=' " + password + '\'' +
                '}';
    }
}
