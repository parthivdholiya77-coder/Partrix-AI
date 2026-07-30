from backend.tools.notes_db import *

user_id = 1

print(add_note(user_id, "Interview on Friday"))

print(add_note(user_id, "Buy groceries"))

print(get_notes(user_id))

print(search_notes(user_id, "Interview"))

print(update_note(
    user_id,
    1,
    "Interview on Saturday"
))

print(delete_note(
    user_id,
    2,
))

print(get_notes(user_id))