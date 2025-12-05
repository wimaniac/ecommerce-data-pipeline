import logging
import time
from transform import transform_data
from load import load_data

# --- CẤU HÌNH LOGGING ---
# Logging giúp bạn theo dõi quá trình chạy chuyên nghiệp hơn dùng print()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"), # Lưu log vào file
        logging.StreamHandler()              # In log ra màn hình
    ]
)

def run_pipeline():
    logging.info("=======================================")
    logging.info("BẮT ĐẦU CHẠY DATA PIPELINE E-COMMERCE")
    logging.info("=======================================")
    
    start_time = time.time()

    try:
        # Bước 1: Transform (Vì bước Extract là tải file thủ công nên ta bắt đầu từ đây)
        logging.info(">>> Bước 1: Bắt đầu Transform dữ liệu...")
        transform_data()
        logging.info("<<< Bước 1: Hoàn thành Transform.")

        # Bước 2: Load
        logging.info(">>> Bước 2: Bắt đầu Load dữ liệu vào Warehouse...")
        load_data()
        logging.info("<<< Bước 2: Hoàn thành Load.")

    except Exception as e:
        logging.error(f"!!! PIPELINE THẤT BẠI: Có lỗi xảy ra: {e}")
        # Ở môi trường thật, đoạn này sẽ gửi email cảnh báo cho kỹ sư
    
    finally:
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"--- Pipeline kết thúc sau {duration:.2f} giây ---")

if __name__ == '__main__':
    run_pipeline()