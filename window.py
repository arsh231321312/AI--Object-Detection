import cv2
import numpy as np
import time
from mss import mss
import ultralytics

add=0  #370 inven  0 normal
x_pixel_start = 1920-992+add   # x-coordinate of top left corner     #292 orig
y_pixel_start = 30+add    # y-coordinate of top left corner     #80 orig
x_pixel_end = 992-30+x_pixel_start    # x-coordinate of bottom right corner
y_pixel_end = 653-30+ y_pixel_start     # y-coordinate of bottom right corner

# Add some padding to the bounding box dimensions
padding = 15
x_pixel_start -= padding
y_pixel_start -= padding
x_pixel_end += padding
y_pixel_end += padding

width = x_pixel_end - x_pixel_start
height = y_pixel_end - y_pixel_start

bounding_box = {'top': y_pixel_start, 'left': x_pixel_start, 'width': width, 'height': height}

sct = mss()

def screenshot():
    sct_img = sct.grab(bounding_box)
    scr_img = np.array(sct_img)
    #cv2.imshow('screen', scr_img) # display screen in box
    cv2.imshow('Testing', scr_img)

    if (cv2.waitKey(0) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
    elif ord('s'):
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f'on1_{timestamp}.png'
        cv2.imwrite(filename, scr_img)
        print(f"Screenshot saved as {filename}!")

try:
    while True:
        if ord(','):
            screenshot()
        else:
            continue
except KeyboardInterrupt:
    pass
finally:
    cv2.destroyAllWindows()
