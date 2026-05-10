import cv2
import os
import numpy as np

dataset_path = "dataset"

faces = []
labels = []
label_map = {}
current_label = 0

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_folder):
        continue

    label_map[current_label] = person_name

    for img_name in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        faces.append(img)
        labels.append(current_label)

    current_label += 1

faces = np.array(faces)
labels = np.array(labels)

print("Training data ready")
print("Labels:", label_map)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, labels)

recognizer.save("face_model.yml")

import json
with open("labels.json", "w") as f:
    json.dump(label_map, f)
print("Model trained and saved as face_model.yml")
print("Labels saved as labels.json")





