from pytest_bdd import scenarios, given, when, then, parsers
import pytest

@pytest.fixture
def login_context():
    return {}

@given("a user on the login page")
def user_on_login_page(login_context):
    login_context["page"] = "login"
    return login_context

@when(parsers.parse('the user enters username "{username}" and password "{password}"'))
def enter_credentials(username, password, login_context):
    login_context["credentials"] = {
        "username": username,
        "password": password,
    }

@then("the user should be logged in")
def verify_login(login_context):
    assert login_context.get("page") == "login"
    assert login_context.get("credentials") == {
        "username": "testuser",
        "password": "secret",
    }
