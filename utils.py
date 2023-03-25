import cv2
import numpy as np
import mediapipe as mp

# HANDS
DETECT_HANDS = mp.solutions.hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
DRAW_HANDS = mp.solutions.drawing_utils
DRAW_HANDS_STYLE = mp.solutions.drawing_styles
# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
DARK_GRAY = (63, 63, 63)
RED = (50, 50, 255)
DARK_RED = (20, 20, 150)
GREEN = (50, 200, 50)
DARK_GREEN = (20, 150, 20)
BLUE = (200, 50, 50)
DARK_BLUE = (150, 20, 20)
# FONT
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.9


def hands_detection(image) -> list:
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = DETECT_HANDS.process(image_rgb)
    if results.multi_hand_landmarks:  # hand found
        for hand_type, hand_landmarks in zip(results.multi_handedness, results.multi_hand_landmarks):
            landmarks_list = []
            for landmark in hand_landmarks.landmark:
                px, py = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
                landmarks_list.append([px, py])

        # landmarks_list[4] - thumb tip
        # landmarks_list[8] - index finger tip
        # landmarks_list[12] - middle finger tip
        # landmarks_list[16] - ring finger tip
        # landmarks_list[20] - pinky finger tip
        return landmarks_list
    
    return [[0, 0]] * 11


def get_distance(first_finger:list, second_finger:list) -> int:
    x1, y1 = first_finger
    x2, y2 = second_finger
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5  # Euclidean norm


def draw_finger(image, finger:list) -> None:
    if finger != [0, 0]:
        cv2.circle(image, (finger), 10, BLUE, 2)
        position = finger[0] - 50, finger[1] + 30
        cv2.putText(image, str(finger), position, FONT_FACE, 0.6, BLUE, 2)


def draw_hands(image, hand_landmarks):
    pass


def draw_text(image, text:str='text', position:tuple=(50, 50), color:tuple=GRAY) -> None:
    cv2.putText(image, text, position, FONT_FACE, FONT_SCALE, DARK_GRAY, 4)  # background
    cv2.putText(image, text, position, FONT_FACE, FONT_SCALE, color, 2)


def draw_circle(image, position:tuple=(50, 50), radius:int=10, color:tuple=GRAY) -> None:
    cv2.circle(image, position, radius, DARK_GRAY, 2)  # background
    cv2.circle(image, position, radius, color, -1)


# if __name__ == '__main__':
#     from setup import *
#
#     MENU = draw_menu(["text"]*9)
#
#     # start camera
#     while CAPTURE.isOpened():
#         success, image = CAPTURE.read()
#         if success:
#             image = cv2.flip(image, 1) if CAMERA_ID == 0 else image
#
#             # show menu
#             cv2.imshow("Menu", MENU)
#
#             # get the forefinger position
#             landmarks = hands_detection(image)
#             forefinger = landmarks[8]
#             draw_finger(image, forefinger)
#
#             # show hand image
#             cv2.imshow("Hand", image)
#
#             # canvas for show colors and text
#             canvas = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), np.uint8)
#             canvas[:, :, :] = (25, 25, 25)  # background color
#
#             # gray
#             canvas[10:70, 10:70, :] = WHITE
#             canvas[10:70, 80:140, :] = GRAY
#             canvas[10:70, 150:210, :] = DARK_GRAY
#             canvas[10:70, 220:280, :] = BLACK
#
#             # rgb
#             canvas[80:140, 10:70, :] = RED
#             canvas[80:140, 80:140, :] = GREEN
#             canvas[80:140, 150:210, :] = BLUE
#
#             # dark rgb
#             canvas[150:210, 10:70, :] = DARK_RED
#             canvas[150:210, 80:140, :] = DARK_GREEN
#             canvas[150:210, 150:210, :] = DARK_BLUE
#
#             # text
#             print_text(canvas, "a"*10)
#
#             # show canvas
#             cv2.imshow("Canvas", canvas)
#
#             # press 'q' to finish program
#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#
#     CAPTURE.release()
#     cv2.destroyAllWindows()