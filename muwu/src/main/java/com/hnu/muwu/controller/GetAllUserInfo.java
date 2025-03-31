package com.hnu.muwu.controller;


import com.hnu.muwu.bean.UserInfo;
import com.hnu.muwu.service.UserService;
import jakarta.annotation.Resource;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/getAllUserInfo" )
public class GetAllUserInfo {

    @Resource
    private UserService userService;

    @RequestMapping(value = "/getAllUserInfo", method = RequestMethod.GET, produces = "application/json;charset=UTF-8")
    public List<UserInfo> getAllUserInfo() {
        return userService.getAllUsers();
    }
}