#Auto generated Octane revision tag
@TID5011REV0.1.0
Feature: Search

  Scenario: Search returns matching results
    Given the user is on the search page
    When the user searches for "pytest"
    Then the search results contain "pytest-bdd"
