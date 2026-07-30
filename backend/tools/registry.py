from .calculator import calculator
from .weather import weather
from .web_search import web_search
from .rag_tool import search_documents
from .notes import notes

TOOLS = [
    calculator,
    weather,
    web_search,
    search_documents,
    notes,
]