import cv2
import json
import os
import numpy as np
from collections import deque, Counter

#LOAD FACE DETECTOR
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

#LOAD LBPH MODEL
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

#LOAD LABEL MAP
with open("labels.json", "r") as f:
    label_map = json.load(f)

label_map = {int(k): v for k, v in label_map.items()}

#LOAD TEMPLATES (FALLBACK)
dataset_path = "dataset"
templates = []
template_labels = []

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_folder):
        continue

    for img_name in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        img = cv2.resize(img, (100, 100))
        templates.append(img)
        template_labels.append(person_name)

templates = np.array(templates)
template_labels = np.array(template_labels)

# ---------- TEMPLATE FALLBACK ----------
def template_verify(face_roi):
    best_score = float('inf')
    best_label = "Unknown"

    for i, template in enumerate(templates):
        diff = np.mean((face_roi.astype("float") - template.astype("float")) ** 2)
        if diff < best_score:
            best_score = diff
            best_label = template_labels[i]

    if best_score < 2000:
        return best_label
    return "Unknown"

#TEMPORAL SMOOTHING BUFFER
history = deque(maxlen=5)

#MAIN RECOGNITION FUNCTION
def recognize_face(frame):
    global history

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=6,
        minSize=(80, 80)
    )

    results = []

    for (x, y, w, h) in faces:
        # Padding
        pad = 10
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(gray.shape[1], x + w + pad)
        y2 = min(gray.shape[0], y + h + pad)

        face = gray[y1:y2, x1:x2]
        face = cv2.resize(face, (100, 100))
        face = cv2.equalizeHist(face)

        label, confidence = recognizer.predict(face)

        # Decision logic
        if confidence < 80:
            name = label_map[label]
        elif confidence < 100:
            name = template_verify(face)
        else:
            name = "Unknown"

        # TEMPORAL SMOOTHING 
        history.append((name, confidence))

        # Majority voting
        names = [h[0] for h in history]
        most_common = Counter(names).most_common(1)[0][0]

        # Average confidence
        avg_conf = sum([h[1] for h in history]) / len(history)

        results.append((most_common, avg_conf, (x, y, w, h)))

    return results


# TEST MODE 
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    print("Stable recognition running... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = recognize_face(frame)

        for (name, confidence, (x, y, w, h)) in results:

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

            cv2.putText(frame, f"{name} ({int(confidence)})",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (255, 0, 0), 2)

            print(f"Stable: {name}, Avg Confidence: {confidence:.2f}")

        cv2.imshow("Stable Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()