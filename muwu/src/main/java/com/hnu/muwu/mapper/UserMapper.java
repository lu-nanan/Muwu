package com.hnu.muwu.mapper;

import com.hnu.muwu.DTO.RegisterRequest;
import com.hnu.muwu.bean.UserInfo;

import org.apache.ibatis.annotations.Insert;
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

    @Select({
            "SELECT",
            "COUNT(*)",
            "FROM users",
            "WHERE user_id = #{userId}"
    })
    Integer findUserId(Integer userId);

    @Select({
            "SELECT",
            "COUNT(*)",
            "FROM users",
            "WHERE email = #{email}"
    })
    Integer findEmail(String email);

    @Select({
            "SELECT",
            "COUNT(*)",
            "FROM users",
            "WHERE telephone = #{phone}"
    })
    Integer findPhone(String phone);

    // 新增插入用户的方法
    @Insert({
            "INSERT INTO users (telephone, username, email, password_hash, storage_quota, used_storage)",
            "VALUES (#{telephone}, #{username}, #{email}, #{passwordHash}, #{storageQuota}, #{usedStorage})"
    })
    int insertUser(RegisterRequest registerRequest);

    // 新增根据用户名搜索用户的方法
    @Select({
            "SELECT",
            "user_id, telephone, username, email, password_hash,",
            "storage_quota, used_storage",
            "FROM users",
            "WHERE username = #{username}"
    })
    List<UserInfo> searchUsersByUsername(String username);
}