import pandas as pd
from pathlib import Path
import logging

# Sử dụng pathlib để quản lý đường dẫn một cách hiện đại và nhất quán
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw_data" / "online_retail_II.csv"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed_data"


def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Thực hiện các bước làm sạch dữ liệu."""
    logging.info("Bắt đầu làm sạch dữ liệu...")

    # Loại bỏ các dòng không có Customer ID (vì không xác định được khách hàng)
    df.dropna(subset=['Customer ID'], inplace=True)

    # Loại bỏ các đơn hàng bị hủy (InvoiceNo bắt đầu bằng chữ 'C')
    df = df[~df['Invoice'].astype(str).str.startswith('C')]

    # Loại bỏ Quantity và Price âm hoặc bằng 0
    df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

    # Chuyển đổi Customer ID về kiểu số nguyên (int) thay vì float
    df['Customer ID'] = df['Customer ID'].astype(int)

    # Chuyển đổi InvoiceDate sang kiểu datetime chuẩn
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Tạo cột mới: TotalAmount = Quantity * Price
    df['TotalAmount'] = df['Quantity'] * df['Price']

    logging.info(f"Dữ liệu sau khi làm sạch có {df.shape[0]} dòng.")
    return df


def _create_dimensions_and_facts(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Tách DataFrame đã làm sạch thành các bảng Dimension và Fact."""
    logging.info("Bắt đầu tạo các bảng Dimension và Fact (Star Schema)...")

    # --- Bảng DIM_CUSTOMER ---
    # Lấy các cột liên quan đến khách hàng và loại bỏ trùng lặp
    dim_customer = df[['Customer ID', 'Country']].drop_duplicates()

    # --- Bảng DIM_PRODUCT ---
    # Lấy các cột sản phẩm và loại bỏ trùng lặp
    dim_product = df[['StockCode', 'Description']].drop_duplicates()
    # Lưu ý: Một StockCode có thể có nhiều Description khác nhau do nhập liệu,
    dim_product = dim_product.groupby('StockCode').first().reset_index()

    # --- Bảng FACT_SALES ---
    # Bảng này chứa các khóa ngoại (Foreign Keys) và dữ liệu đo lường (Measures)
    fact_sales = df[['Invoice', 'StockCode', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'TotalAmount']]
    
    logging.info(f"Đã tạo dim_customer với {len(dim_customer)} dòng.")
    logging.info(f"Đã tạo dim_product với {len(dim_product)} dòng.")
    logging.info(f"Đã tạo fact_sales với {len(fact_sales)} dòng.")
    
    return dim_customer, dim_product, fact_sales


def transform_data():
    """
    Hàm chính điều phối quy trình Transform:
    1. Đọc dữ liệu thô.
    2. Làm sạch dữ liệu.
    3. Mô hình hóa thành Star Schema.
    4. Lưu các bảng đã xử lý.
    """
    logging.info("--- Bắt đầu quy trình Transform ---")

    # 1. Đọc dữ liệu thô
    logging.info(f"Đang đọc dữ liệu từ: {RAW_DATA_PATH}")
    try:
        # encoding='latin1' hoặc 'ISO-8859-1' thường cần cho dataset này
        df = pd.read_csv(RAW_DATA_PATH, encoding='ISO-8859-1')
    except FileNotFoundError:
        logging.error(f"LỖI: Không tìm thấy tệp dữ liệu thô tại '{RAW_DATA_PATH}'. Vui lòng kiểm tra lại đường dẫn.")
        return

    # 2. Làm sạch dữ liệu
    df_cleaned = _clean_data(df)

    # 3. Mô hình hóa dữ liệu
    dim_customer, dim_product, fact_sales = _create_dimensions_and_facts(df_cleaned)

    # 4. Lưu dữ liệu đã xử lý
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    dim_customer.to_csv(PROCESSED_DATA_DIR / 'dim_customer.csv', index=False)
    dim_product.to_csv(PROCESSED_DATA_DIR / 'dim_product.csv', index=False)
    fact_sales.to_csv(PROCESSED_DATA_DIR / 'fact_sales.csv', index=False)
    
    logging.info(f"--- Hoàn thành! Dữ liệu sạch đã được lưu tại thư mục: {PROCESSED_DATA_DIR} ---")

if __name__ == '__main__':
    transform_data()