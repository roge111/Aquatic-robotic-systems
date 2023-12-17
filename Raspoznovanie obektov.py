import cv2 as cv



def ob_zv(blue1, green1, violet1, orange1, image):
    if blue1 == 1:
        imageHSV_blue = cv.cvtColor(image, cv.COLOR_BGR2HSV)
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
                    print('Треугольник')
                    cv.drawContours(image, [c_blue1], 0, (0, 0, 255))
                if len(approx1) == 4: #определить квадрат или прямоугольник
                    cv.drawContours(image, [c_blue1], 0, (0, 0, 255))
                if len(approx1) > 4:
                    print('Круг')
                    cv.drawContours(image, [c_blue1], 0, (0, 0, 255))
                moments = cv.moments(c_blue1)
                try:
                    x_blue1 = int(moments["m10"] / moments["m00"])
                    y_blue1 = int(moments["m01"] / moments["m00"])
                except ZeroDivisionError:
                    return False, 0, 0
                return True, x_blue1, y_blue1
        return False, 0, 0
    elif green1 == 1:
        imageHSV_green = cv.cvtColor(image, cv.COLOR_BGR2HSV)
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
                if len(approx1) == 4:#определить квадрат или прямоугольник
                    cv.drawContours(image, [c1], 0, (0, 0, 255))
                if len(approx1):
                    print('Круг')
                    cv.drawContours(image, [c1], 0, (0, 0, 255))
                moments = cv.moments(c1)
                try:
                    x_green = int(moments["m10"] / moments["m00"])
                    y_green = int(moments["m01"] / moments["m00"])
                except ZeroDivisionError:
                    return False, 0, 0
                return True, x_green, y_green
        return False, 0, 0
    elif violet1 == 1:
        imageHSV1 = cv.cvtColor(image, cv.COLOR_BGR2HSV)
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
                if len(approx1) == 4: #определить квадрат или прямоугольник
                    cv.drawContours(image, [c1], 0, (0, 0, 255))
                if len(approx1) >4:
                    print('Круг')
                    cv.drawContours(image, [c1], 0, (0, 0, 255))
                moments = cv.moments(c1)
                try:
                    x_violet = int(moments["m10"] / moments["m00"])
                    y_violet = int(moments["m01"] / moments["m00"])
                except ZeroDivisionError:
                    return False, 0, 0
                return True, x_violet, y_violet
        return False, 0, 0
    elif orange1 == 1:
        imageHSV_orange = cv.cvtColor(image, cv.COLOR_BGR2HSV)
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
                    cv.drawContours(image, [c_or], 0, (0, 0, 255))
                if len(approx1) == 4: #определить квадрат или прямоугольник
                    cv.drawContours(image, [c_or], 0, (0, 0, 255))
                if len(approx1) > 4:
                    print('Круг')
                    cv.drawContours(image, [c_or], 0, (0, 0, 255))
                moments = cv.moments(c_or)
                try:
                    x_orange = int(moments["m10"] / moments["m00"])
                    y_orange = int(moments["m01"] / moments["m00"])
                except ZeroDivisionError:
                    return False, 0, 0
                return True, x_orange, y_orange
        return False, 0, 0
