package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.UserInfo;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface UserMapper {
    @Select({
            "SELECT",
            "user_id, telephone, username, email, password_hash,",
            "storage_quota, used_storage",
            "FROM users"
    })
    List<UserInfo> getAllUsers();
}