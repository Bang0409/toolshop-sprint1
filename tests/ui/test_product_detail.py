
"""Sprint 2 - Product Detail UI Testing."""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_product_detail_shows_correct_name_and_price(page):
    """Goal: Verify product detail information.
    Precondition: Claw Hammer is available on the homepage.
    Expected: Product name and price match the homepage.
    """

    # 1. Mo trang chu Toolshop
    home = HomePage(page).open()

    # 2. Chon san pham can kiem tra
    product_name = "Claw Hammer"

    # 3. Dam bao san pham ton tai
    expect(home.product_card(product_name)).to_be_visible()

    # 4. Lay danh sach ten va gia san pham tren trang chu
    names = [
        name.strip()
        for name in home.product_names.all_inner_texts()
    ]

    prices = home.prices()

    # 5. Kiem tra ten va gia duoc lay tu cung danh sach
    assert len(names) == len(prices)

    # 6. Lay gia cua Claw Hammer tren trang chu
    product_index = names.index(product_name)
    expected_price = prices[product_index]

    # 7. Mo trang chi tiet san pham
    product = home.open_product(product_name)

    # 8. Kiem tra ten san pham
    expect(product.name).to_have_text(product_name)

    # 9. Kiem tra gia san pham hien thi
    expect(product.unit_price).to_be_visible()

    # 10. Kiem tra gia khop voi trang chu
    actual_price = product.price()

    assert actual_price == expected_price, (
        f"Expected: ${expected_price}, Actual: ${actual_price}"
    )
