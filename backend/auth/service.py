from .repository import signup, login


class AuthService:

    @staticmethod
    def signup(username, email, password):
        return signup(username, email, password)

    @staticmethod
    def login(email, password):
        return login(email, password)