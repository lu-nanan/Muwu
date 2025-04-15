package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.UserInfo;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface UserMapper {
    @Select({
            "SELECT",
            "user_id AS userId,",
            "telephone,",
            "username,",
            "email,",
            "password_hash AS passwordHash,",
            "storage_quota AS storageQuota,",
            "used_storage AS usedStorage,",
            "created_at AS createTime",
            "FROM users"
    })
    List<UserInfo> getAllUsers();

    @Select({
            "SELECT",
            "password_hash",
            "FROM users",
            "WHERE user_id = #{userId}"
    })
    String getPasswordHashByUserId(Integer userId);


    @Select({
            "SELECT COALESCE((SELECT user_id FROM users WHERE telephone = #{phone}), -1)"
    })
    Integer getUserIdByPhone(String phone);

    @Select({
            "SELECT COALESCE((SELECT user_id FROM users WHERE email = #{email}), -1)"
    })
    Integer getUserIdByEmail(String email);

    @Select({
            "SELECT",
            "COUNT(*)",
            "FROM users",
            "WHERE user_id = #{userId}"
    })
    Integer findUserId(Integer userId);
}