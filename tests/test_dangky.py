# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Dữ liệu dùng chung ---
BASE_URL = "https://automationexercise.com/"


class TestSignup:
    """
    Nhóm các test case cho chức năng Đăng ký.
    """

    def setup_method(self, method):
        """Chạy trước mỗi test case. Khởi tạo trình duyệt."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(BASE_URL)
        time.sleep(1)
        # Đi đến trang đăng ký/đăng nhập
        try:
            login_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/login']")))
            login_link.click()
            time.sleep(1)
        except Exception as e:
            pytest.fail(f"Không thể click vào link Login/Signup. Lỗi: {e}")

    def teardown_method(self, method):
        """Chạy sau mỗi test case. Đóng trình duyệt."""
        time.sleep(3)
        self.driver.quit()

    # --- Helper Method: Các hàm hỗ trợ để tái sử dụng code ---
    def _start_signup_step(self, name, email):
        """Hàm thực hiện bước 1: Nhập tên, email và nhấn Signup."""
        self.wait.until(EC.visibility_of_element_located((By.NAME, "name")))
        name_field = self.driver.find_element(By.NAME, "name")
        email_field = self.driver.find_element(By.XPATH, "//form[@action='/signup']/input[@name='email']")

        name_field.clear()
        email_field.clear()

        name_field.send_keys(name)
        time.sleep(0.5)
        email_field.send_keys(email)
        time.sleep(0.5)

        # Sử dụng JavaScript executor để tránh lỗi quảng cáo che khuất
        signup_button = self.driver.find_element(By.XPATH, "//button[text()='Signup']")
        self.driver.execute_script("arguments[0].click();", signup_button)
        time.sleep(2)

    def _fill_account_details_step(self, data, skip_address=False):
        """Hàm thực hiện bước 2: Điền chi tiết thông tin tài khoản."""
        self.wait.until(EC.visibility_of_element_located((By.ID, "password")))
        self.driver.find_element(By.ID, "id_gender1").click()
        self.driver.find_element(By.ID, "password").send_keys(data["password"])

        Select(self.driver.find_element(By.ID, "days")).select_by_value("10")
        Select(self.driver.find_element(By.ID, "months")).select_by_visible_text("May")
        Select(self.driver.find_element(By.ID, "years")).select_by_value("1990")

        self.driver.find_element(By.ID, "newsletter").click()
        self.driver.find_element(By.ID, "optin").click()

        self.driver.find_element(By.ID, "first_name").send_keys(data["first_name"])
        self.driver.find_element(By.ID, "last_name").send_keys(data["last_name"])
        self.driver.find_element(By.ID, "company").send_keys(data["company"])

        # Chỉ bỏ qua việc nhập address1 nếu skip_address là True
        if not skip_address:
            self.driver.find_element(By.ID, "address1").send_keys(data["address1"])

        self.driver.find_element(By.ID, "address2").send_keys(data["address2"])
        Select(self.driver.find_element(By.ID, "country")).select_by_value(data["country"])

        self.driver.find_element(By.ID, "state").send_keys(data["state"])
        self.driver.find_element(By.ID, "city").send_keys(data["city"])
        self.driver.find_element(By.ID, "zipcode").send_keys(data["zipcode"])
        self.driver.find_element(By.ID, "mobile_number").send_keys(data["mobile_number"])
        time.sleep(1)

    def _handle_ad(self):
        """Hàm xử lý quảng cáo nếu có."""
        try:
            # Chờ và bỏ qua quảng cáo nếu có
            iframe = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//iframe[starts-with(@id, 'aswift_')] | //iframe[starts-with(@id, 'ad_iframe')]"))
            )
            self.driver.switch_to.frame(iframe)
            # Tìm iframe con nếu có
            try:
                inner_iframe = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "ad_iframe")))
                self.driver.switch_to.frame(inner_iframe)
            except:
                pass  # Bỏ qua nếu không có iframe con

            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'dismiss-button'))).click()
        except:
            pass  # Bỏ qua nếu không có quảng cáo hoặc không click được
        finally:
            self.driver.switch_to.default_content()  # Luôn quay về nội dung chính

    # --- Các Test Case ---

    def test_tc01_successful_registration(self):
        """REG_TC01: Kiểm tra luồng đăng ký thành công."""
        # TẠO EMAIL ĐỘNG VÀ DUY NHẤT CHO MỖI LẦN CHẠY
        unique_timestamp = int(time.time())
        test_email = f"nguyenvan.an.{unique_timestamp}@vng.com.vn"
        print(f"\n[TC01] Sử dụng email động: {test_email}")

        user_data = {
            "password": "AnNguyen#VNG25", "first_name": "An", "last_name": "Nguyen Van",
            "company": "VNG Corporation", "address1": "Tân Thuận Đông, Quận 7", "address2": "Quận Phú Nhuận",
            "country": "United States", "state": "California", "city": "Los Angeles",
            "zipcode": "90210", "mobile_number": "0903123456"
        }

        self._start_signup_step("Nguyễn Văn An", test_email)
        self._fill_account_details_step(user_data)
        self.driver.find_element(By.XPATH, "//button[text()='Create Account']").click()

        success_message = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']")))
        assert success_message.is_displayed(), "Thông báo 'Account Created!' không hiển thị."

        continue_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Continue']")))
        continue_button.click()

        self._handle_ad()

        delete_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/delete_account']")))
        delete_button.click()

        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Deleted!']")))

    def test_tc02_register_with_existing_email(self):
        """REG_TC02: Kiểm tra đăng ký với email đã tồn tại."""
        # TẠO EMAIL ĐỘNG ĐỂ CHẮC CHẮN NÓ LÀ MỚI
        unique_timestamp = int(time.time())
        email_that_will_exist = f"existing.user.{unique_timestamp}@vng.com.vn"
        print(f"\n[TC02] Sử dụng email động: {email_that_will_exist}")

        user_data = {
            "password": "AnNguyen#VNG25", "first_name": "An", "last_name": "Nguyen Van",
            "company": "VNG Corporation", "address1": "Tân Thuận Đông, Quận 7", "address2": "Quận Phú Nhuận",
            "country": "United States", "state": "California", "city": "Los Angeles",
            "zipcode": "90210", "mobile_number": "0903123456"
        }

        # Bước 1: Tạo tài khoản lần đầu tiên để đảm bảo nó tồn tại
        self._start_signup_step("Nguyễn Văn An", email_that_will_exist)
        self._fill_account_details_step(user_data)
        self.driver.find_element(By.XPATH, "//button[text()='Create Account']").click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']")))
        self.driver.find_element(By.XPATH, "//a[text()='Continue']").click()
        self._handle_ad()

        # Bước 2: Đăng xuất ra
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/logout']"))).click()

        # Bước 3: Quay lại trang đăng ký và cố gắng đăng ký lại với cùng email đó
        self.wait.until(EC.visibility_of_element_located((By.NAME, "name")))
        self._start_signup_step("Người Dùng Khác", email_that_will_exist)

        # Bước 4: Xác thực thông báo lỗi
        error_message = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Email Address already exist!')]")))
        assert error_message.is_displayed(), "Không hiển thị thông báo email đã tồn tại."

    def test_tc03_empty_name(self):
        """REG_TC03: Kiểm tra validation khi để trống Tên nhưng điền Email."""
        initial_url = self.driver.current_url
        self._start_signup_step("", "nguyenvan.an1990@vng.com.vn")
        after_click_url = self.driver.current_url
        assert after_click_url == initial_url, "Trang đã bị chuyển hướng khi Tên để trống."

    def test_tc04_empty_email(self):
        """REG_TC04: Kiểm tra validation khi để trống Email nhưng điền Tên."""
        initial_url = self.driver.current_url
        self._start_signup_step("Nguyễn Văn An", "")
        after_click_url = self.driver.current_url
        assert after_click_url == initial_url, "Trang đã bị chuyển hướng khi Email để trống."

    def test_tc05_invalid_email_format(self):
        """REG_TC05: Kiểm tra validation khi email sai định dạng (thiếu @)."""
        initial_url = self.driver.current_url
        invalid_email = "nguyenvan.an.vng.com.vn"
        self._start_signup_step("Nguyễn Văn An", invalid_email)
        after_click_url = self.driver.current_url
        assert after_click_url == initial_url, "Trang đã bị chuyển hướng khi email sai định dạng."

    def test_tc06_empty_required_field_on_details_page(self):
        """REG_TC06: Kiểm tra validation khi để trống trường Address ở trang chi tiết."""
        unique_timestamp = int(time.time())
        test_email = f"test-tc06-{unique_timestamp}@vng.com.vn"
        print(f"\n[TC06] Sử dụng email động: {test_email}")

        user_data = {
            "password": "AnNguyen#VNG25", "first_name": "An", "last_name": "Nguyen Van",
            "company": "VNG Corporation", "address1": "",  # Dữ liệu trống cho Address
            "address2": "Quận Phú Nhuận",
            "country": "United States", "state": "California", "city": "Los Angeles",
            "zipcode": "90210", "mobile_number": "0903123456"
        }

        self._start_signup_step("Nguyễn Văn An", test_email)

        # Lưu URL trước khi điền form và click
        initial_url = self.driver.current_url
        self._fill_account_details_step(user_data, skip_address=True)
        self.driver.find_element(By.XPATH, "//button[text()='Create Account']").click()

        after_click_url = self.driver.current_url
        assert after_click_url == initial_url, "Trang đã bị chuyển hướng khi trường Address bắt buộc để trống."

    def test_tc07_email_field_is_disabled_on_details_page(self):
        """REG_TC07: Kiểm tra trường Email bị vô hiệu hóa ở trang chi tiết."""
        unique_timestamp = int(time.time())
        test_email = f"test-tc07-{unique_timestamp}@vng.com.vn"
        print(f"\n[TC07] Sử dụng email động: {test_email}")

        self._start_signup_step("Nguyễn Văn An", test_email)

        email_input_on_details_page = self.wait.until(EC.visibility_of_element_located((By.ID, "email")))

        # Kiểm tra thuộc tính 'disabled'
        is_disabled = email_input_on_details_page.get_attribute("disabled")
        assert is_disabled == "true", "Ô Email không bị vô hiệu hóa."

        # Kiểm tra giá trị của ô email
        email_value = email_input_on_details_page.get_attribute("value")
        assert email_value == test_email, "Giá trị email không khớp."