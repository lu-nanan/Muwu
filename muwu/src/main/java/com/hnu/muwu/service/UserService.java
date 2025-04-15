package com.hnu.muwu.service;

import com.hnu.muwu.bean.UserInfo;

import java.util.List;


public interface UserService {

    List<UserInfo> getAllUsers();

    boolean checkCredentialsWithUserId(int count, String password);

    int getUserIdByPhone(String count);

    int getUserIdByEmail(String count);

    boolean checkUserAccount(String count);
}