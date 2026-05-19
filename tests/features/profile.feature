Feature: Profile management

  Scenario: Update profile email
    Given the user is on the profile page
    When the user updates email to "user@example.com"
    Then the profile email should be "user@example.com"
