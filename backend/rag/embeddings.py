from functools import lru_cache
from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def get_embedding_model():
    return CohereEmbeddings(
        model="embed-v4.0"
    )