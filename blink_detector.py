import cv2

eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

blink_state = {
    "eyes_detected": True,
    "blink_detected": False,
    "counter": 0
}

def detect_blink(face_gray):
    global blink_state

    eyes = eye_cascade.detectMultiScale(face_gray, 1.2, 5)

    # Eyes present
    if len(eyes) >= 1:
        if not blink_state["eyes_detected"]:
            # Eyes came back → blink completed
            blink_state["blink_detected"] = True
        blink_state["eyes_detected"] = True

    else:
        # Eyes not detected
        blink_state["eyes_detected"] = False

    return blink_state["blink_detected"]


def reset_blink():
    global blink_state
    blink_state["blink_detected"] = False