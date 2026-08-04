import json
from backend.database.connection import conn
from langchain_core.messages import HumanMessage
from backend.llm.model import llm

def save_memory(user_id: int, memory: str):
    """Save a memory for a specific user."""
    conn.execute(
        """
        INSERT OR IGNORE INTO long_term_memory(user_id, memory)
        VALUES(?, ?)
        """,
        (user_id, memory),
    )
    conn.commit()


def get_all_memories(user_id: int):
    """Return memories for a specific user."""
    cur = conn.execute(
        """
        SELECT memory
        FROM long_term_memory
        WHERE user_id = ?
        ORDER BY created_at
        """,
        (user_id,),
    )

    return [row[0] for row in cur.fetchall()]

def extract_memory(user_message: str):
    """
    Extract a long-term memory from a user message.
    Returns None if nothing should be remembered.
    """

    prompt = f"""
You are a memory extraction system.

Extract ONLY permanent or long-term information about the user.

Remember things like:
- Name
- Occupation
- Education
- Skills
- Preferences
- Goals
- Location
- Birthday
- Projects they are working on

DO NOT remember:
- Questions
- Temporary requests
- Greetings
- One-time tasks
- Small talk

Return ONLY valid JSON.

IMPORTANT:
- The value of "memory" MUST be a SINGLE STRING.
- NEVER return an object.
- NEVER return an array.
- NEVER return nested JSON.
- Summarize the information into one sentence.

Examples:

User:
My name is Parthiv.

Output:
{{"save": true, "memory": "User's name is Parthiv."}}

User:
I study Computer Engineering at LDCE and love Python.

Output:
{{"save": true, "memory": "User studies Computer Engineering at LDCE and likes Python."}}

User:
What is Machine Learning?

Output:
{{"save": false}}

---------------------------------

User:
{user_message}
"""

    try:
        response = llm.invoke(
            [HumanMessage(content=prompt)],
            config={"tags": ["nostream"]},
        )

        result = json.loads(response.content)

        if result.get("save"):
            memory = result.get("memory")

            if isinstance(memory, dict):
                memory = json.dumps(memory)

            elif isinstance(memory, list):
                memory = ", ".join(map(str, memory))

            return memory

    except Exception:
        pass

    return None