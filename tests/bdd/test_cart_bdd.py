
"""Sprint 2B - BDD Shopping Cart Testing."""

import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenario, then, when

from pages.home_page import HomePage


pytestmark = [pytest.mark.bdd, pytest.mark.ui]


@scenario(
    "cart.feature",
    "Calculate cart total for selected quantity"
)
def test_cart_total_matches_selected_quantity():
    """Goal: Verify the complete shopping cart workflow.
    Precondition: The selected product is available.
    Expected: Cart total equals unit price times quantity.
    """


@given(
    "the customer is on the Toolshop homepage",
    target_fixture="home"
)
def customer_opens_homepage(page):
    """Open the product catalogue."""
    return HomePage(page).open()


@when(
    parsers.parse(
        'the customer searches for "{product}" and opens it'
    ),
    target_fixture="product_page"
)
def customer_searches_and_opens_product(home, product):
    """Find and open the selected product."""

    with home.page.expect_response(
        lambda response: (
            "/products/search" in response.url
            and response.status == 200
        )
    ):
        home.search(product)

    expect(home.product_card(product)).to_be_visible()

    return home.open_product(product)


@when(
    parsers.parse(
        "the customer adds {quantity:d} units to the cart"
    ),
    target_fixture="cart_context"
)
def customer_adds_product_to_cart(product_page, quantity):
    """Add the requested quantity to the cart."""

    expect(product_page.quantity).to_be_enabled()

    unit_price = product_page.price()

    product_page.add_to_cart(quantity=quantity)

    cart = product_page.go_to_cart()

    return {
        "cart": cart,
        "unit_price": unit_price,
    }


@then(
    parsers.parse(
        'the cart shows "{product}" with the correct total '
        'for {quantity:d} units'
    )
)
def cart_total_is_correct(cart_context, product, quantity):
    """Verify product details and calculated cart total."""

    cart = cart_context["cart"]
    unit_price = cart_context["unit_price"]

    expect(cart.product_titles.first).to_contain_text(product)

    expect(cart.product_titles).to_have_count(1)

    expected_total = unit_price * quantity

    line_totals = cart.line_totals()

    assert len(line_totals) == 1

    assert line_totals[0] == pytest.approx(expected_total)

    assert cart.total_value() == pytest.approx(expected_total)
