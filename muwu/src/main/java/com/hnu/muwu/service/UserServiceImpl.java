package com.hnu.muwu.service;

import com.hnu.muwu.DTO.RegisterRequest;
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
        if (userMapper.findPhone(count) == 0) {
            return -1;
        }
        return userMapper.getUserIdByPhone(count);
    }

    @Override
    public int getUserIdByEmail(String count){
        if (userMapper.findEmail(count) == 0) {
            return -1;
        }
        return userMapper.getUserIdByEmail(count);
    }

    @Override
    public boolean checkCredentialsWithUserId(int count, String password) {
        String passwordHash = userMapper.getPasswordHashByUserId(count);
        String[] s = passwordHash.split(":");
        System.out.println(s[0]);
        System.out.println(s[1]);
        try{
            System.out.println(HashCodeHelper.verifyPassword(password, s[0], s[1]));
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

    @Override
    public int insertUser(RegisterRequest registerRequest){
        return userMapper.insertUser(registerRequest);
    }
}
