from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import settings


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is required to process documents.")
    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
    )
