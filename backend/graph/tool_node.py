from langchain_core.messages import ToolMessage

from backend.graph.state import ChatState
from backend.tools.registry import TOOLS


TOOLS_BY_NAME = {
    tool.name: tool
    for tool in TOOLS
}


def tool_node(state: ChatState):

    messages = state["messages"]
    user_id = state["user_id"]
    thread_id = str(state["thread_id"])

    ai_message = messages[-1]

    tool_messages = []

    for tool_call in ai_message.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_args["thread_id"] = str(state["thread_id"])

        if tool_name == "search_documents":
            tool_args["user_id"] = user_id
            tool_args["thread_id"] = thread_id

        elif tool_name == "notes":
            tool_args["user_id"] = user_id

        tool = TOOLS_BY_NAME[tool_name]

        result = tool.invoke(tool_args)

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
                name=tool_name,
            )
        )

    return {
        "messages": tool_messages
    }