from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf.errors import EmptyFileError, FileNotDecryptedError, PdfReadError

from app.config import settings


def load_pdf_chunks(file_path: str, document_id: str, filename: str):
    """Extract PDF pages and split them while retaining page metadata."""
    try:
        pages = PyPDFLoader(file_path).load()
    except (EmptyFileError, FileNotDecryptedError, PdfReadError) as exc:
        raise ValueError("The uploaded PDF is invalid or cannot be read.") from exc
    if not pages or not any(page.page_content.strip() for page in pages):
        raise ValueError("The PDF contains no readable text.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
    )
    chunks = splitter.split_documents(pages)
    for chunk in chunks:
        chunk.metadata.update(
            {
                "document_id": document_id,
                "filename": Path(filename).name,
            }
        )
    return chunks
