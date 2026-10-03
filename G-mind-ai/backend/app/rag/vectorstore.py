from functools import lru_cache

from langchain_chroma import Chroma

from app.config import settings
from app.rag.embeddings import get_embeddings


@lru_cache
def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name="docmind_google_documents",
        embedding_function=get_embeddings(),
        persist_directory=settings.chroma_dir,
    )


def add_document(chunks) -> None:
    get_vectorstore().add_documents(chunks)
