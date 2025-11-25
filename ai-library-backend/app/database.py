"""
数据库连接管理
使用 SQLAlchemy 异步引擎连接 MySQL
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


# 定义基类
class Base(DeclarativeBase):
    """数据库模型基类"""
    pass


# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def init_db():
    """初始化数据库（创建所有表）"""
    async with engine.begin() as conn:
        # 导入所有模型以确保它们被注册
        from app.models import visitor  # noqa
        
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
        print("✅ 数据库表创建成功")


async def get_db():
    """
    获取数据库会话
    用于依赖注入
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def connect_to_db():
    """连接到数据库并初始化"""
    try:
        # 测试连接
        async with engine.begin() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        
        print(f"✅ MySQL 连接成功: {settings.DB_HOST}:{settings.DB_PORT}")
        print(f"📊 使用数据库: {settings.DB_NAME}")
        
        # 初始化数据库表
        await init_db()
        
    except Exception as e:
        print(f"❌ MySQL 连接失败: {e}")
        raise


async def close_db_connection():
    """关闭数据库连接"""
    await engine.dispose()
    print("👋 MySQL 连接已关闭")
