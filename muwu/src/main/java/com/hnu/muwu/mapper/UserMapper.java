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

    @Select({
            "SELECT",
            "password_hash",
            "FROM users",
            "WHERE user_id = #{userId}"
    })
    String getPasswordHashByUserId(int userId);


    @Select({
            "SELECT",
            "user_id",
            "FROM users",
            "WHERE telephone = #{phone}"
    })
    int getUserIdByPhone(String phone);

    @Select({
            "SELECT",
            "user_id",
            "FROM users",
            "WHERE email = #{email}"
    })
    int getUserIdByEmail(String email);
}