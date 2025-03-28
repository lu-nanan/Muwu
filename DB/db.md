#### **用户表 (users)**
| 字段名        | 数据类型     | 主键/外键 | 约束条件                   | 说明                         |
| ------------- | ------------ | --------- | -------------------------- | ---------------------------- |
| user_id       | INT          | PK        | AUTO_INCREMENT             | 用户唯一标识                 |
| telephone     | VARCHAR(20)  |           | UNIQUE, NOT NULL           | 用户手机号           |
| username      | VARCHAR(50)  |           | UNIQUE, NOT NULL           | 用户名                       |
| email         | VARCHAR(100) |           | UNIQUE, NOT NULL           | 用户邮箱                     |
| password_hash | VARCHAR(255) |           | NOT NULL                   | 密码哈希值（加密存储）       |
| storage_quota | BIGINT       |           | DEFAULT 10737418240 (10GB) | 用户云存储配额（字节）       |
| used_storage  | BIGINT       |           | DEFAULT 0                  | 已使用存储空间（字节）       |
| created_at    | DATETIME     |           | DEFAULT CURRENT_TIMESTAMP  | 账户创建时间                 |

#### **文件表 (files)**
| 字段名         | 数据类型     | 主键/外键 | 约束条件                  | 说明                         |
| -------------- | ------------ | --------- | ------------------------- | ---------------------------- |
| file_id        | INT          | PK        | AUTO_INCREMENT            | 文件唯一标识                 |
| user_id        | INT          | FK        | NOT NULL                  | 所属用户ID                   |
| filename       | VARCHAR(255) |           | NOT NULL                  | 文件名（含扩展名）           |
| file_path      | VARCHAR(255) |           | NOT NULL                  | 文件在云存储中的路径         |
| file_type      | VARCHAR(50)  |           | NOT NULL                  | 文件类型（如ZIP、PDF、DOCX） |
| is_encrypted   | TINYINT(1)   |           | DEFAULT 0                 | 是否加密（0-否，1-是）       |
| encryption_key | VARCHAR(255) |           |                           | 加密密钥（仅加密文件）       |
| upload_time    | DATETIME     |           | DEFAULT CURRENT_TIMESTAMP | 上传时间                     |
| size           | BIGINT       |           | NOT NULL                  | 文件大小（字节）             |

#### **文件版本历史表 (file_versions)**
| 字段名         | 数据类型     | 主键/外键 | 约束条件                  | 说明                     |
| -------------- | ------------ | --------- | ------------------------- | ------------------------ |
| version_id     | INT          | PK        | AUTO_INCREMENT            | 版本唯一标识             |
| file_id        | INT          | FK        | NOT NULL                  | 关联文件ID               |
| version_number | INT          |           | NOT NULL                  | 版本号（如1.0、2.0）     |
| modified_time  | DATETIME     |           | DEFAULT CURRENT_TIMESTAMP | 版本修改时间             |
| checksum       | VARCHAR(64)  |           | NOT NULL                  | 文件内容校验和（防篡改） |
| description    | VARCHAR(255) |           |                           | 版本描述（如“更新内容”） |

#### **分享链接表 (share_links)**
| 字段名          | 数据类型    | 主键/外键 | 约束条件                  | 说明                  |
| --------------- | ----------- | --------- | ------------------------- | --------------------- |
| link_id         | INT         | PK        | AUTO_INCREMENT            | 链接唯一标识          |
| file_id         | INT         | FK        | NOT NULL                  | 关联文件ID            |
| user_id         | INT         | FK        | NOT NULL                  | 创建者ID              |
| access_password | VARCHAR(50) |           |                           | 访问密码（可选）      |
| expires_at      | DATETIME    |           |                           | 链接过期时间          |
| max_downloads   | INT         |           | DEFAULT 0（不限制）       | 允许下载次数          |
| permission      | VARCHAR(20) |           | ENUM('view', 'edit')      | 访问权限（查看/编辑） |
| created_at      | DATETIME    |           | DEFAULT CURRENT_TIMESTAMP | 链接创建时间          |


#### **文件标签关联表 (file_tags)**
| 字段名      | 数据类型    | 主键/外键 | 约束条件       | 说明         |
| ----------- | ----------- | --------- | -------------- | ------------ |
| file_tag_id | INT         | PK        | AUTO_INCREMENT | 关联唯一标识 |
| file_id     | INT         | FK        | NOT NULL       | 关联文件ID   |
| tag         | VARCHAR(50) | FK        | NOT NULL       | 标签         |

#### **OCR记录表 (ocr_records)**
| 字段名         | 数据类型 | 主键/外键 | 约束条件                  | 说明                      |
| -------------- | -------- | --------- | ------------------------- | ------------------------- |
| ocr_id         | INT      | PK        | AUTO_INCREMENT            | OCR任务唯一标识           |
| file_id        | INT      | FK        | NOT NULL                  | 关联文件ID（图片/扫描件） |
| extracted_text | TEXT     |           | NOT NULL                  | 提取的文本内容            |
| accuracy       | FLOAT    |           | DEFAULT 0.0               | 识别准确率（0-1）         |
| processed_at   | DATETIME |           | DEFAULT CURRENT_TIMESTAMP | 处理时间                  |


#### **加密配置表 (encryption_configs)**
| 字段名              | 数据类型    | 主键/外键 | 约束条件          | 说明               |
| ------------------- | ----------- | --------- | ----------------- | ------------------ |
| config_id           | INT         | PK        | AUTO_INCREMENT    | 配置唯一标识       |
| user_id             | INT         | FK        | NOT NULL          | 用户ID             |
| default_algorithm   | VARCHAR(20) |           | DEFAULT 'AES-256' | 默认加密算法       |
| key_rotation_period | INT         |           | DEFAULT 90        | 密钥轮换周期（天） |

#### **操作日志表 (activity_logs)**
| 字段名           | 数据类型    | 主键/外键 | 约束条件                  | 说明                             |
| ---------------- | ----------- | --------- | ------------------------- | -------------------------------- |
| log_id           | INT         | PK        | AUTO_INCREMENT            | 日志唯一标识                     |
| user_id          | INT         | FK        | NOT NULL                  | 执行用户ID                       |
| action_type      | VARCHAR(50) |           | NOT NULL                  | 操作类型（如“上传文件”、“分享”） |
| affected_file_id | INT         | FK        |                           | 关联文件ID                      |
| timestamp        | DATETIME    |           | DEFAULT CURRENT_TIMESTAMP | 操作时间                         |
| details          | TEXT        |           |                           | 操作详细信息                     |
