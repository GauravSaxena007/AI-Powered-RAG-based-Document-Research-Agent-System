from app.rag.vectorstore import get_vectorstore


def retrieve_chunks(question: str, document_id: str, limit: int = 4):
    return get_vectorstore().similarity_search(
        question,
        k=limit,
        filter={"document_id": document_id},
    )
