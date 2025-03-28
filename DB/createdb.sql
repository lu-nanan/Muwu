-- 用户表
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    storage_quota BIGINT DEFAULT 10737418240,
    used_storage BIGINT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 文件表
CREATE TABLE files (
    file_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    is_encrypted TINYINT(1) DEFAULT 0,
    encryption_key VARCHAR(255),
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    size BIGINT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 文件版本历史表
CREATE TABLE file_versions (
    version_id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    version_number INT NOT NULL,
    modified_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    checksum VARCHAR(64) NOT NULL,
    description VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 分享链接表
CREATE TABLE share_links (
    link_id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    user_id INT NOT NULL,
    access_password VARCHAR(50),
    expires_at DATETIME,
    max_downloads INT DEFAULT 0,
    permission ENUM('view', 'edit') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 文件标签关联表
CREATE TABLE file_tags (
    file_tag_id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    tag VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- OCR记录表
CREATE TABLE ocr_records (
    ocr_id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    extracted_text TEXT NOT NULL,
    accuracy FLOAT DEFAULT 0.0,
    processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 加密配置表
CREATE TABLE encryption_configs (
    config_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    default_algorithm VARCHAR(20) DEFAULT 'AES-256',
    key_rotation_period INT DEFAULT 90
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 操作日志表
CREATE TABLE activity_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    affected_file_id INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;