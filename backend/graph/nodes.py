from langchain_core.messages import SystemMessage
from .state import ChatState
from backend.memory.service import MemoryService
from backend.llm.chat_model import chat_model


def chat_node(state: ChatState):
    messages = state["messages"]
    user_id = state["user_id"]
    latest_user_message = messages[-1].content

    # Extract and save long-term memory
    memory = MemoryService.extract(latest_user_message)

    if memory:
        MemoryService.save(user_id, memory)

    # Retrieve long-term memories
    memories = MemoryService.get_all(user_id)

    memory_text = "No stored memories."

    if memories:
        memory_text = "\n".join(f"- {m}" for m in memories)

    system_prompt = f"""
You are a helpful AI assistant.

You have access to several tools. Use them whenever they are more appropriate than answering from your own knowledge.

IMPORTANT RULES

1. PDF / Document Questions

If the user asks about:
- an uploaded PDF
- an uploaded document
- an uploaded file
- a report
- a resume
- a manual
- "this PDF"
- "the uploaded file"
- "summarize the PDF"

ALWAYS use the `search_documents` tool first.

Never ask the user to upload a PDF unless the `search_documents` tool indicates that no document is available.

2. Current Information

Use the `web_search` tool whenever the user asks about:
- current news
- weather
- sports
- recent events
- information that may have changed recently

3. Personal Notes

Use the `notes` tool whenever the user wants to:
- remember something
- save a note
- write something down
- take a note
- show their notes
- get their notes
- search notes
- update a note
- delete a note

The notes tool manages the user's personal notes stored in the database.

Always use the `notes` tool for note management.
Never rely on conversation history or long-term memory for notes.

Long-term memory:

{memory_text}

Use long-term memory only when it is relevant to the user's request.
"""

    final_messages = [
        SystemMessage(content=system_prompt),
        *messages,
    ]

    try:
        response = chat_model.invoke(final_messages)

    except Exception as e:
        print("=" * 80)
        print(e)
        print("=" * 80)
        raise

    return {
        "messages": [response]
    }