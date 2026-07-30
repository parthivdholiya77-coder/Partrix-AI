from typing import Optional,Any

from langchain_core.tools import tool
from backend.tools.notes_db import (
    add_note,
    get_notes,
    update_note,
    delete_note,
    search_notes,
)


@tool
def notes(
    action: str,
    user_id: int,
    note: Optional[str] = None,
    note_id: Optional[int] = None,
    keyword: Optional[str] = None,
) -> dict[str, Any]:
    """
    Manage user's notes.

    Actions:
    - add
    - get
    - update
    - delete
    - search

    Examples:

    Add:
        action="add"
        note="Interview on Friday"

    Get:
        action="get"

    Update:
        action="update"
        note_id=2
        note="Interview on Saturday"

    Delete:
        action="delete"
        note_id=2

    Search:
        action="search"
        keyword="Interview"
    """

    action = action.lower()

    if action == "add":
        if not note:
            return {
                "status": "error",
                "message": "Please provide a note.",
            }

        note_id = add_note(user_id, note)
        return {
            "status": "success",
            "message": "Note saved successfully.",
            "note_id": note_id,
        }

    elif action == "get":
        user_notes = get_notes(user_id)

        if not user_notes:
            return {
                "status": "success",
                "notes": [],
            }

        return {
            "status": "success",
            "notes": user_notes,
        }

    elif action == "update":
        if note_id is None or not note:
            return {
                "status": "error",
                "message": "Please provide both note_id and note.",
            }

        success = update_note(
            user_id=user_id,
            note_id=note_id,
            note=note,
        )

        if success:
            return {
                "status": "success",
                "message": "Note updated successfully.",
            }

        return {
            "status": "error",
            "message": "Note not found.",
        }

    elif action == "delete":
        if note_id is None:
            return {
                "status": "error",
                "message": "Please provide note_id.",
            }

        success = delete_note(
            user_id=user_id,
            note_id=note_id,
        )

        if success:
            return {
                "status": "success",
                "message": "Note deleted successfully.",
            }

        return {
            "status": "error",
            "message": "Note not found.",
        }

    elif action == "search":
        if not keyword:
            return {
                "status": "error",
                "message": "Please provide a keyword.",
            }

        results = search_notes(
            user_id=user_id,
            keyword=keyword,
        )

        if not results:
            return {
                "status": "success",
                "notes": [],
            }

        return {
            "status": "success",
            "notes": results,
        }

    return {
        "status": "error",
        "message": "Invalid action.",
    }