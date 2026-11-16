
"""Sprint 2 - Login UI Testing."""

import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.regression
def test_login_empty_form_shows_required_errors(page):
    """Goal: Verify required field validation on login form.
    Precondition: Email and password fields are empty.
    Expected: Both required error messages are displayed.
    """

    # 1. Mo trang dang nhap
    login = LoginPage(page).open()

    # 2. Dam bao email va password dang rong
    expect(login.email).to_be_empty()
    expect(login.password).to_be_empty()

    # 3. Nhan Login khi chua nhap du lieu
    login.login_button.click()

    # 4. Kiem tra loi Email
    expect(login.email_error).to_contain_text(
        "Email is required"
    )

    # 5. Kiem tra loi Password
    expect(login.password_error).to_contain_text(
        "Password is required"
    )

    # 6. Kiem tra nguoi dung van o trang dang nhap
    expect(page).to_have_url(
        re.compile(r"/auth/login/?$")
    )
