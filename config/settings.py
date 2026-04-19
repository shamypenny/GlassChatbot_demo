import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ZHIPU_API_KEY: str = os.getenv("ZHIPU_API_KEY", "")
    ZHIPU_API_BASE: str = os.getenv("ZHIPU_API_BASE", "https://open.bigmodel.cn/api/paas/v4")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "./data/glass.db")
    
    PROJECT_NAME: str = "ATG研发端AI助手"
    VERSION: str = "1.0.0"
    
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    TOP_K: int = 5

settings = Settings()
