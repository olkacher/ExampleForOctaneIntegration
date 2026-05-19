from tests.config import config


class SearchPage:
    def __init__(self, app_state):
        self.app_state = app_state

    def open(self):
        self.app_state["page"] = "search"

    def search(self, query: str):
        self.app_state["search_query"] = query
        results = config.SEARCH_RESULTS_PYTEST if query == "pytest" else []
        self.app_state["search_results"] = results
        return results
