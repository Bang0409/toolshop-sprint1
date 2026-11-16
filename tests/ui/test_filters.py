
"""Sprint 2 - Product Filter UI Testing."""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_filter_hammer_category_shows_only_hammer_products(page):
    """Goal: Verify filtering products by Hammer category.
    Precondition: Toolshop homepage has available products.
    Expected: Only products containing Hammer are displayed.
    """

    # 1. Mo trang chu Toolshop
    home = HomePage(page).open()

    # 2. Chon danh muc Hammer
    home.filter_hammer()

    # 3. Kiem tra checkbox Hammer da duoc chon
    expect(home.hammer_checkbox).to_be_checked()

    # 4. Kiem tra danh sach khong rong
    expect(home.product_names.first).to_be_visible()

    # 5. Kiem tra khong co san pham ngoai danh muc Hammer
    expect(home.non_hammer_products).to_have_count(0)
