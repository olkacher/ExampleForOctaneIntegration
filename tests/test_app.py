from pytest_bdd import scenarios, given, when, then, parsers
import pytest

from tests.pages import AppPages

scenarios("features/login.feature")
scenarios("features/search.feature")
scenarios("features/cart.feature")
scenarios("features/profile.feature")


@pytest.fixture
def app():
    return AppPages()


# Login steps
@given("the user is on the login page")
def user_on_login_page(app):
    app.login.open()
    return app


@when(parsers.parse('the user logs in with username "{username}" and password "{password}"'))
def login_with_credentials(username, password, app):
    app.login.login(username, password)


@then("login should succeed")
def login_should_succeed(app):
    assert app.state.get("logged_in") is True


# Search steps
@given("the user is on the search page")
def user_on_search_page(app):
    app.search.open()
    return app


@when(parsers.parse('the user searches for "{query}"'))
def user_searches_for(query, app):
    app.search.search(query)


@then(parsers.parse('the search results contain "{expected}"'))
def search_results_contain(expected, app):
    assert expected in app.state.get("search_results", [])


# Cart steps
@given("the user has an empty cart")
def user_has_empty_cart(app):
    app.cart.open()
    app.state["cart_items"] = []
    return app


@when(parsers.parse('the user adds item "{item}"'))
def user_adds_item(item, app):
    app.cart.add_item(item)


@then(parsers.parse('the cart contains "{item}"'))
def cart_contains_item(item, app):
    assert item in app.state.get("cart_items", [])


@when(parsers.parse('the user removes item "{item}"'))
def user_removes_item(item, app):
    app.cart.remove_item(item)


@then("the cart is empty")
def cart_is_empty(app):
    assert app.state.get("cart_items") == []


# Profile steps
@given("the user is on the profile page")
def user_on_profile_page(app):
    app.profile.open()
    return app


@when(parsers.parse('the user updates email to "{email}"'))
def user_updates_email(email, app):
    app.profile.update_email(email)


@then(parsers.parse('the profile email should be "{email}"'))
def profile_email_should_be(email, app):
    assert app.state.get("profile_email") == email
