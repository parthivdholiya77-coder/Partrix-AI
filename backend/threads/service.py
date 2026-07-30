from .repository import *

class ThreadService:

    @staticmethod
    def create(thread_id, user_id):
        save_thread_name(
            thread_id,
            user_id,
            "New Chat"
        )

    @staticmethod
    def delete(thread_id, user_id):
        delete_thread(thread_id, user_id)

    @staticmethod
    def get_all_threads(user_id):
        return retrieve_all_threads(user_id)

    @staticmethod
    def rename(thread_id, user_id, name):
        save_thread_name(
            thread_id,
            user_id,
            name
        )
    
    @staticmethod
    def get_title(thread_id, user_id):
        return get_thread_name(
            thread_id,
            user_id
        )
    
    @staticmethod
    def belongs_to_user(thread_id, user_id):
        return thread_belongs_to_user(thread_id, user_id)