from fastapi import APIRouter

from app.schemas.chat import ChatRequest
from app.services.rag_service import RAGService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

rag_service = RAGService()


@router.post("")
async def chat(request: ChatRequest):

    return await rag_service.answer(
        repository_id=request.repository_id,
        question=request.question,
        top_k=request.top_k,
    )
