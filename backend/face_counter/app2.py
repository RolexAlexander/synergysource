import cv2
import numpy as np
from flask import Flask, render_template, Response
import logging

# Set up logging
logging.basicConfig(filename='people_count.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class YOLOFaceDetector:
    def __init__(self, weights_path, config_path, names_path):
        self.net = cv2.dnn.readNet(weights_path, config_path)
        self.layer_names = self.net.getLayerNames()
        try:
            self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        except TypeError:
            self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        with open(names_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def detect_faces(self, frame):
        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.7:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        if len(indices) == 0:
            return []

        if isinstance(indices[0], list) or isinstance(indices[0], np.ndarray):
            return [(boxes[i[0]], confidences[i[0]], class_ids[i[0]]) for i in indices]
        else:
            return [(boxes[i], confidences[i], class_ids[i]) for i in indices]

    def count_people(self, faces):
        person_class_id = self.classes.index('person')  # Assuming 'person' is the class name for people
        count = sum(1 for _, _, class_id in faces if class_id == person_class_id)
        return count

# Initialize the YOLOFaceDetector
# Initialize the YOLOFaceDetector
# Initialize the YOLOFaceDetector
detector = YOLOFaceDetector(
    weights_path='C:/Users/sm94c/Documents/Repositiories/innovation_project/synergysource/backend/face_counter/yolov3.weights',
    config_path='C:/Users/sm94c/Documents/Repositiories/innovation_project/synergysource/backend/face_counter/yolov3.cfg',
    names_path='C:/Users/sm94c/Documents/Repositiories/innovation_project/synergysource/backend/face_counter/coco.names'
)



def gen_frames():
    cap = cv2.VideoCapture(0)
    previous_count = None
    while True:
        success, frame = cap.read()
        if not success:
            break

        faces = detector.detect_faces(frame)
        current_count = detector.count_people(faces)
        
        if current_count != previous_count:
            logging.info(f"Number of people detected: {current_count}")
            previous_count = current_count

        for (box, confidence, class_id) in faces:
            x, y, w, h = box
            label = f"{detector.classes[class_id]}: {confidence:.2f}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
