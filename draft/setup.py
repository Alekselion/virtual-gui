import cv2

CAMERA_ID = 0  # webcamera
CAPTURE = cv2.VideoCapture(CAMERA_ID)
CAPTURE.set(3, 640)  # width: min=160, max=1280
CAPTURE.set(4, 480)  # height: min=120, max=720
_, TEST_IMAGE = CAPTURE.read()
IMAGE_HEIGHT, IMAGE_WIDTH, _ = TEST_IMAGE.shape
IMAGE_CENTER = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2
