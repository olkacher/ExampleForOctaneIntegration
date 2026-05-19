Feature: Search

  Scenario: Search returns matching results
    Given the user is on the search page
    When the user searches for "pytest"
    Then the search results contain "pytest-bdd"
