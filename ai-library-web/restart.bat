@echo off
echo 正在重启开发服务器...
taskkill /f /im node.exe 2>nul
timeout /t 2 /nobreak >nul
echo 启动开发服务器...
npm run dev
pause
