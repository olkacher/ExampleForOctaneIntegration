from tests.config import config


class ProfilePage:
    def __init__(self, app_state):
        self.app_state = app_state

    def open(self):
        self.app_state["page"] = "profile"
        self.app_state.setdefault("profile_email", config.DEFAULT_EMAIL)

    def update_email(self, email: str):
        self.app_state["profile_email"] = email
