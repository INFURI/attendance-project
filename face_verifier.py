import cv2
import json

#LOAD MODEL
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

#LOAD LABEL MAP
with open("labels.json", "r") as f:
    label_map = json.load(f)

label_map = {int(k): v for k, v in label_map.items()}


def verify_face(face, expected_name):
    label, confidence = recognizer.predict(face)

    predicted_name = label_map[label]

    #  LBPH confidence 
    if predicted_name == expected_name and confidence < 90:
        return True, confidence, predicted_name

    return False, confidence, predicted_name