package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.ShareFileEntity;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface ShareFileMapper {
    @Insert("INSERT INTO share_links(file_id, user_id, share_path, file_name, " +
            "expires_at, access_password, max_downloads, permission) " +
            "VALUES(#{fileId}, #{userId}, #{sharePath}, #{fileName}, " +
            "#{expiresAt}, #{accessPassword}, #{maxDownloads}, #{permission})")
    @Options(useGeneratedKeys = true, keyProperty = "linkId")
    int insert(ShareFileEntity shareFile);

    @Select("SELECT * FROM share_links WHERE link_id = #{linkId}")
    ShareFileEntity selectById( Integer linkId);

    @Select("SELECT * FROM share_links WHERE user_id = #{userId}")
    List<ShareFileEntity> selectByUserId( Integer userId);

    @Select("SELECT * FROM share_links WHERE expires_at < NOW()")
    List<ShareFileEntity> selectExpiredRecords();

    @Update("UPDATE share_links SET " +
            "expires_at = #{expiresAt}, " +
            "max_downloads = #{maxDownloads}, " +
            "permission = #{permission} " +
            "WHERE link_id = #{linkId}")
    int update(ShareFileEntity shareFile);

    @Delete("DELETE FROM share_links WHERE link_id = #{linkId}")
    int deleteById(@Param("linkId") Integer linkId);
}
