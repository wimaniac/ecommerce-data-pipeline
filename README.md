# E-commerce ETL Data Pipeline �
Dự án sử dụng bộ dữ liệu nổi tiếng Online Retail II (nguồn: UCI Machine Learning Repository). Đây là bộ dữ liệu giao dịch thực tế của một doanh nghiệp bán lẻ trực tuyến (non-store online retail) có trụ sở tại Vương quốc Anh, chuyên bán các mặt hàng quà tặng độc đáo.

Thời gian dữ liệu: 01/12/2009 - 09/12/2011.

Đặc điểm: Bao gồm cả giao dịch bán buôn (B2B) và bán lẻ (B2C).

Kích thước: Khoảng 1 triệu dòng (rows) dữ liệu giao dịch.
## Tổng quan (Overview)
Dự án xây dựng pipeline dữ liệu tự động (ETL) để xử lý dữ liệu giao dịch bán lẻ (Online Retail II dataset), chuyển đổi dữ liệu thô thành mô hình **Star Schema** và lưu trữ vào Data Warehouse để phục vụ phân tích kinh doanh.

## Công nghệ sử dụng (Tech Stack)
* **Ngôn ngữ:** Python 3.9+
* **Xử lý dữ liệu:** Pandas, NumPy
* **Database:** SQLite (Demo), SQLAlchemy
* **Orchestration:** Python Scripts (Giả lập luồng Airflow)
* **IDE:** VS Code

## Kiến trúc dữ liệu (Architecture)
1.  **Extract:** Đọc dữ liệu từ file CSV thô.
2.  **Transform:**
    * Làm sạch dữ liệu (Xử lý Null, loại bỏ đơn hàng hủy/trả lại).
    * Chuyển đổi kiểu dữ liệu (Datetime, Int).
    * Mô hình hóa dữ liệu thành các bảng Fact/Dimension (Fact_Sales, Dim_Customer, Dim_Product).
3.  **Load:** Tải dữ liệu sạch vào Data Warehouse (SQLite).

## Hướng dẫn chạy (How to run)

1.  **Cài đặt thư viện:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Chạy Pipeline:**
    ```bash
    python src/pipeline.py
    ```

3.  **Xem kết quả phân tích:**
    Mở file `src/analysis.py` hoặc `notebooks/exploration.ipynb`.

