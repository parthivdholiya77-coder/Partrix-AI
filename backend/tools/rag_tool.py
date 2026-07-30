from langchain_core.tools import tool

from backend.rag.service import retrieve_context, format_context


@tool
def search_documents(
    question: str,
    user_id: int,
    thread_id: str,
) -> str:
    """
   Search the logged-in user's uploaded documents.
    """

    documents = retrieve_context(
        question=question,
        user_id=user_id,
        thread_id=thread_id
    )

    if not documents:
        return "No relevant information found in the uploaded documents."

    context, sources = format_context(documents)

    return f"""
Retrieved Context:

{context}

Sources:
{sources}
"""