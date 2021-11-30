import cv2
import mediapipe as mp

# hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

numberItems = 3
activeBox = [0] * numberItems
stopClick = [0] * numberItems

# read camera
idCam = 0
widthImage, heightImage = 640, 480
cap = cv2.VideoCapture(idCam)
cap.set(3, widthImage)
cap.set(4, heightImage)
while cap.isOpened():
    success, image = cap.read()
    if success:
        if idCam == 0:
            image = cv2.flip(image, 1)
            
        outputImage = image.copy()
        
        # find hands
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
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

            # draw finger points
            cv2.circle(outputImage, (lmList[8]), 10, (0, 255, 0), -1)  # forefinger

        # checkbox control
        if results.multi_hand_landmarks:
            for i in range(1, numberItems + 1):
                # active checkbox
                if 50 < lmList[8][0] < 70 and i * 40 + 10 < lmList[8][1] < i * 40 + 30 and not stopClick[i-1]:
                    activeBox[i-1] = 1 if activeBox[i-1] == 0 else 0
                    stopClick[i-1] = 1

                # deactive checkbox
                if stopClick[i-1]:
                    if lmList[8][0] < 40 or lmList[8][0] > 80 or \
                        lmList[8][1] < i * 40 or lmList[8][1] > i * 40 + 40:
                        stopClick[i-1] = 0

        # draw checkboxes
        for i in range(1, numberItems + 1):
            if activeBox[i-1]:
                cv2.rectangle(outputImage, (50, i * 40 + 10), (70, i * 40 + 30), (255, 0, 255), -1)
                cv2.putText(outputImage, "X", (53, i * 40 + 27), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (55, 0, 55), 2)
                cv2.putText(outputImage, f"item {i}", (80, i * 40 + 28), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            else:
                cv2.rectangle(outputImage, (50, i * 40 + 10), (70, i * 40 + 30), (155, 0, 155), -1)
                cv2.putText(outputImage, f"item {i}", (80, i * 40 + 28), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (155, 155, 155), 2)

        cv2.imshow("Image", outputImage)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()