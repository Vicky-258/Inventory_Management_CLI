class UserSession:
    current_user = None

    @classmethod
    def login(cls, user):
        cls.current_user = user

    @classmethod
    def logout(cls):
        cls.current_user = None

    @classmethod
    def get_current_user(cls):
        return cls.current_user
