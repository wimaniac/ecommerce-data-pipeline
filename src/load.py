import pandas as pd
from sqlalchemy import create_engine
import os

PROCESSED_DATA_DIR = 'data/processed_data'
# Tạo một file database tên là 'warehouse.db' nằm trong thư mục data
DB_CONNECTION_STRING = 'sqlite:///data/warehouse.db'
def load_data():
    print("--- Bắt đầu quy trình Load ---")
    
    # 1. Tạo kết nối đến Database (Data Warehouse giả lập)
    print(f"Đang kết nối đến Database: {DB_CONNECTION_STRING}")
    engine = create_engine(DB_CONNECTION_STRING)
    
    # Danh sách các file cần load và tên bảng tương ứng
    files_to_load = {
        'dim_customer.csv': 'dim_customer',
        'dim_product.csv': 'dim_product',
        'fact_sales.csv': 'fact_sales'
    }

    # 2. Lặp qua từng file và tải vào DB
    for file_name, table_name in files_to_load.items():
        file_path = os.path.join(PROCESSED_DATA_DIR, file_name)
        
        if os.path.exists(file_path):
            print(f"Đang tải {file_name} vào bảng '{table_name}'...")
            
            # Đọc file CSV
            df = pd.read_csv(file_path)
            
            # Tải vào SQL
            # if_exists='replace': Nếu bảng đã có thì xóa đi tạo lại (phù hợp chạy test nhiều lần)
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            
            print(f"-> Đã tải thành công {len(df)} dòng vào bảng {table_name}.")
        else:
            print(f"CẢNH BÁO: Không tìm thấy file {file_path}")

    print("--- Hoàn thành! Dữ liệu đã nằm trong Data Warehouse (warehouse.db) ---")

if __name__ == '__main__':
    load_data()