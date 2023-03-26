import cv2
import utils
from setup import *

numberItems = 3
activeBox = [0] * numberItems
stopClick = [0] * numberItems

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

        # checkbox control
        if results.multi_hand_landmarks:
            for i in range(1, numberItems + 1):
                # active checkbox
                if 50 < lmList[8][0] < 70 and i * 40 + 10 < lmList[8][1] < i * 40 + 30 and not stopClick[i-1]:
                    activeBox[i-1] = 1 if activeBox[i-1] == 0 else 0
                    stopClick[i-1] = 1

                # inactive checkbox
                if stopClick[i-1]:
                    if lmList[8][0] < 40 or lmList[8][0] > 80 or \
                        lmList[8][1] < i * 40 or lmList[8][1] > i * 40 + 40:
                        stopClick[i-1] = 0

        # draw checkboxes
        for i in range(1, numberItems + 1):
            if activeBox[i-1]:
                cv2.rectangle(image, (50, i * 40 + 10), (70, i * 40 + 30), (255, 0, 255), -1)
                cv2.putText(image, "X", (53, i * 40 + 27),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (55, 0, 55), 2)
                cv2.putText(image, f"item {i}", (80, i * 40 + 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            else:
                cv2.rectangle(image, (50, i * 40 + 10), (70, i * 40 + 30), (155, 0, 155), -1)
                cv2.putText(image, f"item {i}", (80, i * 40 + 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (155, 155, 155), 2)

        cv2.imshow("Image", image)  # show finished image

        # press 'q' to finish program
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()