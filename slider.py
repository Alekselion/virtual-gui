import cv2
import mediapipe as mp

# hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

position = 30, 100
label = "0%"

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
        
        if results.multi_hand_landmarks:
            if 29 < lmList[8][0] < 131 and 90 < lmList[8][1] < 110:
                position = lmList[8][0], 100
                label = f"{lmList[8][0] - 30}%"
        
        cv2.line(outputImage, (30, 100), (130, 100), (155, 0, 155), 10)
        cv2.circle(outputImage, position, 13, (255, 0, 255), -1)
        cv2.circle(outputImage, position, 7, (55, 0, 55), -1)
        cv2.putText(outputImage, label, (position[0], 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
        cv2.imshow("Image", outputImage)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()