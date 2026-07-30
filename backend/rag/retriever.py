from langchain_core.documents import Document

from backend.rag.vectordb import load_vector_db


def retrieve_documents(
    question: str,
    user_id: int,
    thread_id: str,
    k: int = 8,
) -> list[Document]:
    """
    Retrieve the most relevant document chunks
    using similarity search.
    """

    db = load_vector_db(
        user_id=user_id,
        thread_id=thread_id,
    )

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
        },
    )

    return retriever.invoke(question)