Feature: User login

  Scenario: Successful login with correct credentials
    Given the user is on the login page
    When the user logs in with username "testuser" and password "secret"
    Then login should succeed
