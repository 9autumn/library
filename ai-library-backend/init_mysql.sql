-- 青山区图书馆数据库初始化脚本
-- 使用前请先在MySQL中创建数据库

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS ai_library 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE ai_library;

-- 游客用户表
CREATE TABLE IF NOT EXISTS visitors (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
  username VARCHAR(20) NOT NULL UNIQUE COMMENT '用户名',
  email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
  hashed_password VARCHAR(255) NOT NULL COMMENT '加密密码',
  
  -- 个人资料
  name VARCHAR(50) DEFAULT NULL COMMENT '真实姓名',
  phone VARCHAR(11) DEFAULT NULL COMMENT '手机号',
  avatar VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
  
  -- 访问记录
  last_login_at DATETIME DEFAULT NULL COMMENT '最后登录时间',
  login_count INT DEFAULT 0 COMMENT '登录次数',
  
  -- 账户状态
  status ENUM('active', 'inactive', 'banned') NOT NULL DEFAULT 'active' COMMENT '账户状态',
  
  -- 时间戳
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  -- 索引
  INDEX idx_username (username),
  INDEX idx_email (email),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='游客用户表';

-- 插入测试数据（可选）
-- INSERT INTO visitors (username, email, hashed_password, name, status) VALUES
-- ('test_user', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqQl0qx4BG', '测试用户', 'active');
-- 密码: test123456

-- 显示表结构
DESCRIBE visitors;

-- 完成提示
SELECT '数据库初始化完成！' AS message;

