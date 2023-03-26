import cv2
from setup import IMAGE_CENTER
import numpy as np
import mediapipe as mp

# HANDS
DETECT_HANDS = mp.solutions.hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
DRAW_HANDS = mp.solutions.drawing_utils

# GRAY COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
DARK_GRAY = (63, 63, 63)

# RGB COLORS
RED = (50, 50, 200)
DARK_RED = (20, 20, 150)
GREEN = (50, 200, 50)
DARK_GREEN = (20, 150, 20)
BLUE = (200, 50, 50)
DARK_BLUE = (150, 20, 20)

# FONT
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.9

TEXT_MAX_LENGTH = 20
TEXT_POSITION = IMAGE_CENTER[0] - 150, IMAGE_CENTER[1] + 60


def draw_menu(texts:list=["nothing"]*9):
    height = IMAGE_HEIGHT // 2
    canvas = np.zeros((height, IMAGE_WIDTH, 3), np.uint8)
    canvas[:, :, :] = DARK_GRAY  # background color

    if len(texts) > 9:
        texts = texts[:9]
    elif len(texts) < 9:
        texts = texts + ["nothing"] * (9 - len(texts))

    # horizontal split
    cv2.line(canvas, (0, height // 3), (IMAGE_WIDTH, height // 3), GRAY, 2)
    cv2.line(canvas, (0, height - height // 3), (IMAGE_WIDTH, height - height // 3), GRAY, 2)
    # vertical split
    cv2.line(canvas, (IMAGE_WIDTH // 3, 0), (IMAGE_WIDTH // 3, height), GRAY, 2)
    cv2.line(canvas, (IMAGE_WIDTH - IMAGE_WIDTH // 3, 0), (IMAGE_WIDTH - IMAGE_WIDTH // 3, height), GRAY, 2)

    margin = 10

    # row 1
    cv2.putText(canvas, "1. " + str(texts[0]), (margin, height // 5), FONT_FACE, FONT_SCALE, GRAY, 2)
    cv2.putText(canvas, "2. " + str(texts[1]), (IMAGE_WIDTH // 3 + margin, height // 5), FONT_FACE, FONT_SCALE, GRAY, 2)
    cv2.putText(canvas, "3. " + str(texts[2]), ((IMAGE_WIDTH - IMAGE_WIDTH // 3) + margin, height // 5), FONT_FACE, FONT_SCALE, GRAY, 2)
    # row 2
    cv2.putText(canvas, "4. " + str(texts[3]), (margin, height // 2 + margin // 2), FONT_FACE, FONT_SCALE, GRAY, 2)
    cv2.putText(canvas, "5. " + str(texts[4]), (IMAGE_WIDTH // 3 + margin, height // 2 + margin // 2), FONT_FACE, FONT_SCALE, GRAY, 2)
    cv2.putText(canvas, "6. " + str(texts[5]), ((IMAGE_WIDTH - IMAGE_WIDTH // 3) + margin, height // 2 + margin // 2), FONT_FACE, FONT_SCALE, GRAY, 2)
    # row 3
    cv2.putText(canvas, "7. " + str(texts[6]), (margin, height - margin * 3), FONT_FACE, FONT_SCALE, GRAY, 2)
    cv2.putText(canvas, "8. " + str(texts[7]), (IMAGE_WIDTH // 3 + margin, height - margin * 3), FONT_FACE, FONT_SCALE, GRAY, 2)
    cv2.putText(canvas, "9. " + str(texts[8]), ((IMAGE_WIDTH - IMAGE_WIDTH // 3) + margin, height - margin * 3), FONT_FACE, FONT_SCALE, GRAY, 2)

    return canvas


def hands_detection(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = DETECT_HANDS.process(image_rgb)
    if results.multi_hand_landmarks:  # hand found
        for hand_type, hand_landmarks in zip(results.multi_handedness, results.multi_hand_landmarks):
            landmarks_list = []
            for landmark in hand_landmarks.landmark:
                px, py = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
                landmarks_list.append([px, py])

        # # distance from index finger tip to index finger mcp   
        # x1, y1 = forefinger
        # x2, y2 = left_forefinger
        # distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5  # Euclidean norm

        return landmarks_list
    
    return [[0, 0]] * 11


def draw_finger(image, finger:list):
    cv2.circle(image, (finger), 10, GREEN, 2)
    position = finger[0] - 50, finger[1] + 30
    cv2.putText(image, str(finger), position, FONT_FACE, 0.6, GREEN, 2)


def print_text(image, text:str='', color:tuple=GREEN):
    text_length = len(text)
    if text_length < TEXT_MAX_LENGTH:
        text = text.center(TEXT_MAX_LENGTH)
    elif text_length > TEXT_MAX_LENGTH:
        text = text[:20]

    cv2.putText(image, text, TEXT_POSITION, FONT_FACE, FONT_SCALE, DARK_GRAY, 4)  # background
    cv2.putText(image, text, TEXT_POSITION, FONT_FACE, FONT_SCALE, color, 2)


if __name__ == '__main__':
    from versions.setup import *

    MENU = draw_menu(["text"]*9)

    # start camera
    while CAPTURE.isOpened():
        success, image = CAPTURE.read()
        if success:
            image = cv2.flip(image, 1) if CAMERA_ID == 0 else image
            
            # show menu
            cv2.imshow("Menu", MENU)

            # get the forefinger position
            landmarks = hands_detection(image)
            forefinger = landmarks[8]
            draw_finger(image, forefinger)

            # show hand image
            cv2.imshow("Hand", image)

            # canvas for show colors and text
            canvas = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), np.uint8)
            canvas[:, :, :] = (25, 25, 25)  # background color
            
            # gray
            canvas[10:70, 10:70, :] = WHITE
            canvas[10:70, 80:140, :] = GRAY
            canvas[10:70, 150:210, :] = DARK_GRAY
            canvas[10:70, 220:280, :] = BLACK

            # rgb
            canvas[80:140, 10:70, :] = RED
            canvas[80:140, 80:140, :] = GREEN
            canvas[80:140, 150:210, :] = BLUE

            # dark rgb
            canvas[150:210, 10:70, :] = DARK_RED
            canvas[150:210, 80:140, :] = DARK_GREEN
            canvas[150:210, 150:210, :] = DARK_BLUE

            # text
            print_text(canvas, "a"*10)

            # show canvas
            cv2.imshow("Canvas", canvas)

            # press 'q' to finish program
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    CAPTURE.release()
    cv2.destroyAllWindows()