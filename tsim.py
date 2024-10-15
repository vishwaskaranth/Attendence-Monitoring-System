import cv2

try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("LBPH Face Recognizer created successfully!")
except AttributeError as e:
    print("Error: cv2.face module is not available.")
    print(e)
