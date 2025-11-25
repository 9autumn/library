# 青山区图书馆后端服务 (Python FastAPI)

基于 Python FastAPI + MongoDB 的图书馆后端服务，实现游客用户管理系统。

## 📦 技术栈

- **Web框架**: FastAPI 0.104+
- **数据库**: MySQL 5.7+ / MariaDB 10.3+
- **ORM**: SQLAlchemy 2.0 (异步)
- **认证**: JWT (python-jose)
- **密码加密**: Bcrypt (passlib)
- **数据验证**: Pydantic v2

## 🚀 快速开始

### 1. 安装 Python

确保安装 Python 3.9 或更高版本：

```bash
python --version  # 应该 >= 3.9
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

关键配置项：
- `DB_HOST`: MySQL主机地址
- `DB_USER`: 数据库用户名
- `DB_PASSWORD`: 数据库密码
- `DB_NAME`: 数据库名称
- `SECRET_KEY`: JWT密钥（生产环境必须修改）
- `ALLOWED_ORIGINS`: 允许的前端地址

### 5. 创建MySQL数据库

确保MySQL正在运行，然后创建数据库：

```bash
# 方式1：使用初始化脚本
mysql -u root -p < init_mysql.sql

# 方式2：手动创建
mysql -u root -p
CREATE DATABASE ai_library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ai_library;
```

**注意**：项目启动时会自动创建表结构，无需手动创建表

### 6. 启动服务

```bash
# 开发模式（自动重载）
python app/main.py

# 或使用 uvicorn
uvicorn app.main:app --reload --port 8000
```

服务将在 **http://localhost:8000** 启动

### 7. 查看API文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 项目结构

```
ai-library-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   └── visitor.py       # 游客模型
│   ├── schemas/             # API模型
│   │   ├── __init__.py
│   │   └── visitor.py       # 游客请求/响应模型
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   └── visitor_service.py  # 游客服务
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── visitor.py   # 游客路由
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── auth.py          # JWT认证
│       └── security.py      # 密码加密
├── requirements.txt         # 依赖列表
├── .env.example            # 环境变量示例
├── .gitignore              # Git忽略文件
└── README.md               # 本文件
```

## 🔌 API 接口

### 游客用户接口

#### 1. 注册游客
```http
POST /api/v1/visitors/register
Content-Type: application/json

{
  "username": "visitor001",
  "email": "visitor@example.com",
  "password": "password123",
  "name": "张三",
  "phone": "13800138000"
}
```

#### 2. 游客登录
```http
POST /api/v1/visitors/login
Content-Type: application/json

{
  "username": "visitor001",
  "password": "password123"
}
```

#### 3. 获取当前用户信息
```http
GET /api/v1/visitors/me
Authorization: Bearer <access_token>
```

#### 4. 更新用户信息
```http
PUT /api/v1/visitors/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "李四",
  "phone": "13900139000",
  "avatar": "https://example.com/avatar.jpg"
}
```

#### 5. 获取所有游客列表
```http
GET /api/v1/visitors/?skip=0&limit=20&status=active
```

## 🗄️ 数据库

### Visitors 表（游客用户表）

```sql
CREATE TABLE visitors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(20) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  hashed_password VARCHAR(255) NOT NULL,
  name VARCHAR(50),
  phone VARCHAR(11),
  avatar VARCHAR(255),
  last_login_at DATETIME,
  login_count INT DEFAULT 0,
  status ENUM('active', 'inactive', 'banned') DEFAULT 'active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🔒 认证流程

1. 用户注册或登录成功后获得 JWT Token
2. 后续请求在 Header 中携带：`Authorization: Bearer <token>`
3. 服务器验证 Token 有效性并返回用户信息

## 🧪 测试

使用 curl 测试：

```bash
# 注册
curl -X POST http://localhost:8000/api/v1/visitors/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test001","email":"test@example.com","password":"123456"}'

# 登录
curl -X POST http://localhost:8000/api/v1/visitors/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test001","password":"123456"}'

# 获取用户信息（需要替换token）
curl -X GET http://localhost:8000/api/v1/visitors/me \
  -H "Authorization: Bearer <your_token>"
```

## 📝 开发说明

### 添加新的数据模型

1. 在 `app/models/` 创建新模型文件
2. 在 `app/schemas/` 创建对应的请求/响应模型
3. 在 `app/services/` 实现业务逻辑
4. 在 `app/api/v1/` 创建API路由
5. 在 `app/api/v1/__init__.py` 注册路由

### 数据库索引

表创建时已自动添加索引：

```sql
-- 游客表索引
INDEX idx_username (username)
INDEX idx_email (email)
INDEX idx_status (status)
INDEX idx_created_at (created_at)
```

## 🚀 部署

### 使用 Gunicorn + Uvicorn

```bash
pip install gunicorn

gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### 使用 Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📄 许可证

MIT License

---

**最后更新**: 2025-10-11

