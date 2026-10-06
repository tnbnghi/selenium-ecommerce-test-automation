# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Dữ liệu dùng chung ---
BASE_URL = "https://automationexercise.com/"

class TestLogin:
    """
    Nhóm các test case cho chức năng Đăng nhập.
    """
    def setup_method(self, method):
        """Chạy trước mỗi test case. Khởi tạo trình duyệt."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(BASE_URL)
        time.sleep(1)
        # Đi đến trang đăng nhập
        self.driver.find_element(By.XPATH, "//a[@href='/login']").click()
        time.sleep(1)

    def teardown_method(self, method):
        """Chạy sau mỗi test case. Đóng trình duyệt."""
        time.sleep(3)
        self.driver.quit()

    # --- Các Test Case ---

    def test_tc08_successful_login_and_logout(self):
        # ... (giữ nguyên mã nguồn của TC08) ...
        valid_email = "nguyenvan.an1990@vng.com.vn"
        valid_password = "AnNguyen#VNG25"
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(valid_email)
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(valid_password)
        self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        logged_in_user = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Logged in as')]")))
        assert "Nguyễn Văn An" in logged_in_user.text
        self.driver.find_element(By.XPATH, "//a[@href='/logout']").click()
        login_form = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='Login to your account']")))
        assert login_form.is_displayed()

    def test_tc09_login_with_incorrect_password(self):
        # ... (giữ nguyên mã nguồn của TC09) ...
        valid_email = "nguyenvan.an1990@vng.com.vn"
        invalid_password = "WrongPassword123"
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(valid_email)
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(invalid_password)
        self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        error_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'incorrect!')]")))
        assert "Your email or password is incorrect!" in error_message.text

    def test_tc10_login_with_nonexistent_email(self):
        # ... (giữ nguyên mã nguồn của TC10) ...
        non_existent_email = "email.khong.ton.tai@vng.com.vn"
        any_password = "AnyPassword123"
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(non_existent_email)
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(any_password)
        self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        error_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'incorrect!')]")))
        assert "Your email or password is incorrect!" in error_message.text

    def test_tc11_login_with_empty_email(self):
        """Kiểm tra validation khi để trống email."""
        initial_url = self.driver.current_url
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys("AnyPassword123")
        self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        time.sleep(1) # Chờ để xem có chuyển trang không
        after_click_url = self.driver.current_url
        assert initial_url == after_click_url # Khẳng định trang không reload/chuyển hướng

    def test_tc12_login_with_empty_password(self):
        """Kiểm tra validation khi để trống mật khẩu."""
        initial_url = self.driver.current_url
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys("nguyenvan.an1990@vng.com.vn")
        self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        time.sleep(1)
        after_click_url = self.driver.current_url
        assert initial_url == after_click_url

    def test_tc13_login_with_invalid_email_format(self):
        """Kiểm tra validation khi email sai định dạng."""
        initial_url = self.driver.current_url
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys("nguyenvan.an.vng.com.vn")
        self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        time.sleep(1)
        after_click_url = self.driver.current_url
        assert initial_url == after_click_url

    def test_tc14_login_with_case_sensitive_email(self):
        """Kiểm tra đăng nhập với email phân biệt chữ hoa/thường."""
        case_sensitive_email = "Nguyenvan.an1990@vng.com.vn" # Chữ N viết hoa
        valid_password = "AnNguyen#VNG25"
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(case_sensitive_email)
        self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(valid_password)
        self.driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        error_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'incorrect!')]")))
        assert "Your email or password is incorrect!" in error_message.text