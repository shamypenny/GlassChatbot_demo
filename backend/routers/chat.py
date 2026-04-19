from fastapi import APIRouter, HTTPException
from typing import List, Optional
from backend.models.schemas import ChatRequest, ChatResponse, Source
from backend.services.rag_service import RAGService
from backend.services.llm_service import LLMService

router = APIRouter(prefix="/api/chat", tags=["chat"])

rag_service = None
llm_service = None

def get_rag_service():
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
        rag_service.init_knowledge_base()
    return rag_service

def get_llm_service():
    global llm_service
    if llm_service is None:
        llm_service = LLMService()
    return llm_service

@router.post("/query", response_model=ChatResponse)
async def query(request: ChatRequest):
    try:
        rag = get_rag_service()
        llm = get_llm_service()
        
        result = rag.query(request.question, top_k=5)
        sources = result['sources']
        confidence = result['confidence']
        
        context = "\n\n".join([s['content'] for s in sources])
        
        answer = llm.chat_with_context(request.question, context)
        
        formatted_sources = [
            Source(
                content=s['content'][:300] + "..." if len(s['content']) > 300 else s['content'],
                source=s['source'],
                page=s.get('page')
            )
            for s in sources[:3]
        ]
        
        return ChatResponse(
            answer=answer,
            sources=formatted_sources,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_status():
    try:
        rag = get_rag_service()
        return {
            "status": "ok",
            "documents_count": rag.get_collection_count()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
