from backend.threads.service import ThreadService
from langchain_core.messages import HumanMessage
from backend.llm.model import llm

def generate_thread_title(user_message: str, user_id: int = None) -> str:
    try:
        prompt = (
            "Generate a very short title (3 to 5 words, no quotes, no punctuation "
            "at the end) summarizing the topic of this message:\n\n"
            f"{user_message}"
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        title = response.content.strip().strip('"').strip("'")
        title = title if title else user_message[:40]
    except Exception:
        title = user_message.strip()
        title = title[:40] + ("..." if len(title) > 40 else "")

    if user_id is not None:
        existing_titles = {
            ThreadService.get_title(tid, user_id)
            for tid in ThreadService.get_all_threads(user_id)
        }
        base_title = title
        counter = 2
        while title in existing_titles:
            title = f"{base_title} ({counter})"
            counter += 1

    return title