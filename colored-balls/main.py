import cv2
import numpy as np
from skimage import filters

def set_upper(i):
    global colorUpper 
    def func(x):
        colorUpper[i] = x
    return func

def set_lower(i):
    global colorLower
    def func(x):
        colorLower[i] = x
    return func

cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)

cv2.createTrackbar("L hue", 'Mask', 0, 255, set_lower(0))
cv2.createTrackbar("U hue", 'Mask', 0, 255, set_upper(0))

cv2.createTrackbar("L sat", 'Mask', 0, 255, set_lower(1))
cv2.createTrackbar("U sat", 'Mask', 0, 255, set_upper(1))

cv2.createTrackbar("L val", 'Mask', 0, 255, set_lower(2))
cv2.createTrackbar("U val", 'Mask', 0, 255, set_upper(2))

cap = cv2.VideoCapture(0)

colorLower = np.array([0, 0, 0], dtype="uint8")
colorUpper = np.array([255, 255, 255], dtype="uint8")

while True:
    ret, frame = cap.read()
    blurred = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame, colorLower, colorUpper)
    mask = cv2.dilate(mask, None, iterations=2)

    cv2.imshow('frame', frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
