import cv2
from ultralytics import YOLO
from flask import Flask, render_template, Response, jsonify
import threading
import time

# Ayarları danger_threshold.py dosyasından içe aktar
from danger_threshold import (
    TEHLIKELI_NESNELER,
    DEFAULT_CONF_THRESHOLD,
    KNIFE_CONF_THRESHOLD,
    PERSON_DANGER_SCORE,
    DANGEROUS_OBJECT_SCORE,
    MAX_DANGER_PERCENTAGE
)

app = Flask(__name__)

model_path = 'models/yolov8n.pt'
try:
    model = YOLO(model_path)
except Exception as e:
    print(f"YOLO modeli yüklenirken bir hata oluştu: {e}")
    print(f"Lütfen '{model_path}' yolunda model dosyasının olduğundan emin olun.")
    exit()

current_frame = None
detection_results = {}
danger_percentage = 0
display_window_active = True

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera açılamadı. Lütfen kamera bağlantısını kontrol edin veya farklı bir kamera indexi deneyin.")
    exit()

def process_frame():
    global current_frame, detection_results, danger_percentage, display_window_active

    cv2.namedWindow("Canli Goruntu ve Tespit", cv2.WINDOW_NORMAL)

    while display_window_active:
        ret, frame = cap.read()
        if not ret:
            print("Kamera akışından kare alınamadı.")
            break

        results = model(frame, conf=min(DEFAULT_CONF_THRESHOLD, KNIFE_CONF_THRESHOLD) - 0.01, stream=True)
        
        detected_objects_count = {}
        person_count = 0
        has_dangerous_object = False
        
        annotated_frame = frame.copy()

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])

                if class_name == 'knife':
                    if confidence < KNIFE_CONF_THRESHOLD:
                        continue
                elif confidence < DEFAULT_CONF_THRESHOLD:
                    continue
                
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                label = f"{class_name}: {confidence:.2f}"
                cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                detected_objects_count[class_name] = detected_objects_count.get(class_name, 0) + 1
                if class_name == 'person':
                    person_count += 1
                
                if class_name in TEHLIKELI_NESNELER:
                    has_dangerous_object = True
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(annotated_frame, "TEHLIKELI!", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        calculated_danger_percentage = 0
        if person_count > 0:
            calculated_danger_percentage += person_count * PERSON_DANGER_SCORE
        if has_dangerous_object:
            calculated_danger_percentage += DANGEROUS_OBJECT_SCORE

        danger_percentage = min(MAX_DANGER_PERCENTAGE, calculated_danger_percentage)

        detection_results = {
            "nesneler": detected_objects_count,
            "insan_sayisi": person_count
        }

        cv2.putText(annotated_frame, f"Tehlike Orani: %{danger_percentage:.2f}", (annotated_frame.shape[1] - 300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        cv2.imshow("Canli Goruntu ve Tespit", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            display_window_active = False
            break

        ret, jpeg = cv2.imencode('.jpg', annotated_frame)
        current_frame = jpeg.tobytes()

        time.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()


@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global current_frame
    while True:
        if current_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
        else:
            time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data_feed')
def data_feed():
    global detection_results, danger_percentage
    return jsonify({
        "detection_results": detection_results,
        "danger_percentage": danger_percentage
    })

if __name__ == '__main__':
    frame_processor_thread = threading.Thread(target=process_frame)
    frame_processor_thread.daemon = True
    frame_processor_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=False)
