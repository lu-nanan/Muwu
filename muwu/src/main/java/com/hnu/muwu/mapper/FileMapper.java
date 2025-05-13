package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.MyFile;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;

import java.sql.Timestamp;

@Mapper
public interface FileMapper {

    @Insert("INSERT INTO files (user_id, filename, file_path, file_type, upload_time, size) VALUES (#{userId}, #{filename}, #{filePath}, #{fileType}, #{uploadTime}, #{size})")
    int insertFile(Integer userId, String filename, String filePath, String fileType, Timestamp uploadTime, Long size);

}

