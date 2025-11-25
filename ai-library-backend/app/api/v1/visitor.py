"""
游客用户API路由
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.visitor_service import VisitorService
from app.database import get_db
from app.schemas.visitor import (
    VisitorRegister,
    VisitorLogin,
    VisitorResponse,
    VisitorUpdate,
    TokenResponse,
    ResponseModel
)
from app.utils.auth import decode_access_token

router = APIRouter()
security = HTTPBearer()


async def get_current_visitor(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """获取当前登录的游客"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌"
        )
    
    visitor_id = payload.get("sub")
    visitor_type = payload.get("type")
    
    if visitor_type != "visitor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    try:
        visitor_id = int(visitor_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的用户ID"
        )
    
    visitor = await VisitorService.get_visitor_by_id(db, visitor_id)
    if not visitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return visitor


@router.post("/register", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def register_visitor(
    visitor_data: VisitorRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    游客注册
    
    - **username**: 用户名（3-20个字符）
    - **email**: 邮箱地址
    - **password**: 密码（至少6个字符）
    - **name**: 真实姓名（可选）
    - **phone**: 手机号（可选）
    """
    try:
        visitor = await VisitorService.create_visitor(db, visitor_data)
        token = VisitorService.create_token(visitor["id"])
        
        return {
            "success": True,
            "message": "注册成功",
            "data": {
                "user": visitor,
                "token": {
                    "access_token": token,
                    "token_type": "bearer"
                }
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册失败，请稍后重试"
        )


@router.post("/login", response_model=ResponseModel)
async def login_visitor(
    login_data: VisitorLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    游客登录
    
    - **username**: 用户名或邮箱
    - **password**: 密码
    """
    try:
        visitor = await VisitorService.authenticate_visitor(
            db,
            login_data.username,
            login_data.password
        )
        
        if not visitor:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        token = VisitorService.create_token(visitor["id"])
        
        return {
            "success": True,
            "message": "登录成功",
            "data": {
                "user": visitor,
                "token": {
                    "access_token": token,
                    "token_type": "bearer"
                }
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录失败，请稍后重试"
        )


@router.get("/me", response_model=ResponseModel)
async def get_current_visitor_info(
    current_visitor: dict = Depends(get_current_visitor)
):
    """
    获取当前登录游客的信息
    
    需要在请求头中携带 Bearer Token
    """
    return {
        "success": True,
        "message": "获取成功",
        "data": {"user": current_visitor}
    }


@router.put("/me", response_model=ResponseModel)
async def update_current_visitor_info(
    update_data: VisitorUpdate,
    current_visitor: dict = Depends(get_current_visitor),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前游客的个人信息
    
    - **name**: 真实姓名
    - **phone**: 手机号
    - **avatar**: 头像URL
    """
    try:
        updated_visitor = await VisitorService.update_visitor(
            db,
            current_visitor["id"],
            update_data
        )
        
        if not updated_visitor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return {
            "success": True,
            "message": "更新成功",
            "data": {"user": updated_visitor}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新失败"
        )


@router.get("/", response_model=ResponseModel)
async def get_all_visitors(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有游客列表（分页）
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数（最大100）
    - **status**: 过滤状态（active/inactive/banned）
    """
    if limit > 100:
        limit = 100
    
    try:
        result = await VisitorService.get_all_visitors(db, skip, limit, status)
        
        return {
            "success": True,
            "message": "获取成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取列表失败"
        )

