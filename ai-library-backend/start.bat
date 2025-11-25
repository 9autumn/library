@echo off
echo 启动青山区图书馆后端服务...
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate

REM 安装依赖
echo 安装依赖包...
pip install -r requirements.txt

REM 启动服务
echo.
echo 启动服务器...
echo API文档: http://localhost:8000/docs
echo.
python run.py

