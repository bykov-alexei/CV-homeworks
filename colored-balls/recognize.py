import numpy as np
import cv2

cap = cv2.VideoCapture(0)

colors = {
    'red': [np.array([0, 0, 109]), np.array([65, 62, 255])],
    'blue': [np.array([144, 126, 0]), np.array([255, 230, 77])],
    'green': [np.array([57, 144, 0]), np.array([130, 225, 132])],
}

def find_ball(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame, lower, upper)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (curr_x, curr_y), radii = cv2.minEnclosingCircle(c)
        if radii > 10:
            return (int(curr_x), int(curr_y)), int(radii)

while True:
    ret, frame = cap.read()
    blurred = cv2.GaussianBlur(frame, (15, 15), 0)

    balls = {}

    for colorname, color in colors.items():
        ball = find_ball(blurred, color[0], color[1])
        if ball:
            cv2.circle(frame, ball[0], ball[1], (0, 255, 255), 2)
            balls[colorname] = ball
    
    s = sorted(balls.items(), key=lambda x: x[1][0])
    print([el[0] for el in s])

    cv2.imshow('frame', frame)
    # cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break