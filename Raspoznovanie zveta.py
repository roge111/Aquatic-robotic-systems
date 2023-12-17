
import cv2 as cv
import time


image = cv.imread('D:\testtir.jpg')

def color_uckazatelia(image):


    image_HSV = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    image_HSV2 = cv.cvtColor(image1, cv.COLOR_BGR2HSV)
    low_hsv_blue = (90, 50, 50)
    max_hsv_blue = (105, 255, 255)

    low_hsv_violet = (130, 50, 50)
    max_hsv_violet = (145, 255, 255)

    low_hsv_green = (45, 50, 50)
    max_hsv_green = (75, 255, 255)

    low_hsv_orange = (10, 50, 50)
    max_hsv_orange = (25, 255, 255)

    blue_mask = cv.inRange(image_HSV, low_hsv_blue, max_hsv_blue)
    cnt_blue, _ = cv.findContours(blue_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    blue_mask2 = cv.inRange(image_HSV2, low_hsv_blue, max_hsv_blue)
    cnt_blue2, _ = cv.findContours(blue_mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    violet_mask = cv.inRange(image_HSV, low_hsv_violet, max_hsv_violet)
    cnt_violet, _ = cv.findContours(violet_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    violet_mask2 = cv.inRange(image_HSV2, low_hsv_violet, max_hsv_violet)
    cnt_violet2, _ = cv.findContours(violet_mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #cv.imshow('mask', violet_mask2)

    green_mask = cv.inRange(image_HSV, low_hsv_green, max_hsv_green)
    cnt_green, _ = cv.findContours(green_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    orange_mask = cv.inRange(image_HSV, low_hsv_orange, max_hsv_orange)
    cnt_orange, _ = cv.findContours(orange_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    global blue1
    global green1
    global violet1
    global orange1

    blue1 = 0
    green1 = 0
    violet1 = 0
    orange1 = 0

    if cnt_blue:
        blue1 = 1
        green1 =0
        violet1 = 0
        orange1 = 0


        #return True,  blue1, green1, violet1, orange1
    elif cnt_orange:
        blue1 = 0
        green1 = 0
        violet1 = 0
        orange1 = 1

        #return True,  blue1, green1, violet1, orange1
    elif cnt_green:
        blue1 = 0
        green1 = 1
        violet1 = 0
        orange1 = 0

    elif cnt_violet:
        blue1 = int(0)
        green1 = int(0)
        violet1 = int(1)
        orange1 = int(0)


    return blue1, green1, violet1, orange1

, violet1, orange1

, violet1, orange1

