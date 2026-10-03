import logging
import sqlite3

from chromadb.errors import ChromaError
from fastapi import APIRouter, HTTPException
from google.genai.errors import APIError
from langchain_google_genai._common import GoogleGenerativeAIError
from pydantic import BaseModel, Field

from app.api.errors import describe_google_error
from app.agents.graph import agent
from app.config import settings

router = APIRouter(prefix="/api", tags=["chat"])
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    document_id: str | None = None


@router.post("/chat")
async def chat(request: ChatRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    if not settings.google_api_key:
        raise HTTPException(status_code=503, detail="GOOGLE_API_KEY is not configured.")

    try:
        result = await agent.ainvoke(
            {"question": question, "document_id": request.document_id or ""}
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (APIError, GoogleGenerativeAIError) as exc:
        logger.exception("Chat model request failed.")
        status_code, detail = describe_google_error(exc)
        raise HTTPException(status_code=status_code, detail=detail) from exc
    except (ChromaError, sqlite3.Error) as exc:
        logger.exception("Vector retrieval failed.")
        raise HTTPException(status_code=502, detail="Document search failed.") from exc

    return {"answer": result["answer"], "sources": result.get("sources", [])}
