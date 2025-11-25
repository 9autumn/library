"""
应用配置
使用 pydantic-settings 管理环境变量
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets


class Settings(BaseSettings):
    """应用配置类"""
    
    # ==================== 应用信息 ====================
    APP_NAME: str = "青山区图书馆后端服务"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "基于FastAPI的图书馆智能服务系统"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development/staging/production
    
    # ==================== 服务器配置 ====================
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1  # Uvicorn worker数量
    RELOAD: bool = True  # 自动重载（仅开发环境）
    
    # ==================== 数据库配置 ====================
    # MySQL配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "ai_library"
    DB_CHARSET: str = "utf8mb4"
    
    # 数据库连接池配置
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    DB_ECHO: bool = False  # 是否打印SQL语句
    
    @property
    def DATABASE_URL(self) -> str:
        """构建数据库连接URL"""
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"
    
    # ==================== JWT认证配置 ====================
    SECRET_KEY: str = secrets.token_urlsafe(32)  # 自动生成随机密钥
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7天 = 7*24*60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # 刷新令牌30天
    
    # ==================== CORS配置 ====================
    # 使用逗号分隔的字符串，程序会自动转换为列表
    CORS_ORIGINS: str = "http://localhost:5199,http://127.0.0.1:5199,http://localhost:5173,http://127.0.0.1:5173"
    ALLOW_CREDENTIALS: bool = True
    
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """获取允许的源列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def ALLOWED_METHODS(self) -> List[str]:
        """获取允许的方法列表"""
        return ["*"]
    
    @property
    def ALLOWED_HEADERS(self) -> List[str]:
        """获取允许的请求头列表"""
        return ["*"]
    
    # ==================== API文档配置 ====================
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"
    API_V1_PREFIX: str = "/api/v1"
    
    # ==================== 安全配置 ====================
    # 密码强度要求
    PASSWORD_MIN_LENGTH: int = 6
    PASSWORD_MAX_LENGTH: int = 128
    
    # 用户名要求
    USERNAME_MIN_LENGTH: int = 3
    USERNAME_MAX_LENGTH: int = 20
    
    # 速率限制
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_TIMES: int = 100  # 每个时间窗口内的最大请求数
    RATE_LIMIT_SECONDS: int = 60  # 时间窗口（秒）
    
    # ==================== 文件上传配置 ====================
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_EXTENSIONS: str = ".jpg,.jpeg,.png,.gif,.pdf"
    
    @property
    def ALLOWED_UPLOAD_EXTENSIONS(self) -> List[str]:
        """获取允许的上传扩展名列表"""
        return [ext.strip() for ext in self.UPLOAD_EXTENSIONS.split(",")]
    
    # ==================== 日志配置 ====================
    LOG_LEVEL: str = "INFO"  # DEBUG/INFO/WARNING/ERROR/CRITICAL
    LOG_DIR: str = "logs"
    LOG_FILE: str = "app.log"
    LOG_ROTATION: str = "500 MB"  # 日志轮转大小
    LOG_RETENTION: str = "10 days"  # 日志保留时间
    
    # ==================== 邮件配置（可选） ====================
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    SMTP_FROM_NAME: Optional[str] = "青山区图书馆"
    
    # ==================== Redis配置（可选） ====================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_ENABLED: bool = False
    
    # ==================== Dify API配置 ====================
    DIFY_API_URL: str = "http://124.71.97.68/v1"
    DIFY_API_KEY: str = "app-ka994zy9N68cJgaEznXHqbfL"
    DIFY_TIMEOUT: int = 30  # 请求超时时间（秒）
    
    # ==================== 分页配置 ====================
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # ==================== 其他配置 ====================
    TIMEZONE: str = "Asia/Shanghai"
    LANGUAGE: str = "zh-CN"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()


# 配置验证函数
def validate_settings():
    """验证配置的有效性"""
    errors = []
    
    # 检查生产环境的关键配置
    if settings.ENVIRONMENT == "production":
        if settings.DEBUG:
            errors.append("⚠️  生产环境不应开启DEBUG模式")
        
        if settings.SECRET_KEY == "your-secret-key-change-this-in-production":
            errors.append("❌ 生产环境必须设置自定义SECRET_KEY")
        
        if settings.RELOAD:
            errors.append("⚠️  生产环境不应开启自动重载")
    
    # 检查数据库配置
    if not settings.DB_HOST:
        errors.append("❌ 必须配置DB_HOST")
    if not settings.DB_NAME:
        errors.append("❌ 必须配置DB_NAME")
    
    if errors:
        print("\n" + "="*60)
        print("⚠️  配置验证发现以下问题:")
        for error in errors:
            print(f"  {error}")
        print("="*60 + "\n")
    
    return len(errors) == 0

