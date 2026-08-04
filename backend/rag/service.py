import os
import uuid
from datetime import datetime

from langchain_core.documents import Document

from backend.rag.loader import load_pdf
from backend.rag.splitter import split_documents
from backend.rag.retriever import retrieve_documents
from backend.rag.utils import calculate_file_hash
from backend.rag.vectordb import add_documents


def ingest_pdf(
    file_path: str,
    user_id: int,
    thread_id: str,
) -> None:
    """
    Load, split, enrich metadata, and store a PDF
    in the thread-specific vector database.
    """

    documents = load_pdf(file_path)

    chunks = split_documents(documents)

    filename = os.path.basename(file_path)
    file_hash = calculate_file_hash(file_path)

    for chunk in chunks:
        chunk.metadata["user_id"] = user_id
        chunk.metadata["thread_id"] = thread_id
        chunk.metadata["source"] = filename
        chunk.metadata["file_hash"] = file_hash
        chunk.metadata["chunk_id"] = str(uuid.uuid4())
        chunk.metadata["uploaded_at"] = datetime.utcnow().isoformat()

        if "page" not in chunk.metadata:
            chunk.metadata["page"] = "Unknown"

    add_documents(
        user_id=user_id,
        thread_id=thread_id,
        documents=chunks,
    )
    
    


def retrieve_context(
    question: str,
    user_id: int,
    thread_id: str,
) -> list[Document]:
    """
    Retrieve relevant chunks for a question.
    """

    return retrieve_documents(
        question=question,
        user_id=user_id,
        thread_id=thread_id,
    )


def format_context(
    documents: list[Document],
) -> tuple[str, str]:
    """
    Convert retrieved documents into
    a context string and source list.
    """

    context_parts = []
    sources = []
    seen = set()

    for doc in documents:

        context_parts.append(doc.page_content)

        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        key = (source, page)

        if key not in seen:
            seen.add(key)
            sources.append(
                f"- {source} (Page {page})"
            )

    context = "\n\n".join(context_parts)
    source_text = "\n".join(sources)

    return context, source_text