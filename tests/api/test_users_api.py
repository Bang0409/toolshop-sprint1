
"""Sprint 2 - User API Testing."""

import pytest


# -------------------------------------------------------
# Test 1: Register with empty body
# -------------------------------------------------------
@pytest.mark.api
def test_users_register_empty_body_returns_422(api):
    """Goal: Verify server-side registration validation.
    Precondition: Registration body is empty.
    Expected: HTTP 422 with email and password errors.
    """

    # 1. Gui request dang ky voi du lieu rong
    response = api.post(
        "/users/register",
        data={}
    )

    # 2. Kiem tra HTTP status 422
    assert response.status == 422, response.text()

    # 3. Doc JSON response
    body = response.json()

    # 4. Kiem tra loi email va password
    assert "email" in body
    assert "password" in body


# -------------------------------------------------------
# Test 2: Access profile with Bearer Token
# -------------------------------------------------------
@pytest.mark.api
@pytest.mark.smoke
def test_users_me_with_token_returns_own_profile(
    api, auth_headers, test_user
):
    """Goal: Verify authenticated profile access.
    Precondition: A registered test user and valid token.
    Expected: HTTP 200 and matching account email.
    """

    # 1. Goi API lay thong tin tai khoan
    response = api.get(
        "/users/me",
        headers=auth_headers
    )

    # 2. Kiem tra HTTP status 200
    assert response.status == 200, response.text()

    # 3. Lay thong tin tai khoan
    body = response.json()

    # 4. Kiem tra email trung voi tai khoan test
    assert body["email"] == test_user["email"]
