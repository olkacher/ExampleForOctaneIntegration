from config import config


class LoginPage:
    def __init__(self, app_state):
        self.app_state = app_state

    def open(self):
        self.app_state["page"] = "login"

    def login(self, username: str, password: str) -> bool:
        self.app_state["credentials"] = {"username": username, "password": password}
        self.app_state["logged_in"] = (
            username == config.VALID_USERNAME and password == config.VALID_PASSWORD
        )
        return self.app_state["logged_in"]
