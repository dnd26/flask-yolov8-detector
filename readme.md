# Flask YOLOv8 Image Detector

Ứng dụng web đơn giản sử dụng **Flask**, **YOLOv8** để phát hiện đối tượng trong ảnh.

## Tính năng
- Giao diện upload ảnh trực quan.
- Xem ảnh đã chọn trước khi phát hiện.
- Dùng model YOLOv8 để detect và hiển thị kết quả.
- Sau khi bấm Detect, chỉ hiển thị ảnh kết quả (không hiển thị lại ảnh gốc người dùng chọn).

## Cài đặt
1. Clone dự án:
git clone https://github.com/dnd26/flask-yolov8-detector.git  cd flask-yolov8-detector
3. Tạo môi trường ảo và cài dependencies
python -m venv venv
source venv/bin/activate   # Trên macOS/Linux
venv\Scripts\activate      # Trên Windows
pip install -r requirements.txt

4. Chạy ứng dụng
python app.py

5. Truy cập
http://127.0.0.1:5000
