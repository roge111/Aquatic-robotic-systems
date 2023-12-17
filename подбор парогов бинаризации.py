import  cv2

def nothing(x):
    pass
cap = cv2.VideoCapture(0)

cv2.namedWindow("result")

cv2.createTrackbar('minh', 'result', 0, 255, nothing)
cv2.createTrackbar('ming', 'result', 0, 255, nothing)
cv2.createTrackbar('minr', 'result', 0, 255, nothing)

cv2.createTrackbar('maxh', 'result', 0, 255, nothing)
cv2.createTrackbar('maxg', 'result', 0, 255, nothing)
cv2.createTrackbar('maxr', 'result', 0, 255, nothing)

pedistran = cv2.imread("D:\\pp.jpg")

while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #cv2.imshow('hsv', hsv)

    minh = cv2.getTrackbarPos('minh', 'result')
    ming = cv2.getTrackbarPos('ming', 'result')
    minr = cv2.getTrackbarPos('minr', 'result')

    maxh = cv2.getTrackbarPos('maxh', 'result')
    maxg = cv2.getTrackbarPos('maxg', 'result')
    maxr = cv2.getTrackbarPos('maxr', 'result')

    #mask = cv2.inRange(hsv, (minh, ming, minr), (maxh,maxg, maxr))
    mask=cv2.inRange(pedistran, (minh, ming, minr), (maxh,maxg, maxr))

    cv2.imshow('mask', mask)

    result = cv2.bitwise_and(pedistran, pedistran, mask=mask)
    cv2.imshow('result', result)

    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()