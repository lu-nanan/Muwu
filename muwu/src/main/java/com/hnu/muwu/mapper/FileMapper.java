package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.FinalFile;
import com.hnu.muwu.bean.MyFile;
import org.apache.ibatis.annotations.*;

import java.sql.Timestamp;
import java.util.List;

@Mapper
public interface FileMapper {

    @Insert("INSERT INTO files (user_id, filename, file_path, file_type, upload_time, size, tag, description) VALUES (#{userId}, #{filename}, #{filePath}, #{fileType}, #{uploadTime}, #{size}, #{tag}, #{description})")
    int insertFile(Integer userId, String filename, String filePath, String fileType, Timestamp uploadTime, Long size, String tag, String description);

    @Select("SELECT user_id, filename, file_path, file_type, upload_time, size, tag, description FROM files WHERE user_id = #{userId} AND filename = #{filename}")
    @Results({
            @Result(property = "userId", column = "user_id"),
            @Result(property = "filename", column = "filename"),
            @Result(property = "filePath", column = "file_path"),
            @Result(property = "fileType", column = "file_type"),
            @Result(property = "uploadTime", column = "upload_time"),
            @Result(property = "size", column = "size"),
            @Result(property = "tag", column = "tag"),
            @Result(property = "description", column = "description")
    })
    List<FinalFile> getFileByUserIdAndFilename(Integer userId, String filename);

    @Select("SELECT user_id, filename, file_path, file_type, upload_time, size, tag, description FROM files WHERE filename LIKE #{keyword} AND user_id = #{userId}")
    @Results({
            @Result(property = "userId", column = "user_id"),
            @Result(property = "filename", column = "filename"),
            @Result(property = "filePath", column = "file_path"),
            @Result(property = "fileType", column = "file_type"),
            @Result(property = "uploadTime", column = "upload_time"),
            @Result(property = "size", column = "size"),
            @Result(property = "tag", column = "tag"),
            @Result(property = "description", column = "description")
    })
    List<FinalFile> getFileByKeywordAndUserId(String keyword, Integer userId);

    @Select("SELECT user_id, filename, file_path, file_type, upload_time, size, tag, description FROM files WHERE user_id = #{userId}")
    @Results({
            @Result(property = "userId", column = "user_id"),
            @Result(property = "filename", column = "filename"),
            @Result(property = "filePath", column = "file_path"),
            @Result(property = "fileType", column = "file_type"),
            @Result(property = "uploadTime", column = "upload_time"),
            @Result(property = "size", column = "size"),
            @Result(property = "tag", column = "tag"),
            @Result(property = "description", column = "description")
    })
    List<FinalFile> getAllFilesByUserId(Integer userId);
}

