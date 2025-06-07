package com.hnu.muwu.service;

import com.hnu.muwu.bean.ShareFileEntity;

import java.util.List;


public interface ShareFileService {

//    /**
//     * 创建文件分享链接
//     * @param filePath 原始文件路径（相对路径）
//     * @param userId 用户ID
//     * @param expireDays 有效期天数
//     * @return 分享记录实体（包含linkId和访问信息）
//     */
//    ShareFileEntity createShare(String filePath, Integer userId, Integer expireDays);
//
//    /**
//     * 获取有效的分享记录
//     * @param linkId 分享链接ID
//     * @return 未过期的分享记录
//     * @throws RuntimeException 分享不存在或已过期
//     */
//    ShareFileEntity getValidShare(Integer linkId);
//
//    /**
//     * 获取用户所有分享记录
//     * @param userId 用户ID
//     * @param includeExpired 是否包含已过期记录
//     * @return 分享记录列表
//     */
//    List<ShareFileEntity> getUserShares(Integer userId, boolean includeExpired);
//
//    /**
//     * 提前失效分享链接
//     * @param linkId 分享链接ID
//     * @param userId 操作者ID（用于权限验证）
//     */
//    void invalidateShare(Integer linkId, Integer userId);
//
//    /**
//     * 处理文件下载（包含下载计数等逻辑）
//     * @param linkId 分享链接ID
//     * @return 文件物理路径
//     */
//    String processDownload(Integer linkId);
//
//    /**
//     * 清理过期分享记录
//     * @return 清理的记录数量
//     */
//    int cleanExpiredShares();
//
//    // ---------- 扩展方法 ----------
//    /**
//     * 查询分享记录（管理用）
//     * @param fileId 关联文件ID
//     * @param activeOnly 仅查询有效记录
//     * @param startTime 开始时间
//     * @param endTime 结束时间
//     */
//    List<ShareFileEntity> searchShares(
//            Integer fileId,
//            boolean activeOnly,
//            LocalDateTime startTime,
//            LocalDateTime endTime
//    );
    /**
     * 保存分享记录
     */
    int saveShare(ShareFileEntity share);
    List<ShareFileEntity> getShareFilesByUserId(Integer userId);
}
