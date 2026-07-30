from backend.database.connection import conn

def save_thread_name(thread_id, user_id, name):
    conn.execute(
        """
        INSERT INTO thread_metadata(thread_id, user_id, thread_name)
        VALUES(?, ?, ?)
        ON CONFLICT(thread_id)
        DO UPDATE SET thread_name = excluded.thread_name
        """,
        (str(thread_id), user_id, name),
    )

    conn.commit()

def retrieve_all_threads(user_id):
    cur = conn.execute(
        """
        SELECT thread_id
        FROM thread_metadata
        WHERE user_id = ?
        ORDER BY created_at ASC
        """,
        (user_id,),
    )

    return [row[0] for row in cur.fetchall()]

def get_thread_name(thread_id, user_id):
    cur = conn.execute(
    """
    SELECT thread_name
    FROM thread_metadata
    WHERE thread_id = ? AND user_id = ?
    """,
    (str(thread_id), user_id),
)
    row = cur.fetchone()
    return row[0] if row else "New Chat"

def delete_thread(thread_id, user_id):
    thread_id = str(thread_id)
    cur = conn.cursor()

    # delete from LangGraph's checkpoint tables
    cur.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
    cur.execute("DELETE FROM writes WHERE thread_id = ?", (thread_id,))

    # delete our custom metadata row
    cur.execute(
    """
    DELETE FROM thread_metadata
    WHERE thread_id = ? AND user_id = ?
    """,
    (thread_id, user_id),
    )
    conn.commit()

def thread_belongs_to_user(thread_id, user_id):
    cur = conn.execute(
        """
        SELECT 1
        FROM thread_metadata
        WHERE thread_id = ? AND user_id = ?
        """,
        (str(thread_id), user_id),
    )

    return cur.fetchone() is not None

conn.commit()

