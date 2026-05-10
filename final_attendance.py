import cv2
import time
from rfid_reader import get_uid
from attendance import mark_attendance
from face_verifier import verify_face
from uid_manager import load_uid_map
from blink_detector import detect_blink, reset_blink
from sound import success_sound, error_sound



uid_to_name = load_uid_map()


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


cap = cv2.VideoCapture(0)


mode = "IDLE"
current_uid = None
uid_time = 0
uid_timeout = 5

last_mark_time = 0
cooldown = 5

print("System Ready. Scan RFID card...")

while True:

    
    
    uid = get_uid()
    if uid and uid in uid_to_name:
        current_uid = uid
        uid_time = time.time()
        mode = "WAIT_FACE"
        print(f"Card scanned for {uid_to_name[uid]}. Show face.")

    
    
    if mode == "WAIT_FACE" and (time.time() - uid_time > uid_timeout):
        print("Timeout. Please scan again.")
        mode = "IDLE"
        current_uid = None
        reset_blink()

   
    
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    status_text = "Scan RFID"

   
    
    if mode == "WAIT_FACE":

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=6,
            minSize=(80, 80)
        )

        expected_name = uid_to_name[current_uid]

        for (x, y, w, h) in faces:

           
            pad = 20
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(gray.shape[1], x + w + pad)
            y2 = min(gray.shape[0], y + h + pad)

            face = gray[y1:y2, x1:x2]
            face = cv2.resize(face, (100, 100))

            
            face = cv2.equalizeHist(face)

           
            match, confidence, predicted_name = verify_face(face, expected_name)

           
            blink_ok = detect_blink(face)

           
            print(f"Predicted: {predicted_name}, Expected: {expected_name}, Confidence: {confidence:.2f}, Blink: {blink_ok}")

           
            if match and blink_ok:

                if time.time() - last_mark_time > cooldown:
                    success = mark_attendance(expected_name)

                    if success:
                        status_text = "Attendance Marked"
                        success_sound()

                        last_mark_time = time.time()
                        reset_blink()

                        
                        time.sleep(1)
                        mode = "IDLE"
                        current_uid = None
                    else:
                        status_text = "Already Marked"

                else:
                    status_text = "Wait..."

                color = (0, 255, 0)

            else:
                status_text = "Blink Required / Mismatch"
                error_sound()
                color = (0, 0, 255)

            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

            cv2.putText(frame,
                        f"{predicted_name} ({int(confidence)})",
                        (x, y-30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 0),
                        2)

          
            cv2.putText(frame,
                        f"Blink: {'YES' if blink_ok else 'NO'}",
                        (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 0),
                        2)

   
    if mode == "IDLE":
        status_text = "Scan RFID"
    elif mode == "WAIT_FACE":
        status_text = "Show Face + Blink"

    cv2.putText(frame,
                status_text,
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
