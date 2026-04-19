@echo off
chcp 65001 >nul
echo ============================================
echo   ATG研发端AI助手 Demo 启动程序
echo ============================================
echo.

cd /d %~dp0

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

echo [2/3] 安装依赖...
pip install -r requirements.txt -q

echo [3/3] 启动服务...
echo.
echo ============================================
echo   服务启动后请访问:
echo   前端界面: http://localhost:8501
echo   API文档:  http://localhost:8000/docs
echo ============================================
echo.

start /b python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

timeout /t 3 /nobreak >nul

python -m streamlit run frontend/app.py --server.port 8501

pause
