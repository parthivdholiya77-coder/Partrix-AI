from backend.llm.model import llm
from backend.tools.registry import TOOLS

chat_model = llm.bind_tools(TOOLS)