#Auto generated Octane revision tag
@TID5010REV0.1.0
Feature: Profile management

  Scenario: Update profile email
    Given the user is on the profile page
    When the user updates email to "user@example.com"
    Then the profile email should be "user@example.com"
