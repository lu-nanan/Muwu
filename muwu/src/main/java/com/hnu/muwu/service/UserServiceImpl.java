package com.hnu.muwu.service;

import com.hnu.muwu.bean.UserInfo;
import com.hnu.muwu.mapper.UserMapper;
import com.hnu.muwu.utiles.HashCodeHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.security.NoSuchAlgorithmException;
import java.util.List;

@Service("userService")
public class UserServiceImpl implements UserService{

    @Autowired
    private UserMapper userMapper;

    @Override
    public List<UserInfo> getAllUsers() {
        return userMapper.getAllUsers();
    }

    @Override
    public int getUserIdByPhone(String count){
        return userMapper.getUserIdByPhone(count);
    }

    @Override
    public int getUserIdByEmail(String count){
        return userMapper.getUserIdByEmail(count);
    }

    @Override
    public boolean checkCredentialsWithUserId(int count, String password) {
        String passwordHash = userMapper.getPasswordHashByUserId(count);
        String[] s = passwordHash.split(":");
        try{
            return HashCodeHelper.verifyPassword(password, s[0], s[1]);
        } catch (NoSuchAlgorithmException e) {
            System.err.println("Algorithm not available: " + e.getMessage());
            return false;
        }
    }

    @Override
    public boolean checkUserAccount(String count) {
        Integer c = userMapper.findUserId(Integer.parseInt(count));
        return c != 0;
    }


}
