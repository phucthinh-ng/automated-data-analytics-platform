# 📊 Automated Data Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458?logo=pandas)](https://pandas.pydata.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Một nền tảng phân tích dữ liệu chuyên nghiệp được xây dựng bằng Python và Streamlit, giúp tự động hóa quy trình EDA, làm sạch dữ liệu thông minh và trực quan hóa Insights tương tác. Đây là dự án thực tế tập trung vào khả năng xử lý code thuần (code-heavy) để tối ưu hóa hiệu suất phân tích.

---

## 💡 Key Analytical Insights (Sự thật ngầm hiểu)
*Điểm khác biệt của dự án này là khả năng trích xuất thông tin có giá trị ngay lập tức từ dữ liệu rác:*

* **Phát hiện nghịch lý thu nhập:** Qua Ma trận tương quan, hệ thống xác định mối tương quan **0.85** giữa `Số năm kinh nghiệm` và `Lương`, khẳng định chính sách thâm niên của doanh nghiệp.
* **Tóm gọn Outliers:** Sử dụng thuật toán IQR để cô lập các điểm dữ liệu bất thường (ví dụ: mức lương 500M của cấp quản trị so với mức trung bình 25M của nhân viên).
* **Smart Imputation:** Hệ thống tự động phân biệt và áp dụng Mean/Median cho dữ liệu số và Mode cho dữ liệu chữ, đảm bảo tính toàn vẹn của tập dữ liệu sau khi làm sạch.

---

## ✨ Tính năng nổi bật

### 🧹 Làm sạch dữ liệu thông minh (Smart Cleaning)
* **Auto-reset Logic:** Hệ thống tự động làm mới trạng thái (Session State) khi upload file mới, đảm bảo tính nhất quán của dữ liệu.
* **Xử lý giá trị thiếu đa tầng:** * Định lượng: Imputation bằng Mean/Median để tránh lệch phân phối.
  * Định tính: Imputation bằng Mode cho các cột phân loại (Department, City).
* **Smart Type Conversion:** Tự động nhận diện và sửa lỗi định dạng (ví dụ: số bị lưu dưới dạng text).

### 📊 Trực quan hóa tương tác (Plotly-powered)
* **Correlation Heatmap:** Ma trận tương quan trực quan giúp tìm kiếm mối liên hệ giữa các biến số.
* **Interactive Charts:** Scatter, Bar, Box Plot với khả năng zoom, hover và lọc dữ liệu thời gian thực.
* **AI Chart Suggestion:** Gợi ý loại biểu đồ phù hợp nhất dựa trên đặc điểm của cột dữ liệu được chọn.

### 🎯 Phân tích thống kê nâng cao
* **IQR-based Outlier Detection:** Xác định ranh giới dữ liệu an toàn và liệt kê chi tiết các bản ghi ngoại lai.
* **Comprehensive Stats:** Cung cấp cái nhìn tổng thể về phân phối, độ lệch và các chỉ số đo lường trung tâm.

---

## 🛠️ Công nghệ sử dụng
* **Ngôn ngữ:** Python (Xử lý logic thuần code)
* **Thư viện chính:** Pandas, NumPy, Streamlit, Plotly, Seaborn.
* **Deployment:** Streamlit Cloud.

---

## 🚀 Cài đặt & Sử dụng

1. **Clone dự án:**
   ```bash
   git clone [https://github.com/phucthinh-ng/automated-data-analytics-platform.git](https://github.com/phucthinh-ng/automated-data-analytics-platform.git)
2. **Cài đặt môi trường:**
   ```bash
   pip install -r requirements.txt
3. **Khởi chạy ứng dụng:**
   ```bash
   streamlit run app.py
👤 Thông tin tác giả
Họ tên: Nguyễn Phúc Thịnh

Vị trí: Data Analyst / Developer

Kỹ năng: Python, DA, SQL

GitHub: phucthinh-ng
