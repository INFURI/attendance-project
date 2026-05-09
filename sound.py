import winsound

def success_sound():
    winsound.Beep(1000, 200)

def error_sound():
    winsound.Beep(400, 400)