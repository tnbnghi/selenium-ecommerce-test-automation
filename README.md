# Kiểm thử tự động E-Commerce với Selenium WebDriver

**Môn Kỹ thuật Kiểm thử Phần mềm** — Đồ án cá nhân, điểm 7.7/10

---

## 📝 Tổng quan

Đồ án nghiên cứu và ứng dụng **Selenium WebDriver** để xây dựng bộ kiểm thử tự động cho 3 luồng nghiệp vụ cốt lõi của một website thương mại điện tử: **đăng ký tài khoản**, **đăng nhập**, và **mua sắm** (tìm kiếm, giỏ hàng, thanh toán), trên website thực hành [automationexercise.com](https://automationexercise.com/). Đồ án cũng so sánh Selenium với Cypress và đề xuất hướng cải tiến cho một hệ thống kiểm thử chuyên nghiệp hơn.

## ✅ Phạm vi kiểm thử

- **Đăng ký tài khoản** (7 test case): đăng ký thành công, email đã tồn tại, để trống trường bắt buộc, sai định dạng email, email bị khóa chỉnh sửa ở bước 2.
- **Đăng nhập** (7 test case): đăng nhập/đăng xuất thành công, sai mật khẩu, email không tồn tại, để trống trường, sai định dạng, email phân biệt chữ hoa/thường.
- **Mua sắm** (4 test case): tìm kiếm sản phẩm (có/không kết quả), xóa sản phẩm khỏi giỏ hàng, luồng thanh toán hoàn chỉnh.

**Kết quả:** 18/18 test case đạt PASS (100%).

## 🛠️ Công nghệ sử dụng

- **Ngôn ngữ:** Python
- **Framework kiểm thử:** Selenium WebDriver, PyTest
- **Kỹ thuật áp dụng:** Explicit Wait (`WebDriverWait`), JavaScript executor click (xử lý quảng cáo che khuất phần tử), sinh dữ liệu test động (email theo timestamp) để tránh trùng lặp giữa các lần chạy.

## 🚀 Hướng dẫn chạy thử

### Yêu cầu

- Python 3.8+
- Google Chrome (trình duyệt đích của bộ test)

### Các bước

```bash
# 1. Tải mã nguồn về máy
git clone https://github.com/tnbnghi/selenium-ecommerce-test-automation.git
cd selenium-ecommerce-test-automation

# 2. (Khuyến khích) Tạo và kích hoạt môi trường ảo
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Cài đặt thư viện
pip install -r requirements.txt

# 4. Chạy toàn bộ bộ test
pytest tests/ -v
```

Selenium 4+ tự động tải ChromeDriver phù hợp, không cần cài thủ công.

## 📊 So sánh Selenium vs Cypress & Đề xuất cải tiến

Đồ án đầy đủ (báo cáo PDF) phân tích chi tiết ưu/nhược điểm của Selenium, so sánh với Cypress trên các tiêu chí chi phí, hỗ trợ trình duyệt, tốc độ thực thi và khả năng báo cáo, đồng thời đề xuất 3 hướng cải tiến: áp dụng **Page Object Model (POM)**, triển khai **Selenium Grid** để chạy song song, và tích hợp vào quy trình **CI/CD**.

## 📂 Cấu trúc thư mục

```
selenium-ecommerce-test-automation/
├── tests/
│   ├── test_dangky.py      # Test case đăng ký (REG_TC01–07)
│   ├── test_dangnhap.py    # Test case đăng nhập (LOG_TC08–14)
│   └── test_muasam.py      # Test case mua sắm (SEARCH/CART/CHECKOUT)
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔗 Repository

[https://github.com/tnbnghi/selenium-ecommerce-test-automation](https://github.com/tnbnghi/selenium-ecommerce-test-automation)
