from flask import Flask, render_template, request, url_for
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import cv2

# Config
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
RESULT_FOLDER = BASE_DIR / 'static' / 'results'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXT = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_folder='static')

# Load model (change to yolov8m.pt / yolov8l.pt for better accuracy)
MODEL = YOLO('yolov8n.pt')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_image_url = None
    result_image_url = None
    detections = []

    if request.method == 'POST':
        file = request.files.get('image')
        if not file or file.filename == '':
            return render_template('index.html', error='No file uploaded')

        if not allowed_file(file.filename):
            return render_template('index.html', error='Unsupported file type')

        filename = secure_filename(file.filename)
        save_path = UPLOAD_FOLDER / filename
        file.save(save_path)

        # Run inference (tweak imgsz, conf, iou as needed)
        results = MODEL.predict(source=str(save_path), imgsz=800, conf=0.5, iou=0.45, device='cpu')
        res = results[0]

        # Create annotated image from result.plot()
        annotated = res.plot()  # RGB ndarray
        annotated_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
        out_name = f'det_{filename}'
        out_path = RESULT_FOLDER / out_name
        cv2.imwrite(str(out_path), annotated_bgr)

        # Collect detections for display
        if hasattr(res, 'boxes') and res.boxes is not None and len(res.boxes) > 0:
            for box in res.boxes:
                cls_id = int(box.cls.cpu().numpy())
                conf = float(box.conf.cpu().numpy())
                name = MODEL.names.get(cls_id, str(cls_id))
                detections.append({'class': name, 'conf': round(conf, 3)})

        uploaded_image_url = url_for('static', filename=f'uploads/{filename}')
        result_image_url = url_for('static', filename=f'results/{out_name}')

    return render_template('index.html', uploaded_image=uploaded_image_url, result_image=result_image_url, detections=detections)

if __name__ == '__main__':
    # Turn off the auto-reloader to avoid repeated restarts while loading torch models
    app.run(debug=True, use_reloader=False)