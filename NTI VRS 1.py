import pymurapi as mur
import time
import cv2 as cv

auv = mur.mur_init()

prev_time = 0
prev_error = 0.0

vr = 0
count_time = 0

def clamp(v, max_v, min_v):
    if v > max_v:
        return max_v
    if v < min_v:
        return min_v
    return v

class PD(object):
    _kp = 0.0
    _kd = 0.0
    _prev_error = 0.0
    _timestamp = 1

    def __init__(self):
        pass
    def set_p_gain(self, value):
        self._kp = value
    def set_d_gain(self, value):
        self._kd = value

    def process(self, error):
        timestamp = int(round(time.time()*1000))
        output = self._kp*error + self._kd / (timestamp - self._timestamp) * (error - self._prev_error)
        self._timestamp = timestamp
        self._prev_error = error
        return output

def keep_yaw(yaw_to_set):
    def clamp_to_180(angle):
        if angle > 180.0:
            return angle - 360.0
        if angle < - 180.0:
            return angle + 360.0
        return angle
    try:
        error = auv.get_yaw() - yaw_to_set
        error = clamp_to_180((error))
        output = keep_yaw.regulator.process(error)
        auv.set_motor_power(0, -output)
        auv.set_motor_power(1, output)
    except AttributeError:
        keep_yaw.regulator = PD()
        keep_yaw.regulator.set_p_gain(0.8)
        keep_yaw.regulator.set_d_gain(8.5)

def keep_depth(value):
    global prev_time
    global prev_error
    current_time = int(round(time.time() * 1000))
    error = auv.get_depth() - value

    power_2 = 0
    power_3 = 0
    power_value = error * 70

    diff_value = 5 / (current_time + prev_time) + (error - prev_error)

    power_2 = clamp(power_value, 40, -40)
    power_3 = clamp(power_value, 40, -40)
    # Включаем двигатели
    auv.set_motor_power(2, power_2)
    auv.set_motor_power(3, power_3)

    prev_time = current_time
    prev_error = error


def find_violet_circle(image1):
    imageHSV1 = cv.cvtColor(image1, cv.COLOR_BGR2HSV)
    violet_hsv_min = (130, 50, 50)
    violet_hsv_max = (145, 255, 255)
    image_bin1 = cv.inRange(imageHSV1, violet_hsv_min, violet_hsv_max)
    cnt2, _, = cv.findContours(image_bin1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if cnt2:
        for c1 in cnt2:
            area1 = cv.contourArea(c1)
            if abs(area1) < 300:
                continue
            hull1 = cv.convexHull(c1)
            approx1 = cv.approxPolyDP(hull1, cv.arcLength(c1, True) * 0.02, True)

            if len(approx1) == 3:
                cv.drawContours(image, [c1], 0, (0, 0, 255))
            if len(approx1) == 4:
                cv.drawContours(image, [c1], 0, (0, 0, 255))
            moments = cv.moments(c1)
            try:
                x_violet = int(moments["m10"] / moments["m00"])
                y_violet = int(moments["m01"] / moments["m00"])
            except ZeroDivisionError:
                return False, 0, 0
            return True, x_violet, y_violet
    return False, 0, 0


blue2 = 0
orange2 = 0
violet2 = 0
green2 = 0

def raspoznavanie_bottom2(image, image1):
    global blue2
    global orange2
    global violet2
    global green2

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


    violet_mask1 = cv.inRange(image_HSV, low_hsv_violet, max_hsv_violet)
    cnt_violet1, _ = cv.findContours(violet_mask1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    violet_mask1 = cv.inRange(image_HSV2, low_hsv_violet, max_hsv_violet)
    cnt_violet1, _ = cv.findContours(violet_mask1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #cv.imshow('mask', violet_mask2)

    green_mask1 = cv.inRange(image_HSV, low_hsv_green, max_hsv_green)
    cnt_green1, _ = cv.findContours(green_mask1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    orange_mask1 = cv.inRange(image_HSV, low_hsv_orange, max_hsv_orange)
    cnt_orange1, _ = cv.findContours(orange_mask1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    global blue2
    global green2
    global violet2
    global orange2

    blue2 = 0
    green2 = 0
    violet2 = 0
    orange2 = 0

    if cnt_orange1:
        blue2 = 0
        green2 = 0
        violet2 = 0
        orange2 = 1

        blue2 = int(blue2)
        green2 = int(green2)
        violet2 = int(violet2)
        orange2 = int(orange2)
        #return True,  blue1, green1, violet1, orange1
    elif cnt_green1:
        blue2 = 0
        green2 = 1
        violet2 = 0
        orange2 = 0

        blue2 = int(blue2)
        green2 = int(green2)
        violet2 = int(violet2)
        orange2 = int(orange2)
    elif cnt_violet1:
        blue2 = int(0)
        green2= int(0)
        violet2 = int(1)
        orange2 = int(0)

        blue2 = int(blue2)
        green2 = int(green2)
        violet2 = int(violet2)
        orange2 = int(orange2)

    return blue2, green2, violet2, orange2

    cv.waitKey(5)






def raspoznavanie_bottom(image, image1):


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

        blue1 = int(blue1)
        green1 = int(green1)
        violet1 = int(violet1)
        orange1 = int(orange1)
        #return True,  blue1, green1, violet1, orange1
    elif cnt_orange:
        blue1 = 0
        green1 = 0
        violet1 = 0
        orange1 = 1

        blue1 = int(blue1)
        green1 = int(green1)
        violet1 = int(violet1)
        orange1 = int(orange1)
        #return True,  blue1, green1, violet1, orange1
    elif cnt_green:
        blue1 = 0
        green1 = 1
        violet1 = 0
        orange1 = 0

        blue1 = int(blue1)
        green1 = int(green1)
        violet1 = int(violet1)
        orange1 = int(orange1)
    elif cnt_violet:
        blue1 = int(0)
        green1 = int(0)
        violet1 = int(1)
        orange1 = int(0)

        blue1 = int(blue1)
        green1 = int(green1)
        violet1 = int(violet1)
        orange1 = int(orange1)

    return blue1, green1, violet1, orange1

    cv.waitKey(5)

def find_blue_sq_or_tr2(image1):
    imageHSV_blue = cv.cvtColor(image1, cv.COLOR_BGR2HSV)
    blue_hsv_min = (90, 50, 50)
    blue_hsv_max = (105, 255, 255)
    image_bin_blue = cv.inRange(imageHSV_blue, blue_hsv_min, blue_hsv_max)
    cnt_blue2, _, = cv.findContours(image_bin_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if cnt_blue2:
        for c_blue1 in cnt_blue2:
            area1 = cv.contourArea(c_blue1)
            if abs(area1) < 300:
                continue
            hull1 = cv.convexHull(c_blue1)
            approx1 = cv.approxPolyDP(hull1, cv.arcLength(c_blue1, True) * 0.02, True)

            if len(approx1) == 3:
                cv.drawContours(image, [c_blue1], 0, (0, 0, 255))
            if len(approx1) == 4:
                cv.drawContours(image, [c_blue1], 0, (0, 0, 255))
            moments = cv.moments(c_blue1)
            try:
                x_blue1 = int(moments["m10"] / moments["m00"])
                y_blue1 = int(moments["m01"] / moments["m00"])
            except ZeroDivisionError:
                return False, 0, 0
            return True, x_blue1, y_blue1
    return False, 0, 0

def find_blue_sq_or_tr3(image):
    imageHSV_blue = cv.cvtColor(image1, cv.COLOR_BGR2HSV)
    blue_hsv_min = (90, 50, 50)
    blue_hsv_max = (105, 255, 255)
    image_bin_blue = cv.inRange(imageHSV_blue, blue_hsv_min, blue_hsv_max)
    cnt_blue2, _, = cv.findContours(image_bin_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if cnt_blue2:
        for c_blue1 in cnt_blue2:
            area1 = cv.contourArea(c_blue1)
            if abs(area1) < 300:
                continue
            hull1 = cv.convexHull(c_blue1)
            approx1 = cv.approxPolyDP(hull1, cv.arcLength(c_blue1, True) * 0.02, True)

            if len(approx1) == 3:
                cv.drawContours(image, [c_blue1], 0, (0, 0, 255))
            if len(approx1) == 4:
                cv.drawContours(image, [c_blue1], 0, (0, 0, 255))
            moments = cv.moments(c_blue1)
            try:
                x_blue1 = int(moments["m10"] / moments["m00"])
                y_blue1 = int(moments["m01"] / moments["m00"])
            except ZeroDivisionError:
                return False, 0, 0
            return True, x_blue1, y_blue1
    return False, 0, 0

def find_green_sq_or_tr2(image1):
    imageHSV_green = cv.cvtColor(image1, cv.COLOR_BGR2HSV)
    green_hsv_min = (45, 50, 50)
    green_hsv_max = (75, 255, 255)
    image_bin_green = cv.inRange(imageHSV_green, green_hsv_min, green_hsv_max)
    cnt_green2, _, = cv.findContours(image_bin_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if cnt_green2:
        for c1 in cnt_green2:
            area1 = cv.contourArea(c1)
            if abs(area1) < 300:
                continue
            hull1 = cv.convexHull(c1)
            approx1 = cv.approxPolyDP(hull1, cv.arcLength(c1, True) * 0.02, True)
            if len(approx1) == 4:
                cv.drawContours(image1, [c1], 0, (0, 0, 255))
            moments = cv.moments(c1)
            try:
                x_green = int(moments["m10"] / moments["m00"])
                y_green = int(moments["m01"] / moments["m00"])
            except ZeroDivisionError:
                return False, 0, 0
            return True, x_green, y_green
    return False, 0, 0
c_green = 0

def find_orange_sq_or_tr2(image1):
    imageHSV_orange = cv.cvtColor(image1, cv.COLOR_BGR2HSV)
    orange_hsv_min = (10, 50, 50)
    orange_hsv_max = (25, 255, 255)
    image_bin_orange = cv.inRange(imageHSV_orange, orange_hsv_min, orange_hsv_max)
    cnt_orange2, _, = cv.findContours(image_bin_orange, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if cnt_orange2:
        for c_or in cnt_orange2:
            area1 = cv.contourArea(c_or)
            if abs(area1) < 300:
                continue
            hull1 = cv.convexHull(c_or)
            approx1 = cv.approxPolyDP(hull1, cv.arcLength(c_or, True) * 0.02, True)

            if len(approx1) == 3:
                cv.drawContours(image1, [c_or], 0, (0, 0, 255))
            if len(approx1) == 4:
                cv.drawContours(image1, [c_or], 0, (0, 0, 255))
            moments = cv.moments(c_or)
            try:
                x_orange = int(moments["m10"] / moments["m00"])
                y_orange = int(moments["m01"] / moments["m00"])
            except ZeroDivisionError:
                return False, 0, 0
            return True, x_orange, y_orange
    return False, 0, 0
c_green = 0
t = 0
g1 = 0
g2 = 0
c1 = 0
count2 = 0
vr1 =0
vr2 = 0
ndov = 0


def stab_on_violet_1( image1, x_center, y_center):
    found, x_violet, y_violet = find_violet_circle(image1)
    global vr
    global v
    global vr1
    global vr2
    if (vr < 1500) and found and(vr2 == 0):
        if (x_violet < x_center) and (x_center - x_violet > 40):
            auv.set_motor_power(1, 20)
        elif (x_center - x_violet <= 40):
            auv.set_motor_power(1, 0)
        if (x_violet > x_center) and (x_violet - x_center > 40):
            auv.set_motor_power(0, 20)
        elif (x_violet > x_center) and (x_violet - x_center <= 40):
            auv.set_motor_power(0, 0)
        vr += 1
    elif vr >= 1500 and found and vr2 ==0:
        auv.set_motor_power(1, 50)
        auv.set_motor_power(0, 50)
    elif (vr >= 1500) and (not found):
        vr2 = 1
        if (vr1 < 30):
            auv.set_motor_power(1, -50)
            auv.set_motor_power(0, -50)
            vr1 += 1
        elif (vr1>= 30) and (vr1 <= 31):
            print('Торпеда пошла')
            auv.shoot()
            auv.set_motor_power(0, 0)
            auv.set_motor_power(1, 0)
            vr1 += 1
        elif (vr1 > 31) and (vr1 < 200):
            auv.set_motor_power(0, -50)
            auv.set_motor_power(1, -50)
            vr1 += 1
        elif (vr1 == 200):
            auv.set_motor_power(0, 0)
            auv.set_motor_power(1, 0)
            v = 1
            return v



g3 = 0
def green_1(image1, x_center, y_center):
    global g
    global g1
    global g2
    global g3
    found, x_green, y_green = find_green_sq_or_tr2(image1)
    s = int(x_green - x_center)
    s1 = int(x_center - x_green)
    if found and (g3 != 1):
        if g1 < 900:
            if (x_center > x_green) and (s1 > 40):
                auv.set_motor_power(1, 20)
            elif (x_center >= x_green) and (s1 <= 40):
                auv.set_motor_power(1, 0)
            if (x_green > x_center) and (s > 40):
                auv.set_motor_power(0, 20)
            elif (x_green >= x_center) and (s <= 40):
                auv.set_motor_power(0, 0)
            g1 += 1
        if g1>= 900:
            auv.set_motor_power(0, 50)
            auv.set_motor_power(1, 50)
            g1 += 1
    elif (g1 >= 900) and (not found):
        g3 = 1
        if (g2 < 30):
            auv.set_motor_power(1, -50)
            auv.set_motor_power(0, -50)
            g2 += 1
        elif (g2 >= 29) and (g2 <= 31):
            print('Торпеда пошла')
            auv.shoot()
            auv.set_motor_power(0, 0)
            auv.set_motor_power(1, 0)
            g2 += 1
        elif (g2 > 30) and (g2 < 100):
            auv.set_motor_power(0, -50)
            auv.set_motor_power(1, -50)
            g2 += 1
        elif (g2 == 100):
            auv.set_motor_power(0, 0)
            auv.set_motor_power(1, 0)
            g = 1
            return g


or1 = 0
or2 =0
or3 = 0
def orange_1(image1, x_center, y_center):
    global oran
    global or1
    global or2
    global or3
    found, x_orange, y_orange = find_orange_sq_or_tr2(image1)
    if found and or2 == 0:
        if or1 < 700:
            if (x_center > x_orange) and ((x_center - x_orange) > 40):
                auv.set_motor_power(1, 20)
            elif (x_center >= x_orange) and ((x_center - x_orange) <= 40):
                auv.set_motor_power(1, 0)
            if (x_orange > x_center) and ((x_orange - x_center) > 40):
                auv.set_motor_power(0, 20)
            elif (x_orange >= x_center) and ((x_orange - x_center) <= 40):
                auv.set_motor_power(0, 0)
            or1 += 1
        elif or1 >= 700:
            auv.set_motor_power(0, 50)
            auv.set_motor_power(1, 50)
    elif (or1 >= 700) and (not found):
        or2 = 1
        if (or3 < 30):
            auv.set_motor_power(1, -50)
            auv.set_motor_power(0, -50)
            or3 += 1
        elif (or3 >= 30) and (or3 <= 31):
            auv.shoot()
            print('Торпеда пошла')
            auv.set_motor_power(0, 0)
            auv.set_motor_power(1, 0)
            or3 += 1
        elif (or3 > 31) and (or3 < 100):
            auv.set_motor_power(0, -50)
            auv.set_motor_power(1, -50)
            or3 += 1
        elif (or3 == 100):
            auv.set_motor_power(0, 0)
            auv.set_motor_power(1, 0)
            oran = 1
            return oran

no = 0
count = 0
no1 = 0
def prop_on_orange1(image1, x_center, y_center):
    global  count
    global oran
    global no
    global no1
    found, x_orange, y_orange = find_orange_sq_or_tr2(image1)
    x_center = int(x_center//1)
    #auv.set_motor_power(1, 60)
    if found and no1 != 1:
        if count < 400:
            if (x_center > x_orange) and (x_center - x_orange > 30):
                auv.set_motor_power(1, 20)
            elif (x_center > x_orange) and (x_center - x_orange <= 30):
                auv.set_motor_power(1, 0)
            if (x_orange > x_center) and (x_orange - x_center > 30):
                auv.set_motor_power(0, 20)
            elif (x_orange > x_center) and (x_orange - x_center <= 30):
                auv.set_motor_power(0, 0)
            count += 1
        elif count >=400:
            auv.set_motor_power(0, 100)
            auv.set_motor_power(1, 100)
            count += 1
    elif (not found) and (oran != 1) and count >=400:
        no1 = 1
        if no < 200:
            auv.set_motor_power(0, 100)
            auv.set_motor_power(1, 100)
            no += 1
        elif no >= 200:
            oran = 1
        return oran


def prop_on_green1(image1, x_center, y_center):
    global  count
    global gr
    global no
    found, x_green, y_green = find_green_sq_or_tr2(image1)
    x_center = int(x_center//1)
    #auv.set_motor_power(1, 60)
    if found:
        if count < 700:
            if (x_center > x_green) and (x_center - x_green > 30):
                auv.set_motor_power(1, 20)
            elif (x_center > x_green) and (x_center - x_green <= 30):
                auv.set_motor_power(1, 0)
            if (x_green > x_center) and (x_green - x_center > 30):
                auv.set_motor_power(0, 20)
            elif (x_green > x_center) and (x_green - x_center <= 30):
                auv.set_motor_power(0, 0)
            count += 1
        elif count >=700:
            auv.set_motor_power(0, 100)
            auv.set_motor_power(1, 100)
            count += 1
    elif (not found) and (gr != 1) and (count > 150):
        if no < 200:
            auv.set_motor_power(0, 100)
            auv.set_motor_power(1, 100)
            no += 1
        elif no >= 200:
            gr = 1
        return gr


no3 = 0
def prop_on_violet1(image1, x_center, y_center):
    global  count
    global vio
    global no3
    found, x_violet, y_violet = find_violet_circle(image1)
    x_center = int(x_center//1)
    #auv.set_motor_power(1, 60)
    if found:
        if count < 700:
            if (x_center > x_violet) and (x_center - x_violet > 30):
                auv.set_motor_power(1, 20)
            elif (x_center > x_violet) and (x_center - x_violet <= 30):
                auv.set_motor_power(1, 0)
            if (x_violet > x_center) and (x_violet - x_center > 30):
                auv.set_motor_power(0, 20)
            elif (x_violet > x_center) and (x_violet - x_center <= 30):
                auv.set_motor_power(0, 0)
            count += 1
        elif count >=700:
            auv.set_motor_power(0, 100)
            auv.set_motor_power(1, 100)
            count += 1
    elif (not found) and (vio != 1) and (count > 150):
        if no3 < 200:
            auv.set_motor_power(0, 100)
            auv.set_motor_power(1, 100)
            no3 += 1
        elif no3 >= 200:
            vio = 1
        return vio


vp = 0
count = 0
count1 = 0
f = True
grn = True
viot = True

v =0
g = 0
bl = 0
vio = 0
gr = 0
orange1 = 0
while f == True:
    keep_depth(1.3)
    time.sleep(0.02)
    if (auv.get_depth()<1.35) and (auv.get_depth()>1.25):
        auv.set_motor_power(2, 0)
        auv.set_motor_power(3, 0)
        count1 += 1
        auv.set_motor_power(1, 60)
        auv.set_motor_power(0, -20)
    if count1 >= 50:
        f = False
org = True
vlt = True
g = 0
oran = 0
v_count = 0
g_count = 0
or_count = 0
z1 = 0
y_center = 240/2
x_center = 320/2
image = auv.get_image_bottom()
image1 = auv.get_image_front()
if count == 0:
    blue1, green1, violet1, orange1 = raspoznavanie_bottom(image, image1)
    count += 1

if orange1 == 1:
    print('Указатель оранжевый')
    while org == True:
        image1 = auv.get_image_front()
        found1, x_violet, y_violet = find_violet_circle(image1)
        found2, x_green, y_green = find_green_sq_or_tr2(image1)
        found3, x_orange, y_orange = find_orange_sq_or_tr2(image1)
        if (orange1 == 1) and (((x_orange < x_violet) or (x_orange == 0)) or ((x_orange > x_violet) or (x_orange == 0))) and ((y_violet < y_green) or y_orange == 0 or y_green == 0 ):#Оранжевый слева,фиолетовый справа
            if v != 1:
                v = stab_on_violet_1(image1, x_center, y_center)
            if v == 1 and (v_count < 1600):
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                v_count += 1
            elif v_count >= 1600 and v_count<=1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                v_count += 1
            elif (v_count == 1602) and  (g!=1):
                keep_depth(3.20)
                if (auv.get_depth()<3.40) and (auv.get_depth()>2.90):
                    g = green_1(image1, x_center, y_center)
            elif g ==1 and g_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                g_count += 1
            elif g_count == 1600 and oran != 1:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                keep_depth(1.2)
                if auv.get_depth() <1.60 and auv.get_depth() > 1.00:
                    oran = prop_on_orange1(image1, x_center, y_center)
            elif oran == 1:
                keep_depth(0.03)
                if auv.get_depth() < 0.10 and auv.get_depth() > 0.01:
                    org = False
                    orange1 = 0

        elif (orange1 == 1) and (((x_violet < x_green) or (x_green == 0)) or ((x_violet > x_green) or (x_green == 0))) and ((y_orange < y_green) or y_orange == 0 or y_green == 0 ): #Фиолетовый слева, зелёный справа и Фиолетовый справа, зелёный слева
            if v != 1:
                v = stab_on_violet_1(image1, x_center, y_center)
            if v == 1 and (v_count < 1600):
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                v_count += 1
            elif v_count >= 1600 and v_count <= 1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                v_count += 1
            elif v_count == 1602 and g != 1:
                g = green_1(image1, x_center, y_center)
            elif g == 1 and (g_count < 1600):
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                g_count += 1
            elif g_count == 1600 and oran != 1:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                keep_depth(3.20)
                if (auv.get_depth() < 3.40) and (auv.get_depth() > 2.90):
                    oran = prop_on_orange1(image1, x_center, y_center)
            elif oran == 1:
                keep_depth(0.03)
                if auv.get_depth() < 0.10 and auv.get_depth() > 0.01:
                    org = False
                    orange1 = 0
        elif (((x_orange < x_green)or x_orange == 0) or ((x_orange > x_green) or x_orange == 0)) and ((y_green < y_violet) or y_violet == 0 or y_green == 0):#Оранжевый слева и зелёный справа и наоборот
            if g!=1:
                 g = green_1(image1, x_center, y_center)
            elif g == 1 and g_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                g_count += 1
            elif g_count >= 1600 and g_count <= 1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                g_count += 1
            elif g_count== 1602 and v != 1:
                keep_depth(3.20)
                if auv.get_depth()<3.40 and auv.get_depth()> 2.90:
                    v = stab_on_violet_1(image1, x_center, y_center)
            elif v == 1 and v_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                v_count += 1
            elif v_count >= 1600 and v_count <= 1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                v_count += 1
            elif v_count == 1602 and oran != 1:
                keep_depth(1.20)
                if auv.get_depth()<1.50 and auv.get_depth()>1.00:
                    oran = prop_on_orange1(image1, x_center, y_center)
            elif oran == 1:
                keep_depth(0.03)
                if auv.get_depth() < 0.10 and auv.get_depth() > 0.01:
                    org = False
                    orange1 = 0



if green1 == 1:
    print('Указатель зелёный')
    while grn == True:
        image = auv.get_image_bottom()
        image1 = auv.get_image_front()
        found1, x_violet, y_violet = find_violet_circle(image1)
        found2, x_green, y_green = find_green_sq_or_tr2(image1)
        found3, x_orange, y_orange = find_orange_sq_or_tr2(image1)
        if (green1 == 1) and (((x_violet < x_green) or (x_green == 0)) or ((x_violet > x_green) or (x_green == 0))) and ((y_orange>y_violet) or y_orange == 0 or y_violet == 0):#Фиолетовый слева, Зеленый справа  и Феолетовый справа, зеленый слева
            if v != 1:
                v = stab_on_violet_1(image1, x_center, y_center)
            if v == 1 and (v_count < 1800):
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                v_count += 1
            elif v_count >= 1800 and v_count <= 1801:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                v_count += 1
            elif(v_count == 1802) and (oran != 1):
                keep_depth(3.20)
                if (auv.get_depth() < 3.40) and (auv.get_depth() > 2.90):
                    oran = orange_1(image1, x_center, y_center)
            elif oran == 1 and or_count < 1900:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                or_count += 1
            elif or_count == 1900 and gr !=1:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                keep_depth(1.4)
                if auv.get_depth() < 1.50 and auv.get_depth() > 1.20:
                    gr = prop_on_green1(image1, x_center, y_center)
            elif gr == 1:
                keep_depth(0.03)
                if auv.get_depth() < 0.10 and auv.get_depth() > 0.01:
                    grn = False
                    green1 = 0

        elif (((x_orange > x_violet) or x_violet == 0) or ((x_orange < x_violet) or x_violet == 0)) and ( y_green > x_orange or y_green == 0 or y_orange == 0): # Оранжевый справа, фиолетовый слева и Фиолетовый справа, орагжевый слева
            if v != 1:
                v = stab_on_violet_1(image1, x_center, y_center)
            if v == 1 and (v_count < 1600):
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                v_count += 1
            elif v_count >= 1600 and v_count <= 1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                v_count += 1
            elif (v_count == 1602) and (oran != 1):
                oran = orange_1(image1, x_center, y_center)
            elif oran == 1 and or_count < 1900:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                or_count += 1
            elif or_count == 1900 and gr !=1:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                keep_depth(3.20)
                if auv.get_depth() <3.40 and auv.get_depth()>2.90:
                    gr = prop_on_green1(image1, x_center, y_center)
            elif gr == 1:
                keep_depth(0.03)
                if auv.get_depth() < 0.10 and auv.get_depth() > 0.01:
                    grn = False
                    green1 = 0
        elif (((x_green < x_orange) or x_orange == 0) or ((x_orange<x_green) or x_orange == 0)) and ((y_violet > y_green) or y_green == 0 or y_violet == 0):
            if oran != 1:
                oran = orange_1(image1, x_center, y_center)
            elif oran == 1 and or_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                or_count += 1
            elif or_count >= 1600 and or_count <=1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                or_count += 1
            elif or_count == 1602 and v!=1:
                keep_depth(3.20)
                if auv.get_depth() < 3.40 and auv.get_depth()>2.90:
                    v = stab_on_violet_1(image1, x_center, y_center)
            elif v == 1 and v_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                v_count += 1
            elif v_count >= 1600 and v_count <=1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, -0)
                v_count += 1
            elif v_count == 1602 and gr != 1:
                keep_depth(1.20)
                if auv.get_depth() < 1.50 and auv.get_depth() > 1.00:
                    gr = prop_on_green1(image1, x_center, y_center)
            elif gr == 1:
                keep_depth(0.10)
                if auv.get_depth()<0.15 and auv.get_depth()>0.01:
                    green1 = 0
                    grn = False

if violet1 == 1:
    print('Указатель фиолетовый')
    while vlt == True:
        image = auv.get_image_bottom()
        image1 = auv.get_image_front()
        found1, x_violet, y_violet = find_violet_circle(image1)
        found2, x_green, y_green = find_green_sq_or_tr2(image1)
        found3, x_orange, y_orange = find_orange_sq_or_tr2(image1)
        if (((x_orange < x_violet) or x_violet == 0)or ((x_orange > x_violet)or x_violet == 0)) and ((y_green > y_violet) or y_violet == 0 or y_green == 0):#Оранжевый слева, филетовый справа и наоборот
            if oran != 1:
                oran = orange_1(image1, x_center, y_center)
            elif oran == 1 and or_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                or_count += 1
            elif or_count >= 1600 and or_count<=1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                or_count += 1
            elif or_count == 1602 and g != 1:
                keep_depth(3.20)
                if auv.get_depth()<3.40 and auv.get_depth()>2.90:
                    g = green_1(image1, x_center, y_center)
            elif g == 1 and g_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                g_count += 1
            elif g_count >=1600 and g_count <= 1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                g_count += 1
            elif g_count == 1602 and vio != 1:
                keep_depth(1.20)
                if auv.get_depth()<1.50 and auv.get_depth()>1.00:
                    vio = prop_on_violet1(image1, x_center, y_center)
            elif vio == 1:
                keep_depth(0.10)
                if auv.get_depth() < 0.15 and auv.get_depth()>0.01:
                    violet = 0
                    vlt = False
        elif (((x_violet < x_green) or x_violet == 0) or ((x_violet > x_green) or x_violet == 0)) and ((y_green < y_orange) or y_green == 0 or y_orange == 0):#Фиолетовый слева, зеленый справа и наоборот
            if g != 1:
                g = green_1(image1, x_center, y_center)
            elif g == 1 and g_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                g_count+= 1
            elif g_count >= 1600 and g_count <= 1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                g_count += 1
            elif g_count == 1602 and oran != 1:
                keep_depth(3.20)
                if auv.get_depth()<3.40 and auv.get_depth()>2.90:
                    oran = orange_1(image1, x_center, y_center)
            elif oran == 1 and or_count<1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                or_count += 1
            elif or_count >= 1600 and or_count <= 1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                or_count += 1
            elif or_count == 1602 and vio != 1:
                keep_depth(1.20)
                if auv.get_depth()< 1.50 and auv.get_depth()>1.00:
                    vio = prop_on_violet1(image1, x_center, y_center)
            elif vio == 1:
                keep_depth(0.10)
                if auv.get_depth()<0.15 and auv.get_depth()>0.01:
                    violet1 = 0
                    vlt = False
        elif (((x_orange > x_green) or x_green == 0) and ((x_orange > x_green) or x_green == 0)) and ((y_green < y_violet) or y_green == 0 and y_violet == 0):
            if oran != 1:
                oran = orange_1(image1, x_center, y_center)
            elif oran == 1 and or_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                or_count += 1
            elif or_count >= 1600 and or_count<=1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                or_count+= 1
            elif or_count == 1602 and g != 1:
                g = green_1(image1, x_center, y_center)
            elif g == 1 and g_count < 1600:
                auv.set_motor_power(0, -50)
                auv.set_motor_power(1, -50)
                g_count += 1
            elif g_count>= 1600 and g_count <= 1601:
                auv.set_motor_power(0, 0)
                auv.set_motor_power(1, 0)
                g_count += 1
            elif g_count == 1602 and vio != 1:
                keep_depth(3.20)
                if auv.get_depth()<3.40 and auv.get_depth()>2.90:
                    vio = prop_on_violet1(image1, x_center, y_center)
            elif vio == 1:
                keep_depth(0.10)
                if auv.get_depth() < 0.15 and auv.get_depth()>0.01:
                    violet1 = 0
                    vlt = False
    cv.waitKey(5)
