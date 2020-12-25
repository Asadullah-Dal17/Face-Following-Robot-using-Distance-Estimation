import cv2 as cv

camera = cv.VideoCapture(2)

while True:
    ret, frame = camera.read()
    cv.imshow("window", frame)
    key= cv.waitKey(1)
    if key == ord('q')or ret ==False:
        break
camera.release()
cv.destroyAllWindows()