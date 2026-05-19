class CartPage:
    def __init__(self, app_state):
        self.app_state = app_state
        self.app_state.setdefault("cart_items", [])

    def open(self):
        self.app_state["page"] = "cart"

    def add_item(self, item: str):
        self.app_state.setdefault("cart_items", []).append(item)

    def remove_item(self, item: str):
        self.app_state.setdefault("cart_items", [])
        if item in self.app_state["cart_items"]:
            self.app_state["cart_items"].remove(item)
