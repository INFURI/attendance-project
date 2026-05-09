import cv2
import os
import time
from rfid_reader import get_uid
from uid_manager import add_user

#INPUT
person_name = input("Enter person name/ID: ").strip()

if not person_name:
    print("Invalid name")
    exit()

print("Now scan RFID card...")

#GET UID
uid = None
while not uid:
    uid = get_uid()

print("Scanned UID:", uid)

#SAVE UID
add_user(uid, person_name)

#DATASET SETUP
dataset_path = "dataset"
person_folder = os.path.join(dataset_path, person_name)

os.makedirs(person_folder, exist_ok=True)

#CAMERA
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible")
    exit()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0
max_images = 30

print("Press SPACE to start capturing faces...")

started = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=6,
        minSize=(80, 80)
    )

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))

        cv2.imshow("Face", face)

        if started and count < max_images:
            img_path = os.path.join(person_folder, f"{count}.jpg")
            cv2.imwrite(img_path, face)
            print(f"Saved {img_path}")
            count += 1
            time.sleep(0.2)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        started = True
        print("Capture started...")

    if key == ord('q'):
        break

    if count >= max_images:
        print("Capture complete.")
        break

cap.release()
cv2.destroyAllWindows()

print(f"[✔] Registration complete for {person_name}")