from langgraph.graph import StateGraph, START
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import tools_condition

from backend.database.connection import conn
from backend.graph.state import ChatState
from backend.graph.nodes import chat_node
from backend.graph.tool_node import tool_node

checkpointer = SqliteSaver(conn)

graph = StateGraph(ChatState)

graph.add_node("chatbot", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chatbot")

graph.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph.add_edge("tools", "chatbot")

chatbot = graph.compile(
    checkpointer=checkpointer
)