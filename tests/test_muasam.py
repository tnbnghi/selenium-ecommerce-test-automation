# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Dữ liệu dùng chung ---
BASE_URL = "https://automationexercise.com/"
USER_EMAIL = "nguyenvan.an1990@vng.com.vn"
USER_PASSWORD = "AnNguyen#VNG25"


class TestShoppingFunctionalities:
    """
    Nhóm các test case cho các chức năng mua sắm: Tìm kiếm, Giỏ hàng, Thanh toán.
    """

    def setup_method(self, method):
        """Chạy trước mỗi test case. Khởi tạo trình duyệt và đăng nhập."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get(BASE_URL)

        self._handle_ad_if_present()

        self.driver.find_element(By.XPATH, "//a[@href='/login']").click()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-qa='login-email']"))).send_keys(
            USER_EMAIL)
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(USER_PASSWORD)
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']")
        self._js_click(login_button)

        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Logged in as')]")))
        print(f"\n--- Bắt đầu Test Case: {method.__name__} ---")

    def teardown_method(self, method):
        """Chạy sau mỗi test case. Đóng trình duyệt."""
        print(f"--- Kết thúc Test Case: {method.__name__} ---")
        time.sleep(3)
        self.driver.quit()

    def _js_click(self, element):
        """Sử dụng JavaScript click để tăng độ ổn định."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", element)

    def _handle_ad_if_present(self):
        """Hàm tìm và đóng quảng cáo toàn màn hình."""
        try:
            WebDriverWait(self.driver, 3).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='aswift']"))
            )
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.frame_to_be_available_and_switch_to_it((By.ID, "ad_iframe"))
                )
            except Exception:
                pass

            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.ID, "dismiss-button"))
            ).click()
            print("Thông báo: Đã phát hiện và đóng quảng cáo.")
        except Exception:
            pass
        finally:
            self.driver.switch_to.default_content()

    # --- Kịch bản kiểm thử ---

    def test_search_tc01_successful_search(self):
        self._js_click(self.driver.find_element(By.XPATH, "//a[@href='/products']"))
        self._handle_ad_if_present()
        search_box = self.wait.until(EC.visibility_of_element_located((By.ID, 'search_product')))
        search_box.send_keys("Dress")
        self._js_click(self.driver.find_element(By.ID, 'submit_search'))
        title = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.title.text-center')))
        assert "SEARCHED PRODUCTS" in title.text
        assert len(self.driver.find_elements(By.CSS_SELECTOR, '.productinfo p')) > 0
        print("Kết quả: Tìm kiếm thành công.")

    def test_search_tc02_nonexistent_search(self):
        self._js_click(self.driver.find_element(By.XPATH, "//a[@href='/products']"))
        self._handle_ad_if_present()
        search_box = self.wait.until(EC.visibility_of_element_located((By.ID, 'search_product')))
        search_box.send_keys("xyzabc")
        self._js_click(self.driver.find_element(By.ID, 'submit_search'))
        title = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.title.text-center')))
        assert "SEARCHED PRODUCTS" in title.text
        assert len(self.driver.find_elements(By.CSS_SELECTOR, '.single-products')) == 0
        print("Kết quả: Tìm kiếm không thành công như mong đợi.")

    def test_cart_tc01_remove_item(self):
        """Kiểm tra việc xóa sản phẩm khỏi giỏ hàng."""
        PRODUCT_ID_TO_TEST = "3"
        product_row_locator = (By.ID, f"product-{PRODUCT_ID_TO_TEST}")

        self.driver.get(BASE_URL + "products")
        self._handle_ad_if_present()

        add_to_cart_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//a[@data-product-id='{PRODUCT_ID_TO_TEST}']")
        ))
        self._js_click(add_to_cart_button)

        self._js_click(self.wait.until(EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))))

        self._handle_ad_if_present()

        self.wait.until(EC.presence_of_element_located(product_row_locator))

        delete_button_for_product = self.driver.find_element(By.XPATH,
                                                             f"//tr[@id='product-{PRODUCT_ID_TO_TEST}']//a[@class='cart_quantity_delete']")
        self._js_click(delete_button_for_product)

        assert self.wait.until(
            EC.invisibility_of_element_located(product_row_locator)), "Sản phẩm đã không bị xóa khỏi giỏ hàng."
        print("Kết quả: Xóa sản phẩm thành công.")

    def test_checkout_tc01_full_purchase_flow(self):
        """Kiểm tra toàn bộ luồng mua hàng thành công (Happy Path)."""
        self.driver.get(BASE_URL + "products")
        self._handle_ad_if_present()

        self._js_click(self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@data-product-id='1'])[1]"))))
        self._js_click(self.wait.until(EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))))

        self._handle_ad_if_present()

        self.wait.until(EC.presence_of_element_located((By.ID, 'cart_items')))
        self._js_click(self.driver.find_element(By.CLASS_NAME, 'check_out'))
        self.wait.until(EC.presence_of_element_located((By.ID, 'address_delivery')))
        self._js_click(self.driver.find_element(By.XPATH, "//a[@href='/payment']"))
        self.wait.until(EC.presence_of_element_located((By.NAME, 'name_on_card'))).send_keys("Test Card")
        self.driver.find_element(By.NAME, 'card_number').send_keys("4100000000000")
        self.driver.find_element(By.NAME, 'cvc').send_keys("123")
        self.driver.find_element(By.NAME, 'expiry_month').send_keys("01")
        self.driver.find_element(By.NAME, 'expiry_year').send_keys("2028")
        self._js_click(self.driver.find_element(By.ID, 'submit'))
        success_title = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2[data-qa='order-placed']")))
        assert "ORDER PLACED!" in success_title.text
        assert self.driver.find_element(By.XPATH,
                                        "//p[contains(text(), 'Congratulations! Your order has been confirmed!')]").is_displayed()
        print("Kết quả: Luồng thanh toán hoàn tất thành công.")