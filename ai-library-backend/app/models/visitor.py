"""
游客用户数据模型 - SQLAlchemy
"""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum


class UserStatus(str, enum.Enum):
    """用户状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


class Visitor(Base):
    """游客用户表"""
    __tablename__ = "visitors"
    
    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    
    # 基本信息
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="邮箱")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment="加密密码")
    
    # 个人资料
    name: Mapped[str] = mapped_column(String(50), nullable=True, comment="真实姓名")
    phone: Mapped[str] = mapped_column(String(11), nullable=True, comment="手机号")
    avatar: Mapped[str] = mapped_column(String(255), nullable=True, comment="头像URL")
    
    # 访问记录
    last_login_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="最后登录时间")
    login_count: Mapped[int] = mapped_column(Integer, default=0, comment="登录次数")
    
    # 账户状态
    status: Mapped[str] = mapped_column(
        SQLEnum(UserStatus),
        default=UserStatus.ACTIVE,
        nullable=False,
        comment="账户状态"
    )
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="更新时间"
    )
    
    def __repr__(self):
        return f"<Visitor(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile": {
                "name": self.name,
                "phone": self.phone,
                "avatar": self.avatar
            },
            "status": self.status,
            "login_count": self.login_count,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
