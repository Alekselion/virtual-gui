import cv2
import utils
import time
from abc import ABC


class Template(ABC):
    def __init__(self): ...

    def draw(self): ...

    def action(self): ...

    def reset(self): ...


class Switch(Template):
    def __init__(self, point:tuple, line_len:int=50, text_on:str='turn on', text_off:str='turn off'):
        # line
        self.line_len = line_len
        self.line_half_len = line_len // 2
        self.line_pt1 = point[0] - self.line_half_len, point[1]
        self.line_pt2 = point[0] + self.line_half_len, point[1]
        # cursor
        self.cursor_is_active = False
        self.cursor_radius = self.line_len // 3
        # text
        self.text_pos = point[0] - 50, point[1] + 50  # under line
        self.text_on = str(text_on)
        self.text_off = str(text_off)
        # border
        self.border_width = self.line_pt1[0], self.line_pt2[0]
        self.border_center = (self.border_width[0] + self.border_width[1]) // 2
        self.border_height = (
            (self.line_pt2[1] - self.line_half_len // 2),
            (self.line_pt2[1] + self.line_half_len // 2)
        )
        self.border_off = (
            (self.border_width[0], self.border_height[0]),
            (self.border_center, self.border_height[1])
        )
        self.border_on = (
            (self.border_center, self.border_height[0]),
            (self.border_width[1], self.border_height[1])
        )

    def draw(self, image, debug:bool=False):
        # line
        cv2.line(image, self.line_pt1, self.line_pt2, utils.DARK_GRAY, self.line_half_len)
        # cursor
        cursor_pt = self.line_pt2 if self.cursor_is_active else self.line_pt1
        cursor_color = utils.GREEN if self.cursor_is_active else utils.GRAY
        utils.draw_circle(image, cursor_pt, self.cursor_radius, cursor_color)
        # text
        text = self.text_on if self.cursor_is_active else self.text_off
        text_color = utils.GREEN if self.cursor_is_active else utils.RED
        utils.draw_text(image, text, self.text_pos, text_color)
        if debug:
            cv2.rectangle(image, self.border_off[0], self.border_off[1], utils.RED, 2)
            cv2.rectangle(image, self.border_on[0], self.border_on[1], utils.GREEN, 2)

    def action(self, finger:list):
        if self.border_height[0] < finger[1] < self.border_height[1]:  # finger on line
            if self.border_width[0] < finger[0] < self.border_center:  # switch off
                self.cursor_is_active = False
                return
            if self.border_center < finger[0] < self.border_width[1]:  # switch on
                self.cursor_is_active = True
                return

    def reset(self):
        self.cursor_is_active = False


class Swipe(Template):
    def __init__(self, point:tuple, line_len:int=180, text:str='move cursor', text_done:str='completed'):
        # line
        self.line_len = line_len
        self.line_half_len = line_len // 2
        self.line_thickness = self.line_half_len // 3
        self.line_pt1 = point[0] - self.line_half_len, point[1]
        self.line_pt2 = point[0] + self.line_half_len, point[1]
        # cursor
        self.cursor_is_moving = False
        self.cursor_at_end = False
        self.cursor_len = self.line_half_len // 5
        self.cursor_min = self.line_pt1[0] + self.cursor_len
        self.cursor_max = self.line_pt2[0] - self.cursor_len
        self.cursor_pos = self.cursor_min
        # text
        self.text = str(text)
        self.text_done = str(text_done)
        self.text_pos = self.line_pt1[0] + 15, self.line_pt1[1] + 50  # under line
        # border
        self.border_width = self.line_pt1[0], self.line_pt2[0]
        self.border_height = (
            (self.line_pt1[1] - self.line_thickness // 2),
            (self.line_pt2[1] + self.line_thickness // 2)
        )
        self.border_line = (
            (self.border_width[0], self.border_height[0]),
            (self.border_width[1], self.border_height[1])
        )
        self.border_cursor_min = (
            (self.cursor_min, self.border_height[0]),
            (self.cursor_min + self.cursor_len, self.border_height[1])
        )
        self.border_cursor_max = (
            (self.cursor_max, self.border_height[0]),
            (self.cursor_max + self.cursor_len, self.border_height[1])
        )

    def draw(self, image, debug:bool=False):
        # line
        cv2.line(image, self.line_pt1, self.line_pt2, utils.DARK_GRAY, self.line_thickness)
        # cursor
        cursor_pt1 = self.cursor_pos - self.cursor_len, self.line_pt1[1]
        cursor_pt2 = self.cursor_pos + self.cursor_len, self.line_pt2[1]
        cursor_color = utils.GREEN if self.cursor_at_end else utils.GRAY
        cv2.line(image, cursor_pt1, cursor_pt2, cursor_color, self.line_thickness)
        # text
        text = self.text_done if self.cursor_at_end else self.text
        text_color = utils.GREEN if self.cursor_at_end else utils.RED
        utils.draw_text(image, text, self.text_pos, text_color)
        if debug:
            cv2.rectangle(image, self.border_line[0], self.border_line[1], utils.GREEN, 2)
            cv2.rectangle(image, self.border_cursor_min[0], self.border_cursor_min[1], utils.RED, 2)
            cv2.rectangle(image, self.border_cursor_max[0], self.border_cursor_max[1], utils.RED, 2)

    def action(self, finger:list):
        if self.cursor_at_end:
            return
        finger_in_border_x = self.border_width[0] < finger[0] < self.border_width[1]
        finger_in_border_y = self.border_height[0] < finger[1] < self.border_height[1]
        if self.cursor_is_moving:  # continue move cursor
            if finger_in_border_x and finger_in_border_y:  # finger on line
                if finger[0] > self.cursor_max:  # cursor at end point
                    self.cursor_pos = self.cursor_max
                    self.cursor_at_end = True
                    return
                if finger[0] < self.cursor_min:  # cursor at start point
                    self.cursor_pos = self.cursor_min
                    return

                self.cursor_pos = finger[0]
                return

        # begin move cursor
        self.cursor_pos = self.cursor_min
        self.cursor_is_moving = (
                finger_in_border_y and
                self.line_pt1[0] < finger[0] < self.line_pt1[0] + self.cursor_len * 2
        )

    def reset(self):
        self.cursor_at_end = False


class Slider(Template):
    def __init__(self, point:tuple, line_len:int=400, scale_step:int=5):
        # line
        self.line_len = line_len
        self.line_half_len = line_len // 2
        self.line_thickness = self.line_half_len // 10
        self.line_pt1 = point[0] - self.line_half_len, point[1]
        self.line_pt2 = point[0] + self.line_half_len, point[1]
        # cursor
        self.cursor_percent = 0
        self.cursor_min = self.line_pt1[0]
        self.cursor_max = self.line_pt2[0]
        self.cursor_len = 20
        self.cursor_pos = self.cursor_min
        self.text_pos = self.line_len // 2 + 15, self.line_pt1[1] + 55
        # scale
        self.scale_step = scale_step  # 0%, 5%, ..., 95%, 100%
        self.scale_offset = line_len // (100 // scale_step)
        self.scale_half_offset = self.scale_offset // 2
        # dictionary "percent => cursor_position"
        scale_pos_keys = list(range(0, 101, self.scale_step))
        scale_pos_vals = list(range(self.line_pt1[0], self.line_pt2[0] + 1, self.scale_offset))
        self.scale_positions = dict(zip(scale_pos_keys, scale_pos_vals))
        # dictionary "finger_position_by_x => percent"
        scale_first_keys = list(range(self.line_pt1[0], self.line_pt1[0] + self.scale_half_offset))
        scale_last_keys = list(range(self.line_pt2[0] - self.scale_half_offset, self.line_pt2[0] + 1))
        list_to_dict = list(zip(scale_first_keys, [0] * len(scale_first_keys))) +\
                       list(zip(scale_last_keys, [100] * len(scale_last_keys)))
        curr_min_x = self.line_pt1[0] + self.scale_half_offset
        curr_val = self.scale_step
        while curr_val < 100:
            for i in range(curr_min_x, curr_min_x + self.scale_offset):
                list_to_dict.append((i, curr_val))
            curr_min_x += self.scale_offset
            curr_val += self.scale_step
        self.scale_ranges = dict(list_to_dict)
        # border
        self.border_width = self.line_pt1[0], self.line_pt2[0]
        self.border_height = (
            (self.line_pt1[1] - self.line_thickness),
            (self.line_pt2[1] + self.line_thickness)
        )
        self.border_line = (
            (self.border_width[0], self.border_height[0]),
            (self.border_width[1], self.border_height[1])
        )

    def draw(self, image, debug:bool=False):
        # line
        cv2.line(image, self.line_pt1, self.line_pt2, utils.DARK_GRAY, self.line_thickness)
        # cursor
        cursor_pt1 = self.cursor_pos, self.line_pt1[1] - self.cursor_len
        cursor_pt2 = self.cursor_pos, self.line_pt1[1] + self.cursor_len
        cv2.line(image, cursor_pt1, cursor_pt2, utils.DARK_GRAY, self.line_thickness)
        cv2.line(image, cursor_pt1, cursor_pt2, utils.GRAY, self.line_thickness - 5)
        # text
        utils.draw_text(image, f"{self.cursor_percent}%", self.text_pos, utils.GREEN)
        if debug:
            cv2.rectangle(image, self.border_line[0], self.border_line[1], utils.RED, 2)
            for scale in self.scale_positions.values():
                border_scale = (scale, self.border_height[0]), (scale, self.border_height[1])
                cv2.rectangle(image, border_scale[0], border_scale[1], utils.GREEN, 2)

    def action(self, finger):
        finger_in_border_x = self.border_width[0] < finger[0] < self.border_width[1]
        finger_in_border_y = self.border_height[0] < finger[1] < self.border_height[1]
        if finger_in_border_y and finger_in_border_x:  # finger on line
            self.cursor_percent = self.scale_ranges[finger[0]]
            self.cursor_pos = self.scale_positions[self.cursor_percent]

    def reset(self):
        self.cursor_percent = 0
        self.cursor_pos = self.cursor_min


class Dial(Template):
    def __init__(self, point:tuple, radius:int=50):
        # circle
        self.point = point
        self.inner_radius = radius
        self.outer_radius = radius * 2
        # line
        self.line_len = radius - 15
        self.line_pos = point[0], point[1] - radius

    def draw(self, image, debug:bool=False):
        cv2.circle(image, self.point, self.outer_radius, utils.DARK_GRAY, 2)
        utils.draw_circle(image, self.point, self.inner_radius)
        cv2.line(image, self.point, self.line_pos, utils.GREEN, 3)

    def action(self, finger:list):
        # finger not in circle
        finger_in_circle = ((self.point[0] - finger[0]) ** 2 + (self.point[1] - finger[1]) ** 2) ** 0.5
        if finger_in_circle <= self.inner_radius or finger_in_circle >= self.outer_radius:
            return
        # get distance from center circle and finger
        ax, ay = self.point
        bx, by = finger
        ab = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5  # Euclidean norm
        # get end point position
        ac = ab - self.inner_radius if ab <= self.inner_radius else self.inner_radius
        k = ac / ab
        cx = int(ax + (bx - ax) * k)
        cy = int(ay + (by - ay) * k)
        self.line_pos = [cx, cy]

    def reset(self):
        self.line_pos = self.point[0], self.point[1] - self.inner_radius


class AnalogStick(Template):
    def __init__(self, point:tuple, radius:int=35):
        # inner circle
        self.point = point
        self.inner_radius = radius
        self.inner_half_radius = radius // 2
        # outer circle
        self.outer_radius = radius + radius // 3
        self.outer_half_radius = self.outer_radius // 2  # shift
        # positions
        top_pos = self.point[0], self.point[1] - radius
        bottom_pos = self.point[0], self.point[1] + radius
        left_pos = self.point[0] - radius, self.point[1]
        right_pos = self.point[0] + radius, self.point[1]
        shift = self.outer_half_radius // 2
        self.positions = {
            "default": self.point,
            "up": top_pos,
            "down": bottom_pos,
            "left": left_pos,
            "right": right_pos,
            "up left": (left_pos[0] + shift, top_pos[1] + shift),
            "up right": (right_pos[0] - shift, top_pos[1] + shift),
            "down left": (left_pos[0] + shift, bottom_pos[1] - shift),
            "down right": (right_pos[0] - shift, bottom_pos[1] - shift)
        }
        # cursor
        self.cursor_text = "default"
        self.cursor_pos = self.point

    def draw(self, image, debug:bool=False):
        cv2.circle(image, self.point, self.outer_radius, utils.DARK_GRAY, -1)
        utils.draw_circle(image, self.cursor_pos, self.inner_radius)
        # text
        text = "default"
        for key, center in self.positions.items():
            finger_in_circle = ((center[0] - self.cursor_pos[0]) ** 2 + (center[1] - self.cursor_pos[1]) ** 2) ** 0.5
            if finger_in_circle < self.inner_half_radius:
                text = key
        text_x = self.point[0] - len(text) * 6
        text_y = self.point[1] + self.outer_radius + 30
        utils.draw_text(image, text, (text_x, text_y), utils.GREEN)
        if debug:
            for center in self.positions.values():
                cv2.circle(image, center, self.inner_half_radius, (0, 255, 0), 2)

    def action(self, finger:list):
        finger_in_circle = ((self.point[0] - finger[0]) ** 2 + (self.point[1] - finger[1]) ** 2) ** 0.5
        self.cursor_pos = finger if finger_in_circle < self.outer_radius else self.point

    def reset(self):
        self.cursor_pos = self.point


class Rating(Template):
    def __init__(self, point:tuple, number:int=5, radius:int=15):
        self.point = point
        self.number = int(number)
        # circles
        self.radius = int(radius)
        self.rating = 0
        self.positions = { 0: self.point }
        for i in range(1, self.number):
            self.positions[i] = self.positions[i - 1][0] + self.radius * 2 + 5, self.positions[i - 1][1]

    def draw(self, image, degub:bool=False):
        for i in range(self.rating):
            utils.draw_circle(image, self.positions[i], self.radius, utils.GREEN)
        for j in range(self.rating, self.number):
            utils.draw_circle(image, self.positions[j], self.radius, utils.GRAY)


    def action(self, finger:list):
        for i, pos in self.positions.items():
            finger_in_circle = ((pos[0] - finger[0]) ** 2 + (pos[1] - finger[1]) ** 2) ** 0.5 < self.radius
            if finger_in_circle:
                self.rating = i + 1
                return

    def reset(self):
        self.rating = 0


class Radiobutton(Template):
    def __init__(self, point:list, number:int=3, radius:int=15, names:list=['button1', 'button2', 'button3']):
        self.point = point
        self.number = int(number)
        # circles
        self.radius = int(radius)
        self.cursor = 0
        self.positions = { 0: self.point }
        # texts
        self.names = list(names)[:self.number]
        self.text_positions = { 0: ( self.point[0] + self.radius + 10, self.point[1] + 10 ) }
        for i in range(1, self.number):
            self.positions[i] = (
                self.positions[i - 1][0],
                self.positions[i - 1][1] + self.radius * 2 + 5
            )
            self.text_positions[i] = (
                self.text_positions[i - 1][0],
                self.text_positions[i - 1][1] + self.radius * 2 + 5
            )

    def draw(self, image, debug:bool=False):
        for i in range(self.number):
            utils.draw_circle(image, self.positions[i], self.radius, utils.GRAY)
            utils.draw_text(image, self.names[i], self.text_positions[i], utils.GRAY)
        utils.draw_circle(image, self.positions[self.cursor], self.radius // 2, utils.GREEN)
        utils.draw_text(image, self.names[self.cursor], self.text_positions[self.cursor], utils.GREEN)

    def action(self, finger:list):
        for i, pos in self.positions.items():
            finger_in_circle = ((pos[0] - finger[0]) ** 2 + (pos[1] - finger[1]) ** 2) ** 0.5 < self.radius
            if finger_in_circle:
                self.cursor = i
                return

    def reset(self):
        self.cursor = 0


# TODO:
# - add Button
# - add Dropdown list
# - add Checkbox
# - add Drag and Drop / Scale / Rotate


if __name__ == '__main__':
    # camera settings
    CAMERA_ID = 0  # webcamera
    CAPTURE = cv2.VideoCapture(CAMERA_ID)
    CAPTURE.set(3, 640)  # width: min=160, max=1280
    CAPTURE.set(4, 480)  # height: min=120, max=720

    # control panel
    switch_debug = Switch(point=(150, 30), text_on='debug', text_off='debug')
    switch_debug.text_pos = [10, 40]  # left of switch
    switch_reset = Switch(point=(150, 80), text_on='reset', text_off='reset')
    switch_reset.text_pos = [20, 90]  # left of switch
    swipe_quit = Swipe(point=(410, 50), line_len=200, text='quit', text_done='')
    swipe_quit.text_pos = [230, 60]  # left of swipe

    # create elements
    objs = []
    objs.append(Switch(point=(60, 150), text_on='', text_off=''))
    objs.append(Swipe(point=(260, 150), text='', text_done=''))
    objs.append(Rating(point=(450, 150)))
    objs.append(Slider(point=(230, 210)))
    objs.append(Dial(point=(110, 360)))
    objs.append(AnalogStick(point=(300, 360)))
    objs.append(Radiobutton(point=(400, 260)))

    image_load = 2
    while CAPTURE.isOpened():
        success, image = CAPTURE.read()
        if success:
            image = cv2.flip(image, 1) if CAMERA_ID == 0 else image

            # get the index finger tip position
            landmarks = utils.hands_detection(image)
            index_finger_tip = landmarks[8]

            # draw / action the elements
            for obj in objs:
                obj.action(index_finger_tip)
                obj.draw(image, switch_debug.cursor_is_active)

            # debub mod
            switch_debug.action(index_finger_tip)
            switch_debug.draw(image)
            if switch_debug.cursor_is_active:
                utils.draw_finger(image, index_finger_tip)
                # utils.draw_hands(image, landmarks)
                # # color finger
                # cv2.circle(image, (index_finger_tip), 13, (204, 229, 242), -1)

            # reset
            switch_reset.action(index_finger_tip)
            switch_reset.draw(image)
            if switch_reset.cursor_is_active:
                for obj in objs:
                    obj.reset()
                switch_reset.cursor_is_active = False

            # quit
            swipe_quit.action(index_finger_tip)
            swipe_quit.draw(image)
            if swipe_quit.cursor_at_end:
                # bye screen
                image_height, image_width, _ = image.shape
                image_center = image_width // 2, image_height // 2
                image[:, :, :] = (0, 0, 0)  # black canvas
                text = 'B Y E !'
                text_pos = image_center[0] - len(text) * 8, image_center[1]
                utils.draw_text(image, text, text_pos, utils.GREEN)
                if image_load == 0:  # otherwise the image will not be displayed in time
                    # delete the objects
                    del switch_debug
                    del swipe_quit
                    for obj in objs:
                        del obj
                    time.sleep(2)
                    break
                image_load -= 1

            # additional actions (using the keyboard)
            pressed_key = cv2.waitKey(1) & 0xFF
            if pressed_key == ord("q"):  # press 'q' to finish the program
                del switch_debug
                del swipe_quit
                for obj in objs:
                    del obj
                break
            elif pressed_key == ord("r"):  # press 'r' to reset the elements
                for obj in objs:
                    obj.reset()

            cv2.imshow("Image", image)  # show the finished image

    CAPTURE.release()
    cv2.destroyAllWindows()
