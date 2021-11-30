import cv2
import mediapipe as mp

# hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

numberItems = 3
activeRadioButton = 1

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

            # draw finger points
            cv2.circle(outputImage, (lmList[8]), 10, (0, 255, 0), -1)  # forefinger

        # active radio button
        if results.multi_hand_landmarks:
            for i in range(1, numberItems + 1):
                if 40 < lmList[8][0] < 60 and i * 40 < lmList[8][1] < i * 40 + 20:
                    activeRadioButton = i

        # draw radio buttons
        for i in range(1, numberItems + 1):
            cv2.circle(outputImage, (50, i * 40 + 10), 10, (155, 0, 155), -1)
            cv2.putText(outputImage, f"item {i}", (70, i * 40 + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (155, 155, 155), 2)

            if i == activeRadioButton:
                cv2.circle(outputImage, (50, i * 40 + 10), 10, (255, 0, 255), -1)
                cv2.circle(outputImage, (50, i * 40 + 10), 5, (55, 0, 55), -1)
                cv2.putText(outputImage, f"item {i}", (70, i * 40 + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Image", outputImage)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()