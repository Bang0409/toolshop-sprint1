
"""Sprint 2 - Cart API Testing."""

import pytest


# -------------------------------------------------------
# Fixture: Create a new cart
# -------------------------------------------------------
@pytest.fixture
def new_cart(api):
    """Create a new cart using the Toolshop API."""

    # 1. Tao gio hang moi
    response = api.post("/carts")

    # 2. Kiem tra HTTP 201
    assert response.status == 201, response.text()

    # 3. Tra ve ID cua gio hang
    return response.json()["id"]


# -------------------------------------------------------
# Test: Add product to cart
# -------------------------------------------------------
@pytest.mark.api
@pytest.mark.smoke
def test_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: Verify that the cart stores product quantities.
    Precondition: A new cart and an available product.
    Expected: One cart item with quantity 2 and matching product ID.
    """

    # 1. Lay danh sach san pham
    response = api.get("/products", params={"page": 1})
    assert response.status == 200, response.text()

    # 2. Lay san pham dau tien
    product = response.json()["data"][0]
    product_id = product["id"]

    # 3. Them san pham vao gio hang voi so luong 2
    add_response = api.post(
        f"/carts/{new_cart}",
        data={
            "product_id": product_id,
            "quantity": 2
        }
    )

    assert add_response.ok, add_response.text()

    # 4. Doc thong tin gio hang
    cart_response = api.get(f"/carts/{new_cart}")
    assert cart_response.status == 200, cart_response.text()

    cart_items = cart_response.json()["cart_items"]

    # 5. Kiem tra gio hang co 1 dong san pham
    assert len(cart_items) == 1

    # 6. Kiem tra so luong bang 2
    assert cart_items[0]["quantity"] == 2

    # 7. Kiem tra ID san pham
    assert str(cart_items[0]["product_id"]) == str(product_id)
