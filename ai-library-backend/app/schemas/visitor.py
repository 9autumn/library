"""
游客用户的请求和响应模型
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class VisitorBase(BaseModel):
    """游客基础模型"""
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    email: EmailStr = Field(..., description="邮箱")


class VisitorRegister(VisitorBase):
    """游客注册请求"""
    password: str = Field(..., min_length=6, description="密码，至少6个字符")
    name: Optional[str] = Field(None, description="真实姓名")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号")


class VisitorLogin(BaseModel):
    """游客登录请求"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


class VisitorUpdate(BaseModel):
    """游客信息更新"""
    name: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$")
    avatar: Optional[str] = None


class VisitorProfile(BaseModel):
    """游客个人资料"""
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None


class VisitorResponse(BaseModel):
    """游客信息响应"""
    id: str = Field(..., description="用户ID")
    username: str
    email: str
    profile: VisitorProfile
    status: str
    login_count: int
    last_login_at: Optional[datetime] = None
    created_at: datetime


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class VisitorLoginResponse(BaseModel):
    """登录响应"""
    user: VisitorResponse
    token: TokenResponse


class ResponseModel(BaseModel):
    """通用响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[dict] = Field(None, description="响应数据")

