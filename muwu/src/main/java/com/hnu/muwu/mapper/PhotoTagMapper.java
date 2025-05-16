package com.hnu.muwu.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface PhotoTagMapper {
    @Select("SELECT name FROM photo_tag WHERE user_id = #{userId}")
    List<String> getTagsByUserId(Integer userId);

    @Select("SELECT tag FROM photo_tag WHERE user_id = #{userId} AND name = #{name}")
    String getTagByName(Integer userId, String name);
}
