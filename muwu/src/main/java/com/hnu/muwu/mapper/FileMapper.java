package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.FinalFile;
import com.hnu.muwu.bean.MyFile;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.sql.Timestamp;
import java.util.List;

@Mapper
public interface FileMapper {

    @Insert("INSERT INTO files (user_id, filename, file_path, file_type, upload_time, size, tag, description) VALUES (#{userId}, #{filename}, #{filePath}, #{fileType}, #{uploadTime}, #{size}, #{tag}, #{description})")
    int insertFile(Integer userId, String filename, String filePath, String fileType, Timestamp uploadTime, Long size, String tag, String description);

    @Select("SELECT user_id, filename, file_path, file_type, upload_time, size, tag, description FROM files WHERE user_id = #{userId} AND filename = #{filename}")
    List<FinalFile> getFileByUserIdAndFilename(Integer userId, String filename);
}

