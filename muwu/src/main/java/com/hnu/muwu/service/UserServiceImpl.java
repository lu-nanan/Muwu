package com.hnu.muwu.service;

import com.hnu.muwu.bean.UserInfo;
import com.hnu.muwu.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service("userService")
public class UserServiceImpl implements UserService{

    @Autowired
    private UserMapper userMapper;

    @Override
    public List<UserInfo> getAllUsers() {
        return userMapper.getAllUsers();
    }
}
