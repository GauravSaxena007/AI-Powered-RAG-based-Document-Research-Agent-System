from typing import Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from app.config import settings
from app.mcp.server import calculate, get_current_datetime
from app.rag.retriever import retrieve_chunks


class RouteDecision(BaseModel):
    route: Literal["document", "calculator", "datetime"] = Field(
        description="Use document for questions about the uploaded PDF, calculator for arithmetic, and datetime for current date or time."
    )
    expression: str | None = Field(
        default=None,
        description="For calculator requests, the exact arithmetic expression to evaluate, with no surrounding prose.",
    )


class AgentState(TypedDict, total=False):
    question: str
    document_id: str
    route: str
    expression: str | None
    answer: str
    sources: list[dict]


def _chat_model():
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is required to chat.")
    return ChatGoogleGenerativeAI(
        model=settings.llm_model,
        google_api_key=settings.google_api_key,
        temperature=0,
    )


async def understand_question(state: AgentState) -> dict:
    router = _chat_model().with_structured_output(RouteDecision)
    decision = await router.ainvoke(
        [
            SystemMessage(
                content="Choose the best route. Questions about an uploaded file or its contents use document. Plain arithmetic uses calculator and include only its expression in expression. Requests for the current date or time use datetime."
            ),
            HumanMessage(content=state["question"]),
        ]
    )
    return {"route": decision.route, "expression": decision.expression}


async def document_search(state: AgentState) -> dict:
    from starlette.concurrency import run_in_threadpool

    if not state.get("document_id"):
        raise ValueError("Upload a PDF before asking questions about a document.")
    documents = await run_in_threadpool(
        retrieve_chunks, state["question"], state["document_id"]
    )
    if not documents:
        return {
            "answer": "I couldn't find relevant information in this document.",
            "sources": [],
        }

    context = "\n\n".join(
        f"[Source {index}; page {doc.metadata.get('page', 0) + 1}]\n{doc.page_content}"
        for index, doc in enumerate(documents, start=1)
    )
    response = await _chat_model().ainvoke(
        [
            SystemMessage(
                content="Answer using only the supplied document excerpts. If they do not contain the answer, say so. Cite evidence as [Source N]."
            ),
            HumanMessage(
                content=f"Document excerpts:\n{context}\n\nQuestion: {state['question']}"
            ),
        ]
    )
    sources = [
        {
            "page": int(doc.metadata.get("page", 0)) + 1,
            "content": doc.page_content,
        }
        for doc in documents
    ]
    return {"answer": response.content, "sources": sources}


async def use_calculator(state: AgentState) -> dict:
    expression = state.get("expression")
    if not expression:
        raise ValueError("I couldn't identify an arithmetic expression to calculate.")
    result = calculate(expression)
    return {"answer": result, "sources": []}


async def use_datetime(_: AgentState) -> dict:
    return {"answer": get_current_datetime(), "sources": []}


def _select_route(state: AgentState) -> str:
    return state["route"]


builder = StateGraph(AgentState)
builder.add_node("understand_question", understand_question)
builder.add_node("document_search", document_search)
builder.add_node("calculator", use_calculator)
builder.add_node("datetime", use_datetime)
builder.add_edge(START, "understand_question")
builder.add_conditional_edges(
    "understand_question",
    _select_route,
    {
        "document": "document_search",
        "calculator": "calculator",
        "datetime": "datetime",
    },
)
builder.add_edge("document_search", END)
builder.add_edge("calculator", END)
builder.add_edge("datetime", END)
agent = builder.compile()
