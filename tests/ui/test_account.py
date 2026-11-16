
"""Sprint 2 - Account UI Testing."""

import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage


@pytest.mark.ui
@pytest.mark.smoke
def test_account_logged_in_user_shows_my_account(logged_in_page):
    """Goal: Verify authenticated account page.
    Precondition: User is logged in using storage_state.
    Expected: My account title and QA Bot user menu.
    """

    # 1. Mo trang tai khoan da dang nhap
    account = AccountPage(logged_in_page).open()

    # 2. Kiem tra tieu de trang
    expect(account.title).to_have_text("My account")

    # 3. Kiem tra menu hien thi ten nguoi dung
    expect(account.nav_menu).to_contain_text("QA Bot")
