import cv2
import utils
from setup import *

dragActive = 0
centerBox = 100, 100
sizeBox = 50
colorBox = (155, 0, 155)

while CAPTURE.isOpened():
    success, image = CAPTURE.read()
    if success:
        image = cv2.flip(image, 1) if CAMERA_ID == 0 else image
        
        # find hands
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = utils.DETECT_HANDS.process(imgRGB)
        if results.multi_hand_landmarks:  # hand found
            for handType, handLms in zip(results.multi_handedness, results.multi_hand_landmarks):
                lmList = []
                for lm in handLms.landmark:
                    px, py = int(lm.x * image.shape[1]), int(lm.y * image.shape[0])
                    lmList.append([px, py])

            # find distance from index finger tip to index finger mcp   
            x1, y1 = lmList[8]
            x2, y2 = lmList[5]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5  # Euclidean norm

            # draw forefinger
            cv2.circle(image, (lmList[8]), 10, (0, 255, 0), -1)

        # box control
        if results.multi_hand_landmarks:
            # finger out box
            if lmList[8][0] < centerBox[0] - 50 or lmList[8][0] > centerBox[0] + 50 or \
                lmList[8][1] < centerBox[1] - 50 or lmList[8][1] > centerBox[1] + 50:
                colorBox = (155, 0, 155)
                dragActive = 0
            
            # finger in box
            if centerBox[0] - 50 < lmList[8][0] < centerBox[0] + 50 and \
                centerBox[1] - 50 < lmList[8][1] < centerBox[1] + 50:
                dragActive = 1
                colorBox = (255, 0, 255)
                fixPos = lmList[6][1]
            
            # box captured
            if dragActive and centerBox[0] - 50 < lmList[8][0] < centerBox[0] + 50 and \
                centerBox[1] - 50 < lmList[8][1] < fixPos and distance < 85:
                centerBox = lmList[8]
                colorBox = (55, 0, 55)

        # draw box
        cv2.rectangle(image, (centerBox[0]-50, centerBox[1]-50),
                    (centerBox[0]+50, centerBox[1]+50), colorBox, -1)

        cv2.imshow("Image", image)  # show finished image

        # press 'q' to finish program
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()