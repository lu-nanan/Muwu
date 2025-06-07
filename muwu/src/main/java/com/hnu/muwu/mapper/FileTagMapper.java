package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.FileTag;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface FileTagMapper {
    @Select("SELECT tag FROM file_tag WHERE user_id = #{userId}")
    List<String> getTagsByUserId(Integer userId);
    /**
     * 插入文件标签记录
     * @param fileTag 文件标签实体对象
     * @return 插入的行数
     */
    @Insert({
            "INSERT INTO file_tag (user_id, tag)",
            "VALUES (#{userId}, #{tag})"
    })
    @Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    int insertFileTag(FileTag fileTag);
    /**
     * 更新文件标签（根据用户ID和旧标签值更新为新标签值）
     * @param userId 用户ID
     * @param oldTag 旧标签值
     * @param newTag 新标签值
     * @return 更新的行数
     */
    @Update({
            "UPDATE file_tag",
            "SET tag = #{newTag}",
            "WHERE user_id = #{userId} AND tag = #{oldTag}"
    })
    int updateFileTag(@Param("userId") String userId,
                      @Param("oldTag") String oldTag,
                      @Param("newTag") String newTag);
    /**
     * 根据用户ID和标签删除文件标签记录
     * @param userId 用户ID
     * @param tag 标签值
     * @return 删除的行数
     */
    @Delete({
            "DELETE FROM file_tag",
            "WHERE user_id = #{userId} AND tag = #{tag}"
    })
    int deleteFileTagByUserIdAndTag(@Param("userId") String userId,
                                    @Param("tag") String tag);
}
