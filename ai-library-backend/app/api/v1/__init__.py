# API v1路由
from fastapi import APIRouter
from app.api.v1 import visitor

api_router = APIRouter()
api_router.include_router(visitor.router, prefix="/visitors", tags=["游客用户"])

