package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.ShareFileEntity;
import org.apache.ibatis.annotations.*;

import java.util.List;




@Mapper
public interface ShareFileMapper {

    /**
     * 插入分享文件记录（linkId为自增主键，无需指定）
     * @param shareFile 分享文件实体对象
     * @return 插入的行数
     */
    @Insert({
            "INSERT INTO share_links (user_id, created_at, share_path, file_name, url, qrcodePath)",
            "VALUES (#{userId}, #{created_at}, #{sharePath}, #{fileName}, #{url}, #{qrcodePath})"
    })
    @Options(useGeneratedKeys = true, keyProperty = "linkId", keyColumn = "link_id")
    int insertShareFile(ShareFileEntity shareFile);

    /**
     * 根据用户ID查询分享文件记录
     * @param userId 用户ID
     * @return 该用户的所有分享文件记录
     */
    @Select("SELECT link_id, user_id, created_at, share_path, file_name, url, qrcodePath " +
            "FROM share_links " +
            "WHERE user_id = #{userId}")
    @Results({
            @Result(property = "userId", column = "user_id"),
            @Result(property = "fileName", column = "file_name"),
            @Result(property = "sharePath", column = "share_path"),
            @Result(property = "linkId", column = "link_id"),
            @Result(property = "created_at", column = "created_at"),
            @Result(property = "url", column = "url"),
            @Result(property = "qrcodePath", column = "qrcodePath"),
    })
    List<ShareFileEntity> getShareFilesByUserId(Integer userId);
}