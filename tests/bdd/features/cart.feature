
Feature: Shopping cart total calculation
  As a customer
  I want to search for products and choose a quantity
  So that I can verify the correct total before checkout

  Scenario Outline: Calculate cart total for selected quantity
    Given the customer is on the Toolshop homepage
    When the customer searches for "<product>" and opens it
    And the customer adds <quantity> units to the cart
    Then the cart shows "<product>" with the correct total for <quantity> units

    Examples:
      | product     | quantity |
      | Claw Hammer | 1        |
      | Claw Hammer | 2        |
