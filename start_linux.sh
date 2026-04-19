#!/bin/bash

echo "============================================"
echo "  ATG研发端AI助手 Demo 启动程序"
echo "============================================"
echo ""

cd "$(dirname "$0")"

echo "[1/3] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python 3.9+"
    exit 1
fi

echo "[2/3] 安装依赖..."
pip3 install -r requirements.txt -q

echo "[3/3] 启动服务..."
echo ""
echo "============================================"
echo "  服务启动后请访问:"
echo "  前端界面: http://localhost:8501"
echo "  API文档:  http://localhost:8000/docs"
echo "============================================"
echo ""

python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

sleep 3

python3 -m streamlit run frontend/app.py --server.port 8501

kill $UVICORN_PID 2>/dev/null
