import time
import numpy as np
import cv2
from mss import mss
from PIL import Image, ImageEnhance
from pynput.mouse import Button, Controller, Listener

def find_different(arr):
    for num,i in enumerate(arr):
        if (arr.count(i)==1):
            return num
    return -1
        
mon = {'top': 400, 'left': 1200, 'width': 400, 'height': 400}
mouse = Controller()
click_delay = .4 #secs
sct = mss()
start = time.time()

def on_click():
    time.sleep(click_delay)
Listener(on_click=on_click)

while 1:
    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    converter = ImageEnhance.Color(img)
    img2 = np.array(converter.enhance(2))

    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,1.2,10)
    output = img2
    
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        this = []
        for (x, y, r) in circles:
            this.append(list(img[y,x,:]))
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
        #print(circles)
        nn = find_different(this)
        
        for num,(x, y, r) in enumerate(circles):
            if num == nn:
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                # Move mouse to circle with delay
                # if time.time() > start + click_delay:
                #     start = time.time()
                # Mac user with Retina x2 need to divide by 2
                mouse.position = (mon['left'] + x, mon['top'] + y)
                mouse.position = (mon['left'] + x, mon['top'] + y)
                mouse.click(Button.left)
                time.sleep(click_delay)
                break
            
        
    # cv2.imshow('vit', np.array(img))
    cv2.imshow('vit', np.array(output))
    cv2.moveWindow('vit', mon['left'] - mon['width'] - 80, mon['top']) 
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    
