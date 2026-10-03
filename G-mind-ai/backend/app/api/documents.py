import asyncio
import logging
import sqlite3
import uuid
from pathlib import Path

from chromadb.errors import ChromaError
from fastapi import APIRouter, File, HTTPException, UploadFile
from google.genai.errors import APIError
from langchain_google_genai._common import GoogleGenerativeAIError
from starlette.concurrency import run_in_threadpool

from app.api.errors import describe_google_error
from app.config import settings
from app.rag.loader import load_pdf_chunks
from app.rag.vectorstore import add_document

router = APIRouter(prefix="/api/documents", tags=["documents"])
logger = logging.getLogger(__name__)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not settings.google_api_key:
        raise HTTPException(status_code=503, detail="GOOGLE_API_KEY is not configured.")
    filename = Path(file.filename or "document.pdf").name
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    content = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"PDF must be {settings.max_upload_mb} MB or smaller.",
        )
    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF.")

    document_id = str(uuid.uuid4())
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / f"{document_id}.pdf"
    try:
        await asyncio.to_thread(file_path.write_bytes, content)
        chunks = await run_in_threadpool(
            load_pdf_chunks, str(file_path), document_id, filename
        )
        await run_in_threadpool(add_document, chunks)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (APIError, GoogleGenerativeAIError) as exc:
        logger.exception("Document embedding failed.")
        status_code, detail = describe_google_error(exc)
        raise HTTPException(status_code=status_code, detail=detail) from exc
    except (ChromaError, sqlite3.Error) as exc:
        logger.exception("Document embedding or vector storage failed.")
        raise HTTPException(
            status_code=502,
            detail="Document storage failed. Check the vector database configuration.",
        ) from exc
    finally:
        file_path.unlink(missing_ok=True)

    return {
        "document_id": document_id,
        "filename": filename,
        "chunks": len(chunks),
        "message": "Document processed successfully.",
    }
