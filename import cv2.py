import cv2

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) == ord('q'):
        break