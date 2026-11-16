
"""Sprint 2 - Shopping Cart UI Testing."""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


# -------------------------------------------------------
# Test 1: Verify cart price calculation
# -------------------------------------------------------
@pytest.mark.ui
@pytest.mark.regression
def test_cart_line_price_equals_unit_price_times_quantity(page):
    """Goal: Verify cart price calculation.
    Precondition: Combination Pliers is available.
    Expected: Line price equals unit price times quantity.
    """

    # 1. Mo trang chu
    home = HomePage(page).open()

    # 2. Mo chi tiet san pham
    product = home.open_product("Claw Hammer")

    unit_price = product.price()

    # Cho o so luong san sang de nhap
    expect(product.quantity).to_be_enabled(timeout=15000)

    # Them 2 san pham
    product.add_to_cart(quantity=2)

    # 5. Kiem tra badge gio hang
    expect(product.cart_quantity).to_have_text("2")

    # 6. Mo trang gio hang
    cart = product.go_to_cart()

    # 7. Kiem tra gio hang co 1 dong san pham
    expect(cart.product_titles).to_have_count(1)

    # 8. Lay thanh tien cua san pham
    line_totals = cart.line_totals()

    # 9. Kiem tra thanh tien = don gia * so luong
    assert line_totals[0] == pytest.approx(unit_price * 2)

    # 10. Kiem tra tong tien gio hang
    assert cart.total_value() == pytest.approx(
        sum(line_totals)
    )


# -------------------------------------------------------
# Test 2: Continue Shopping
# -------------------------------------------------------
@pytest.mark.ui
@pytest.mark.regression
def test_cart_continue_shopping_returns_to_home(page):
    """Goal: Verify Continue Shopping navigation.
    Precondition: A product has been added to the cart.
    Expected: Homepage and product list are displayed.
    """

    # 1. Mo trang chu
    home = HomePage(page).open()

    # 2. Mo san pham Claw Hammer
    product = home.open_product("Claw Hammer")

    # 3. Them 1 san pham vao gio
    product.add_to_cart()

    # 4. Mo trang gio hang
    cart = product.go_to_cart()

    # 5. Kiem tra gio hang co san pham
    expect(cart.product_titles).to_have_count(1)

    # 6. Nhan Continue Shopping
    cart.continue_shopping.click()

    # 7. Kiem tra danh sach san pham hien thi lai
    home = HomePage(page)

    expect(home.product_names.first).to_be_visible()
