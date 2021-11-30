import cv2
import mediapipe as mp

# hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

dragActive = 0
centerBox = 100, 100
sizeBox = 50
colorBox = (155, 0, 155)

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
        cv2.rectangle(outputImage, (centerBox[0]-50, centerBox[1]-50), 
                    (centerBox[0]+50, centerBox[1]+50), colorBox, -1)

        cv2.imshow("Image", outputImage)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()