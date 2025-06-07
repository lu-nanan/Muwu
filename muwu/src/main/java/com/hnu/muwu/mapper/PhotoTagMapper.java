package com.hnu.muwu.mapper;

import com.hnu.muwu.bean.PhotoTag;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface    PhotoTagMapper {
    @Select("SELECT name FROM photo_tag WHERE user_id = #{userId}")
    List<String> getTagsByUserId(Integer userId);

    @Select("SELECT tag FROM photo_tag WHERE user_id = #{userId} AND name = #{name}")
    String getTagByName(Integer userId, String name);
    /**
     * 插入文件标签记录
     * @param photoTag 文件标签实体对象
     * @return 插入的行数
     */
    @Insert({
            "INSERT INTO photo_tag (user_id, tag,name)",
            "VALUES (#{userId}, #{tag},#{name})"
    })
    @Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    int insertPhotoTag(PhotoTag photoTag);
    @Update({
            "UPDATE photo_tag",
            "SET tag = #{newTag},name = #{newName}",
            "WHERE user_id = #{userId} AND tag = #{oldTag}"
    })
    int updateFileTag(@Param("userId") String userId,
                      @Param("oldTag") String oldTag,
                      @Param("newTag") String newTag,
                      @Param("newName") String newName);
    /**
     * 根据用户ID和标签删除文件标签记录
     * @param userId 用户ID
     * @param tag 标签值
     * @return 删除的行数
     */
    @Delete({
            "DELETE FROM photo_tag",
            "WHERE user_id = #{userId} AND tag = #{tag}"
    })
    int deleteFileTagByUserIdAndTag(@Param("userId") String userId,
                                    @Param("tag") String tag);
    @Select("SELECT tag FROM photo_tag WHERE user_id = #{userId}")
    List<String> getTagByUserId(Integer userId);
}
