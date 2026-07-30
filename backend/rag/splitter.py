from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)


def split_documents(
    documents: list[Document],
) -> list[Document]:
    """
    Split documents into chunks.
    """

    return _splitter.split_documents(documents)