
"""Sprint 2 - Network Interception Testing."""

import json
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


# Regex nhan dien API danh sach san pham
PRODUCT_LIST = re.compile(r"/products(\?.*)?$")

# JSON gia lap danh sach san pham rong
EMPTY_PAGE = {
    "current_page": 1,
    "data": [],
    "from": None,
    "last_page": 1,
    "per_page": 9,
    "to": None,
    "total": 0
}


# -------------------------------------------------------
# Test 1: Block image resources
# -------------------------------------------------------
@pytest.mark.ui
@pytest.mark.smoke
def test_home_without_images_still_lists_products(page):
    """Goal: Verify the page works when images are blocked.
    Precondition: Image requests are intercepted.
    Expected: Product names remain visible and images are blocked.
    """

    # 1. Luu URL cua cac anh bi chan
    blocked = []

    # 2. Xu ly request anh
    def block(route):
        blocked.append(route.request.url)
        route.abort()

    # 3. Dang ky route truoc khi mo trang
    page.route(
        re.compile(r"\.(png|jpe?g|webp|avif|svg)(\?.*)?$"),
        block
    )

    # 4. Mo trang chu
    home = HomePage(page).open()

    # 5. Kiem tra san pham van hien thi
    expect(home.product_names.first).to_be_visible()

    # 6. Kiem tra anh da bi chan
    assert blocked, "No image requests were blocked"


# -------------------------------------------------------
# Test 2: Mock empty product list
# -------------------------------------------------------
@pytest.mark.ui
def test_home_with_empty_products_shows_no_results(page):
    """Goal: Verify the UI when the product list is empty.
    Precondition: Product API is mocked with empty data.
    Expected: No products found message and zero products.
    """

    # 1. Gia lap API tra ve danh sach rong
    page.route(
        PRODUCT_LIST,
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(EMPTY_PAGE)
        )
    )

    # 2. Mo trang chu
    home = HomePage(page).open()

    # 3. Kiem tra thong bao khong co san pham
    expect(home.no_results).to_have_text(
        "There are no products found."
    )

    # 4. Kiem tra danh sach san pham rong
    expect(home.product_names).to_have_count(0)
