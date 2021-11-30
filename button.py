import cv2
import mediapipe as mp

# hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

clicks = 0
stopClick = 0
buttonActive = 0

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

            # draw forefinger
            cv2.circle(outputImage, (lmList[8]), 10, (0, 255, 0), -1)

        cv2.rectangle(outputImage, (50, 50), (200, 100), (155, 0, 155), -1)
        cv2.putText(outputImage, "button", (80, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (155, 155, 155), 2)
        cv2.putText(outputImage, f"click x{clicks}", (75, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

        # button control
        if results.multi_hand_landmarks:
            # active button
            if 50 < lmList[8][0] < 200 and 50 < lmList[8][1] < 100:
                buttonActive = 1
                fixPos = lmList[6][1]
                cv2.rectangle(outputImage, (50, 50), (200, 100), (255, 0, 255), -1)
                cv2.putText(outputImage, "button", (80, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                cv2.putText(outputImage, f"click x{clicks}", (75, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
            
            # make click
            if buttonActive and 50 < lmList[8][0] < 200 and 50 < lmList[8][1] < fixPos:
                if distance < 85 and stopClick == 0:
                    clicks += 1
                    stopClick = 1
                    buttonActive = 0
            
            if distance > 85 and stopClick == 1:
                stopClick = 0
                            
        cv2.imshow("Image", outputImage)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()