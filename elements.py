import cv2
import numpy as np

canvas = np.zeros([420, 650, 3], np.uint8)
        
# ######
# switch
# ######

# hover
cv2.line(canvas, (60, 30), (80, 30), (100, 0, 100), 10)
cv2.circle(canvas, (60, 30), 10, (155, 0, 155), -1)

# active
cv2.line(canvas, (60, 60), (80, 60), (100, 0, 100), 10)
cv2.circle(canvas, (80, 60), 10, (255, 0, 255), -1)

cv2.putText(canvas, "switch", (160, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

# ######
# button
# ######

# hover
cv2.rectangle(canvas, (20, 90), (130, 120), (155, 0, 155), -1)
cv2.putText(canvas, "button", (35, 113), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (155, 155, 155), 2)

# active
cv2.rectangle(canvas, (20, 130), (130, 160), (255, 0, 255), -1)
cv2.putText(canvas, "button", (35, 153), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

cv2.putText(canvas, "button", (160, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

# ############
# radio button
# ############

# hover
cv2.circle(canvas, (30, 200), 13, (155, 0, 155), -1)
cv2.putText(canvas, "item 1", (50, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (155, 155, 155), 2)

# active
cv2.circle(canvas, (30, 240), 13, (255, 0, 255), -1)
cv2.circle(canvas, (30, 240), 8, (55, 0, 55), -1)
cv2.putText(canvas, "item 2", (50, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

cv2.putText(canvas, "radio", (160, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
cv2.putText(canvas, "button", (160, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

# ########
# checkbox
# ########

# hover
cv2.rectangle(canvas, (20, 280), (40, 300), (155, 0, 155), -1)
cv2.putText(canvas, "item 1", (50, 298), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (155, 155, 155), 2)

# active
cv2.rectangle(canvas, (20, 320), (40, 340), (255, 0, 255), -1)
cv2.putText(canvas, "X", (23, 337), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (55, 0, 55), 2)
cv2.putText(canvas, "item 2", (50, 337), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

cv2.putText(canvas, "checkbox", (160, 315), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

# ######
# slider
# ######

cv2.line(canvas, (20, 380), (120, 380), (155, 0, 155), 10)
cv2.putText(canvas, "0%", (10, 405), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
cv2.putText(canvas, "100%", (100, 405), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
cv2.circle(canvas, (60, 380), 13, (255, 0, 255), -1)
cv2.circle(canvas, (60, 380), 7, (55, 0, 55), -1)
cv2.putText(canvas, "slider", (160, 385), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

# #############
# dropdown list
# #############

# hover
cv2.rectangle(canvas, (350, 30), (450, 60), (255, 0, 255), -1)
cv2.putText(canvas, "items >", (355, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# active
cv2.rectangle(canvas, (350, 90), (450, 120), (255, 0, 255), -1)
cv2.putText(canvas, "items ^", (355, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# list
cv2.rectangle(canvas, (350, 120), (450, 260), (155, 0, 155), -1)
cv2.putText(canvas, "item 1", (355, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
cv2.putText(canvas, "item 2", (355, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
cv2.putText(canvas, "item 3", (355, 195), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
cv2.putText(canvas, "item 4", (355, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
cv2.putText(canvas, "item 5", (355, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

# scroll
cv2.rectangle(canvas, (440, 120), (450, 260), (155, 155, 155), -1) 
cv2.rectangle(canvas, (440, 120), (450, 130), (255, 255, 255), -1) 
cv2.rectangle(canvas, (440, 250), (450, 260), (255, 255, 255), -1) 

cv2.putText(canvas, "dropdown", (490, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
cv2.putText(canvas, "list", (490, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

cv2.imshow("Image", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()