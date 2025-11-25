"""
游客用户服务 - SQLAlchemy版本
处理游客相关的业务逻辑
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.visitor import Visitor, UserStatus
from app.schemas.visitor import VisitorRegister, VisitorUpdate
from app.utils.security import get_password_hash, verify_password
from app.utils.auth import create_access_token


class VisitorService:
    """游客用户服务类"""
    
    @staticmethod
    async def create_visitor(db: AsyncSession, visitor_data: VisitorRegister) -> Dict[str, Any]:
        """
        创建新游客
        
        Args:
            db: 数据库会话
            visitor_data: 游客注册数据
            
        Returns:
            创建的游客信息
            
        Raises:
            ValueError: 用户名或邮箱已存在
        """
        # 检查用户名或邮箱是否已存在
        stmt = select(Visitor).where(
            or_(
                Visitor.username == visitor_data.username,
                Visitor.email == visitor_data.email
            )
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            raise ValueError("用户名或邮箱已被注册")
        
        # 创建游客对象
        visitor = Visitor(
            username=visitor_data.username,
            email=visitor_data.email,
            hashed_password=get_password_hash(visitor_data.password),
            name=visitor_data.name,
            phone=visitor_data.phone,
            status=UserStatus.ACTIVE
        )
        
        db.add(visitor)
        await db.commit()
        await db.refresh(visitor)
        
        return visitor.to_dict()
    
    @staticmethod
    async def authenticate_visitor(db: AsyncSession, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        验证游客身份
        
        Args:
            db: 数据库会话
            username: 用户名或邮箱
            password: 密码
            
        Returns:
            游客信息，如果验证失败返回None
        """
        # 查找游客
        stmt = select(Visitor).where(
            or_(
                Visitor.username == username,
                Visitor.email == username
            )
        )
        result = await db.execute(stmt)
        visitor = result.scalar_one_or_none()
        
        if not visitor:
            return None
        
        # 验证密码
        if not verify_password(password, visitor.hashed_password):
            return None
        
        # 检查账户状态
        if visitor.status != UserStatus.ACTIVE:
            raise ValueError("账户已被禁用")
        
        # 更新登录信息
        visitor.last_login_at = datetime.utcnow()
        visitor.login_count += 1
        
        await db.commit()
        await db.refresh(visitor)
        
        return visitor.to_dict()
    
    @staticmethod
    async def get_visitor_by_id(db: AsyncSession, visitor_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取游客信息
        
        Args:
            db: 数据库会话
            visitor_id: 游客ID
            
        Returns:
            游客信息，如果不存在返回None
        """
        stmt = select(Visitor).where(Visitor.id == visitor_id)
        result = await db.execute(stmt)
        visitor = result.scalar_one_or_none()
        
        if visitor:
            return visitor.to_dict()
        return None
    
    @staticmethod
    async def update_visitor(
        db: AsyncSession,
        visitor_id: int,
        update_data: VisitorUpdate
    ) -> Optional[Dict[str, Any]]:
        """
        更新游客信息
        
        Args:
            db: 数据库会话
            visitor_id: 游客ID
            update_data: 更新数据
            
        Returns:
            更新后的游客信息
        """
        stmt = select(Visitor).where(Visitor.id == visitor_id)
        result = await db.execute(stmt)
        visitor = result.scalar_one_or_none()
        
        if not visitor:
            return None
        
        # 更新字段
        if update_data.name is not None:
            visitor.name = update_data.name
        if update_data.phone is not None:
            visitor.phone = update_data.phone
        if update_data.avatar is not None:
            visitor.avatar = update_data.avatar
        
        visitor.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(visitor)
        
        return visitor.to_dict()
    
    @staticmethod
    async def get_all_visitors(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取所有游客列表（分页）
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的记录数
            status: 过滤状态
            
        Returns:
            游客列表和总数
        """
        # 构建查询
        stmt = select(Visitor)
        
        if status:
            stmt = stmt.where(Visitor.status == status)
        
        # 获取总数
        count_stmt = select(func.count()).select_from(Visitor)
        if status:
            count_stmt = count_stmt.where(Visitor.status == status)
        
        count_result = await db.execute(count_stmt)
        total = count_result.scalar()
        
        # 获取游客列表
        stmt = stmt.order_by(Visitor.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        visitors = result.scalars().all()
        
        return {
            "visitors": [v.to_dict() for v in visitors],
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
    @staticmethod
    def create_token(visitor_id: int) -> str:
        """
        为游客创建访问令牌
        
        Args:
            visitor_id: 游客ID
            
        Returns:
            JWT令牌
        """
        token_data = {
            "sub": str(visitor_id),
            "type": "visitor"
        }
        return create_access_token(token_data)
