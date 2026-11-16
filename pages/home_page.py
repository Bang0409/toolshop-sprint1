
"""Page Object for Toolshop Home Page."""

import re

from pages.base_page import BasePage


# Match product list API, but not /products/search
PRODUCT_LIST = re.compile(r"/products(\?.*)?$")


class HomePage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)

        # --------------------------------------------------
        # Search
        # --------------------------------------------------
        self.search_box = page.get_by_test_id("search-query")
        self.search_result_count = page.get_by_test_id(
            "search-result-count"
        )
        self.search_button = page.get_by_test_id("search-submit")
        self.search_caption = page.get_by_test_id("search-caption")
        self.search_completed = page.get_by_test_id("search_completed")

        # --------------------------------------------------
        # Products
        # --------------------------------------------------
        self.product_names = page.get_by_test_id("product-name")
        self.product_prices = page.get_by_test_id("product-price")

        # --------------------------------------------------
        # Empty results
        # --------------------------------------------------
        self.no_results = page.get_by_test_id("no-results")

        # --------------------------------------------------
        # Sorting
        # --------------------------------------------------
        self.sort_select = page.get_by_test_id("sort")
        self.sorting_completed = page.get_by_test_id(
            "sorting_completed"
        )

        # --------------------------------------------------
        # Hammer category filter
        # --------------------------------------------------
        self.hammer_checkbox = page.get_by_role(
            "checkbox",
            name="Hammer",
            exact=True
        )

        self.non_hammer_products = self.product_names.filter(
            has_not_text=re.compile("hammer", re.IGNORECASE)
        )

    # ------------------------------------------------------
    # Open Home Page
    # ------------------------------------------------------
    def open(self):
        """Open homepage and wait for initial product response."""

        with self.page.expect_response(
            lambda response: PRODUCT_LIST.search(response.url) is not None
        ):
            super().open()

        return self

    # ------------------------------------------------------
    # Search Products
    # ------------------------------------------------------
    def search(self, keyword: str):
        """Search products by keyword."""

        self.search_box.fill(keyword)
        self.search_button.click()

        return self

    # ------------------------------------------------------
    # Sort Products
    # ------------------------------------------------------
    def sort_by(self, value: str):
        """Sort products: name,asc | name,desc | price,asc | price,desc."""

        self.sort_select.select_option(value)

        return self

    # ------------------------------------------------------
    # Filter Hammer Category
    # ------------------------------------------------------
    def filter_hammer(self):
        """Filter products by Hammer category."""

        with self.page.expect_response(
            lambda response: (
                PRODUCT_LIST.search(response.url) is not None
                and response.status == 200
            )
        ):
            self.hammer_checkbox.check()

        return self

    # ------------------------------------------------------
    # Find Product Card
    # ------------------------------------------------------
    def product_card(self, name: str):
        """Find a product by its exact name."""

        return self.product_names.filter(
            has_text=re.compile(
                rf"^\s*{re.escape(name)}\s*$"
            )
        )

    # ------------------------------------------------------
    # Open Product Detail
    # ------------------------------------------------------
    def open_product(self, name: str):
        """Open product detail page."""

        from pages.product_page import ProductPage

        self.product_card(name).click()

        return ProductPage(self.page)

    # ------------------------------------------------------
    # Get Product Prices
    # ------------------------------------------------------
    def prices(self) -> list[float]:
        """Return displayed product prices as floats."""

        return [
            float(
                text.replace("$", "")
                    .replace(",", "")
                    .strip()
            )
            for text in self.product_prices.all_inner_texts()
        ]
