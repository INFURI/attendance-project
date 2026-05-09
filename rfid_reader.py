import serial

ser = serial.Serial("COM3", 9600)


def get_uid():
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode(errors='ignore').strip()
            if data.startswith("UID:"):
                return data.replace("UID:", "")
        except:
            return None
    return None