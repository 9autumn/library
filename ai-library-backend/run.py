"""
运行脚本
解决模块导入问题
"""

import sys
from pathlib import Path

# 将项目根目录添加到Python路径
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )

