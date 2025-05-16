package com.hnu.muwu.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface FileTagMapper {
    @Select("SELECT tag FROM file_tag WHERE user_id = #{userId}")
    List<String> getTagsByUserId(Integer userId);
}
