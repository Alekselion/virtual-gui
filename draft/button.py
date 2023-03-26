import cv2
import utils
from setup import *

clicks = 0
stopClick = 0
buttonActive = 0

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

        cv2.rectangle(image, (50, 50), (200, 100), (155, 0, 155), -1)
        cv2.putText(image, "button", (80, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (155, 155, 155), 2)
        cv2.putText(image, f"click x{clicks}", (75, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

        if results.multi_hand_landmarks:
            # active button
            if 50 < lmList[8][0] < 200 and 50 < lmList[8][1] < 100:
                buttonActive = 1
                fixPos = lmList[6][1]
                cv2.rectangle(image, (50, 50), (200, 100), (255, 0, 255), -1)
                cv2.putText(image, "button", (80, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                cv2.putText(image, f"click x{clicks}", (75, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

            # make click
            if buttonActive and 50 < lmList[8][0] < 200 and 50 < lmList[8][1] < fixPos:
                if distance < 85 and stopClick == 0:
                    clicks += 1
                    stopClick = 1
                    buttonActive = 0

            if distance > 85 and stopClick == 1:
                stopClick = 0


        cv2.imshow("Image", image)  # show finished image

        # press 'q' to finish program
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

CAPTURE.release()
cv2.destroyAllWindows()