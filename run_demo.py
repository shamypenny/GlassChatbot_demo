import subprocess
import sys
import os
import time
import threading

def check_dependencies():
    print("检查依赖...")
    try:
        import streamlit
        import fastapi
        import chromadb
        print("✓ 核心依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("正在安装依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def init_knowledge_base():
    print("\n初始化知识库...")
    os.makedirs("./data/chroma_db", exist_ok=True)
    
    from backend.services.rag_service import RAGService
    rag = RAGService()
    rag.init_knowledge_base()
    print("✓ 知识库初始化完成")

def run_backend():
    print("\n启动后端服务 (端口 8000)...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ])

def run_frontend():
    print("\n启动前端服务 (端口 8501)...")
    subprocess.run([
        sys.executable, "-m", "streamlit", 
        "run", "frontend/app.py",
        "--server.port", "8501",
        "--server.headless", "true"
    ])

def main():
    print("=" * 60)
    print("  ATG研发端AI助手 Demo 启动程序")
    print("=" * 60)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if not check_dependencies():
        print("依赖安装失败，请手动执行: pip install -r requirements.txt")
        return
    
    init_knowledge_base()
    
    print("\n" + "=" * 60)
    print("  服务启动中...")
    print("=" * 60)
    
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    time.sleep(3)
    
    print("\n" + "=" * 60)
    print("  ✓ 后端服务: http://localhost:8000")
    print("  ✓ API文档: http://localhost:8000/docs")
    print("  ✓ 前端界面: http://localhost:8501")
    print("=" * 60)
    print("\n按 Ctrl+C 停止服务\n")
    
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n服务已停止")

if __name__ == "__main__":
    main()
