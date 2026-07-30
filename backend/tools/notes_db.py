from backend.database.connection import conn


def add_note(
    user_id: int,
    note: str,
) -> int:
    """
    Save a note for a user.
    Returns the newly created note ID.
    """

    cursor = conn.execute(
        """
        INSERT INTO notes (user_id, note)
        VALUES (?, ?)
        """,
        (user_id, note),
    )

    conn.commit()

    return cursor.lastrowid


def get_notes(user_id: int) -> list[dict]:
    """
    Get all notes for a user.
    """

    cursor = conn.execute(
        """
        SELECT id, note, created_at
        FROM notes
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    return [dict(row) for row in cursor.fetchall()]


def update_note(
    user_id: int,
    note_id: int,
    note: str,
) -> bool:
    """
    Update a user's note.
    """

    cursor = conn.execute(
        """
        UPDATE notes
        SET note = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            note,
            note_id,
            user_id,
        ),
    )

    conn.commit()

    return cursor.rowcount > 0


def delete_note(
    user_id: int,
    note_id: int,
) -> bool:
    """
    Delete a note.
    """

    cursor = conn.execute(
        """
        DELETE FROM notes
        WHERE id = ? AND user_id = ?
        """,
        (
            note_id,
            user_id,
        ),
    )

    conn.commit()

    return cursor.rowcount > 0


def search_notes(
    user_id: int,
    keyword: str,
) -> list[dict]:
    """
    Search notes using a keyword.
    """

    cursor = conn.execute(
        """
        SELECT id, note, created_at
        FROM notes
        WHERE user_id = ?
        AND note LIKE ?
        ORDER BY created_at DESC
        """,
        (
            user_id,
            f"%{keyword}%",
        ),
    )

    return [dict(row) for row in cursor.fetchall()]