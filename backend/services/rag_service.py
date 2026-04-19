import os
import json
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class RAGService:
    def __init__(self, data_path: str = "./demo_data", persist_dir: str = "./data/chroma_db"):
        self.data_path = data_path
        self.persist_dir = persist_dir
        self.documents_file = os.path.join(data_path, "documents.json")
        
        os.makedirs(persist_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="glass_knowledge",
            metadata={"description": "玻璃材料知识库"}
        )
        
        print("正在加载Embedding模型...")
        self.embedding_model = SentenceTransformer('BAAI/bge-m3')
        print("Embedding模型加载完成")
        
        self._documents = self._load_documents()
    
    def _load_documents(self) -> List[Dict]:
        if os.path.exists(self.documents_file):
            with open(self.documents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def init_knowledge_base(self):
        print("正在初始化知识库...")
        
        existing = self.collection.count()
        if existing > 0:
            print(f"知识库已存在 {existing} 条记录，跳过初始化")
            return
        
        documents = self._documents
        if not documents:
            print("警告：没有找到文档数据")
            return
        
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            content = doc.get('content', '')
            chunks = self._split_text(content, chunk_size=500, overlap=100)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc['id']}_chunk_{i}"
                ids.append(chunk_id)
                texts.append(chunk)
                metadatas.append({
                    "source": doc.get('title', '未知'),
                    "author": doc.get('author', ''),
                    "category": doc.get('category', ''),
                    "doc_id": doc['id']
                })
        
        if texts:
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            print(f"知识库初始化完成，共 {len(texts)} 个文档片段")
    
    def _split_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            if end < text_length:
                for sep in ['。', '；', '，', '\n', ' ']:
                    last_sep = chunk.rfind(sep)
                    if last_sep > chunk_size * 0.5:
                        chunk = chunk[:last_sep + 1]
                        end = start + last_sep + 1
                        break
            
            chunks.append(chunk.strip())
            start = end - overlap if end < text_length else text_length
        
        return [c for c in chunks if c]
    
    def query(self, question: str, top_k: int = 5) -> Dict:
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k
        )
        
        sources = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                sources.append({
                    "content": doc,
                    "source": metadata.get('source', '未知'),
                    "author": metadata.get('author', ''),
                    "category": metadata.get('category', '')
                })
        
        confidence = 0.0
        if results['distances'] and results['distances'][0]:
            distances = results['distances'][0]
            if distances:
                avg_distance = sum(distances) / len(distances)
                confidence = max(0, 1 - avg_distance)
        
        return {
            "sources": sources,
            "confidence": round(confidence, 2)
        }
    
    def get_context(self, question: str, top_k: int = 5) -> str:
        result = self.query(question, top_k)
        sources = result['sources']
        
        context_parts = []
        for i, source in enumerate(sources, 1):
            context_parts.append(f"[{i}] {source['content']}")
        
        return "\n\n".join(context_parts)
    
    def get_collection_count(self) -> int:
        return self.collection.count()
