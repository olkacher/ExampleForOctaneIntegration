@TID123456REV0.1.0
Feature: Shopping cart

  Scenario: Add and remove an item from the cart
    Given the user has an empty cart
    When the user adds item "book"
    Then the cart contains "book"
    When the user removes item "book"
    Then the cart is empty
