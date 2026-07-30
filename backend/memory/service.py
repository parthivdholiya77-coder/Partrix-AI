from .repository import (
    extract_memory,
    save_memory,
    get_all_memories,
)


class MemoryService:

    @staticmethod
    def extract(user_message):
        return extract_memory(user_message)

    @staticmethod
    def save(user_id, memory):
        save_memory(user_id, memory)

    @staticmethod
    def get_all(user_id):
        return get_all_memories(user_id)