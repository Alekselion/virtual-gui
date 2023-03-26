from setup import IMAGE_CENTER
import time

HOLD_RADIUS = 35
HOLD_TIMER_SECONDS = 2
HOLD_TIMER_POINT = IMAGE_CENTER[0] - 18, IMAGE_CENTER[1] + 18


def draw(image, seconds_left:int=0):
    if seconds_left > 0:
        circle_color = text_color = utils.DARK_GREEN
        text = "hold"
    elif seconds_left == 0:
        circle_color = text_color = utils.GREEN
        text = "done"
    else:
        circle_color = utils.GRAY
        text_color = utils.RED
        text = "Put your finger"
        seconds_left = ""

    # circle
    cv2.circle(image, IMAGE_CENTER, HOLD_RADIUS, circle_color, -1)
    cv2.circle(image, IMAGE_CENTER, HOLD_RADIUS, utils.DARK_GRAY, 2)

    # number in circle
    cv2.putText(image, str(seconds_left), HOLD_TIMER_POINT, utils.FONT_FACE, 1.6, utils.DARK_GRAY, 3)
    utils.print_text(image, text, text_color)  # text


def hold(finger:list, prev_state:bool, finish_time:time=None):
    # finger in circle
    if ((IMAGE_CENTER[0] - finger[0]) ** 2 + (IMAGE_CENTER[1] - finger[1]) ** 2) ** 0.5 < HOLD_RADIUS:
        current_state = True
        # continue timer
        if prev_state and finish_time is not None:
            seconds_left = finish_time - time.perf_counter()
        # start timer
        else:
            finish_time = time.perf_counter() + HOLD_TIMER_SECONDS + 1
            seconds_left = HOLD_TIMER_SECONDS
    else:
        current_state = False
        finish_time = None
        seconds_left = -1

    return current_state, finish_time, int(seconds_left)


if __name__ == '__main__':
    from setup import *
    import utils

    DEBUG = True
    state = False
    timer = None

    # start camera
    while CAPTURE.isOpened():
        success, image = CAPTURE.read()
        if success:
            image = cv2.flip(image, 1) if CAMERA_ID == 0 else image
            
            # get the forefinger position
            landmarks = utils.hands_detection(image)
            forefinger = landmarks[8]

            # hold
            state, timer, seconds_left = hold(forefinger, state, timer)
            draw(image, seconds_left)

            if DEBUG:
                utils.draw_finger(image, forefinger)

            cv2.imshow("Image", image)  # show finished image

            # press 'q' to finish program
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    CAPTURE.release()
    cv2.destroyAllWindows()