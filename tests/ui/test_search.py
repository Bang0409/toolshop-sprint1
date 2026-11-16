
"""Sprint 2 - Search UI Testing."""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_search_unknown_keyword_shows_no_results(page):
    """Goal: Verify searching for an unknown product.
    Precondition: Toolshop home page is available.
    Expected: No products found message and zero products.
    """

    # 1. Mo trang chu Toolshop
    home = HomePage(page).open()

    # 2. Tim kiem san pham khong ton tai
    home.search("zzz-no-such-tool")

    # 3. Kiem tra thong bao khong co san pham
    expect(home.no_results).to_contain_text(
        "There are no products found."
    )

    # 4. Kiem tra danh sach san pham rong
    expect(home.product_names).to_have_count(0)


@pytest.mark.ui
@pytest.mark.regression
def test_sort_products_by_price_ascending_shows_sorted_prices(page):
    """Goal: Verify ascending product price sorting.
    Precondition: Toolshop has available products.
    Expected: Product prices are sorted from low to high.
    """

    # 1. Mo trang chu Toolshop
    home = HomePage(page).open()

    # 2. Dam bao san pham da duoc hien thi
    expect(home.product_names.first).to_be_visible()

    # 3. Sap xep san pham theo gia tang dan
    home.sort_by("price,asc")

    # 4. Doi thao tac sap xep hoan thanh
    expect(home.sorting_completed).to_be_visible()

    # 5. Lay danh sach gia san pham
    prices = home.prices()

    # 6. Kiem tra danh sach khong rong
    assert prices, "No product prices found"

    # 7. Kiem tra gia tang dan
    assert prices == sorted(prices), prices

