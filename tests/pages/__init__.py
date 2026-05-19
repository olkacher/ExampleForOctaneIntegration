from .cart_page import CartPage
from .login_page import LoginPage
from .profile_page import ProfilePage
from .search_page import SearchPage


class AppPages:
    def __init__(self):
        self.state = {}
        self.login = LoginPage(self.state)
        self.search = SearchPage(self.state)
        self.cart = CartPage(self.state)
        self.profile = ProfilePage(self.state)
