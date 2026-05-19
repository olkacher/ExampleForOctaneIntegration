from playwright.sync_api import Page

from pageobjects.login_page import LoginPage
from pageobjects.profile_page import ProfilePage
from pageobjects.search_page import SearchPage
from pageobjects.cart_page import CartPage


class Pages:
    def __init__(self, page: Page):

        self.login_page = LoginPage(page)
        self.search_page = SearchPage(page)
        self.cart_page = CartPage(page)
        self.profile_page = ProfilePage(page)