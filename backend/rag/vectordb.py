import os

from langchain_core.documents import Document
from langchain_chroma import Chroma

from backend.rag.embeddings import get_embedding_model


def get_db_path(
    user_id: int,
    thread_id: str,
) -> str:
    """
    Returns the vector database path for a user's specific chat thread.
    """

    db_path = os.path.join(
        "backend",
        "vector_db",
        str(user_id),
        thread_id,
    )

    os.makedirs(db_path, exist_ok=True)

    return db_path


def load_vector_db(
    user_id: int,
    thread_id: str,
) -> Chroma:
    """
    Load (or create) the Chroma vector database for a specific chat thread.
    """

    return Chroma(
        persist_directory=get_db_path(
            user_id,
            thread_id,
        ),
        embedding_function=get_embedding_model(),
    )


def add_documents(
    user_id: int,
    thread_id: str,
    documents: list[Document],
) -> None:
    """
    Add document chunks to the thread-specific Chroma database.
    """

    db = load_vector_db(
        user_id=user_id,
        thread_id=thread_id,
    )

    BATCH_SIZE = 64

    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i:i + BATCH_SIZE]

        ids = [
            doc.metadata["chunk_id"]
            for doc in batch
        ]

        db.add_documents(
            documents=batch,
            ids=ids,
        )

    del db