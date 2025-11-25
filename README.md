# 🏛️ 青山区图书馆 AI 智能服务系统

一个基于 Vue 3 + Node.js + MongoDB + Dify AI 的现代化图书馆智能服务系统。

## 📋 项目概述

本项目为青山区图书馆开发的智能服务系统，提供 AI 对话、智能推荐、常见问题解答等功能，提升图书馆的服务质量和用户体验。

## 🎯 核心功能

### 前端功能
- ✅ AI 智能对话（基于 Dify 平台）
- ✅ 流式响应，实时显示 AI 回复
- ✅ 支持 Markdown 格式显示
- ✅ 响应式设计，支持桌面和移动端
- ✅ 中英文切换
- ✅ 常见问题快速选择
- ✅ 图书推荐功能
- ✅ 活动推荐展示

### 后端功能
- ✅ RESTful API 设计
- ✅ JWT 身份认证
- ✅ 用户管理系统
- ✅ 聊天会话管理
- ✅ FAQ 管理系统
- ✅ 数据统计分析
- ✅ 日志记录和错误处理

## 🛠️ 技术栈

### 前端技术
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **路由**: Vue Router
- **样式**: CSS3 + 响应式设计
- **Markdown 渲染**: marked

### 后端技术
- **运行时**: Node.js 18+
- **框架**: Express.js
- **数据库**: MongoDB + Mongoose
- **认证**: JWT (jsonwebtoken)
- **日志**: Winston
- **安全**: Helmet, CORS, Rate Limiting

### AI 平台
- **平台**: Dify
- **功能**: 自然语言处理、智能对话、知识库管理

## 📁 项目结构

```
AI_Library/
├── ai-library-backend/       # 后端服务
│   ├── src/
│   │   ├── app.js           # 应用入口
│   │   ├── config/          # 配置文件
│   │   ├── middleware/      # 中间件
│   │   ├── models/          # 数据模型
│   │   └── routes/          # 路由
│   ├── scripts/             # 脚本文件
│   └── package.json         # 依赖配置
│
├── ai-library-web/          # 前端项目
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── pages/           # 页面
│   │   ├── router/          # 路由配置
│   │   ├── services/        # 服务
│   │   ├── styles/          # 样式
│   │   └── utils/           # 工具函数
│   ├── public/              # 静态资源
│   └── package.json         # 依赖配置
│
├── .gitignore               # Git 忽略文件
├── INTEGRATION_GUIDE.md     # 集成指南
└── README.md                # 项目说明
```

## 🚀 快速开始

### 环境要求

- Node.js 18+
- MongoDB 4.4+
- Dify 平台（可选，用于 AI 功能）

### 1. 克隆项目

```bash
git clone <repository-url>
cd AI_Library
```

### 2. 启动后端服务

```bash
cd ai-library-backend

# 安装依赖
npm install

# 配置环境变量（复制 .env.example 为 .env 并修改）
# 需要配置：
# - PORT=3000
# - MONGODB_URI=mongodb://localhost:27017/ai-library
# - JWT_SECRET=your-secret-key
# - DIFY_API_URL=http://127.0.0.1:8089
# - DIFY_API_KEY=your-dify-api-key

# 初始化数据库（可选）
npm run init-db

# 启动开发服务器
npm run dev
```

后端服务将在 http://localhost:3000 启动

### 3. 启动前端服务

```bash
cd ai-library-web

# 安装依赖
npm install

# 配置环境变量（可选）
# 创建 .env 文件配置 Dify API 和后端 API

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动

### 4. 访问系统

打开浏览器访问: http://localhost:5173

## 📖 API 文档

详细的 API 文档请参考 [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)

### 主要接口

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/chat/sessions` - 获取聊天会话列表
- `POST /api/chat/sessions` - 创建新会话
- `GET /api/faq` - 获取常见问题列表
- `GET /api/recommendations` - 获取推荐列表

## 🔧 配置说明

### 后端环境变量

```env
# 服务器配置
PORT=3000
NODE_ENV=development

# 数据库配置
MONGODB_URI=mongodb://localhost:27017/ai-library

# JWT 配置
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=7d

# Dify API 配置
DIFY_API_URL=http://127.0.0.1:8089
DIFY_API_KEY=your-dify-app-key

# 前端地址
FRONTEND_URL=http://localhost:5173
```

### 前端环境变量

```env
# Dify API 配置
VITE_DIFY_BASE_PATH=/dify
VITE_DIFY_TARGET=http://127.0.0.1:8089
VITE_DIFY_APP_KEY=your-dify-app-key

# 后端 API 配置
VITE_API_BASE_URL=http://localhost:3000/api
```

## 📦 部署

### 前端部署

```bash
cd ai-library-web
npm run build
# 将 dist 目录部署到 Web 服务器（如 Nginx）
```

### 后端部署

```bash
cd ai-library-backend
npm install --production
# 使用 PM2 管理进程
pm2 start src/app.js --name "ai-library-backend"
```

## 🧪 测试

```bash
# 后端测试
cd ai-library-backend
npm test

# 前端测试（如果有）
cd ai-library-web
npm test
```

## 📝 开发指南

### 代码规范

- 使用 ESLint 进行代码检查
- 遵循 Vue 3 组合式 API 规范
- 使用 TypeScript 类型注解
- 保持代码简洁和可读性

### Git 提交规范

```
feat: 新功能
fix: 修复问题
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 联系方式

- 项目负责人：青山区图书馆
- Email: [待补充]
- 官网: [待补充]

---

**最后更新**: 2025-10-11

