
import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage


@pytest.mark.smoke
def test_smoke_search_product(page):
    """Mục tiêu: Kiểm tra chức năng tìm kiếm sản phẩm.
    Điều kiện: Trang Toolshop hoạt động và có sản phẩm pliers.
    Mong đợi: Mọi sản phẩm hiển thị đều chứa chữ pliers.
    """
    home = HomePage(page).open()
    home.search("pliers")

    expect(home.product_names.first).to_be_visible()
    expect(
        home.product_names.filter(has_not_text="pliers")
    ).to_have_count(0)


@pytest.mark.smoke
def test_smoke_add_to_cart(page):
    """Mục tiêu: Kiểm tra thêm 3 Claw Hammer vào giỏ hàng.
    Điều kiện: Sản phẩm Claw Hammer có thể mua.
    Mong đợi: Badge giỏ hàng hiển thị số 3.
    """
    home = HomePage(page).open()
    product = home.open_product("Claw Hammer")
    product.add_to_cart(quantity=3)

    expect(product.cart_quantity).to_have_text("3")


@pytest.mark.smoke
def test_smoke_invalid_login(page):
    """Mục tiêu: Kiểm tra đăng nhập bằng tài khoản không tồn tại.
    Điều kiện: Sử dụng email không tồn tại và mật khẩu bất kỳ.
    Mong đợi: Hiện lỗi Invalid email or password và vẫn ở trang login.
    """
    login = LoginPage(page).open()

    login.login(
        "nobody-here@example.com",
        "WrongPassword123!"
    )

    expect(login.login_error).to_have_text(
        "Invalid email or password"
    )

    expect(page).to_have_url(
        re.compile(r"/auth/login/?$")
    )


@pytest.mark.smoke
def test_smoke_empty_contact_form(page):
    """Mục tiêu: Kiểm tra validation khi gửi form Contact trống.
    Điều kiện: Không nhập bất kỳ thông tin nào vào form.
    Mong đợi: Hiện lỗi Subject is required và Message is required.
    """
    contact = ContactPage(page).open()

    contact.submit()

    expect(contact.subject_error).to_have_text(
        "Subject is required"
    )

    expect(contact.message_error).to_have_text(
        "Message is required"
    )
