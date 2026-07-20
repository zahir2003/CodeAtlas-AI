from fastapi import APIRouter, HTTPException

from app.schemas.search import (
    SearchRequest,
    SearchResponse,
)
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

service = SearchService()


@router.post(
    "/",
    response_model=SearchResponse,
)
async def semantic_search(
    request: SearchRequest,
):

    try:
        return await service.search(
            repository_id=request.repository_id,
            query=request.query,
            top_k=request.top_k,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
