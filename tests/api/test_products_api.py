
"""Sprint 2 - Product API Testing."""

import json
from pathlib import Path

import pytest


# Read test data from JSON
DATA_FILE = Path(__file__).parents[2] / "data" / "search_keywords.json"
KEYWORDS = json.loads(DATA_FILE.read_text(encoding="utf-8"))


# -------------------------------------------------------
# Test 1: Product JSON structure
# -------------------------------------------------------
@pytest.mark.api
@pytest.mark.smoke
def test_products_first_page_has_valid_structure(api):
    """Goal: Check the product JSON contract.
    Precondition: Product API is available.
    Expected: HTTP 200 and valid product fields.
    """

    response = api.get("/products", params={"page": 1})

    assert response.status == 200, response.text()

    body = response.json()

    required_keys = [
        "current_page",
        "data",
        "per_page",
        "total",
        "last_page"
    ]

    for key in required_keys:
        assert key in body

    assert 0 < len(body["data"]) <= body["per_page"]

    for product in body["data"]:
        assert isinstance(product["id"], (str, int))
        assert isinstance(product["name"], str)
        assert product["name"].strip()
        assert isinstance(product["price"], (int, float))
        assert product["price"] > 0


# -------------------------------------------------------
# Test 2: Data-driven product search
# -------------------------------------------------------
@pytest.mark.api
@pytest.mark.parametrize(
    "case",
    KEYWORDS,
    ids=[case["keyword"] for case in KEYWORDS]
)
def test_products_search_returns_matching_names(api, case):
    """Goal: Search products using JSON test data.
    Precondition: Search keyword exists in test data.
    Expected: Every returned name contains the keyword.
    """

    response = api.get(
        "/products/search",
        params={"q": case["keyword"]}
    )

    assert response.status == 200, response.text()

    body = response.json()
    names = [product["name"] for product in body["data"]]

    assert len(names) > 0

    assert all(
        case["must_contain"] in name.lower()
        for name in names
    ), names


# -------------------------------------------------------
# Test 3: HTTP 4xx error handling
# -------------------------------------------------------
@pytest.mark.api
@pytest.mark.parametrize(
    "path, expected",
    [
        ("/users/me", 401),
        ("/products/does-not-exist", 404),
    ]
)
def test_products_invalid_or_protected_path_returns_4xx(
    api, path, expected
):
    """Goal: Verify HTTP error responses.
    Precondition: Missing resource or unauthenticated user.
    Expected: Correct HTTP 401 or 404 status.
    """

    response = api.get(path)

    assert response.status == expected, response.text()
