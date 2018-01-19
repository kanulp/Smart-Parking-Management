import numpy as np
import cv2
import pickle

cap = cv2.VideoCapture('vid.mp4')

vacant = []
with open('vidCrs', 'rb') as fp:
    coordinates = pickle.load(fp)

with open('vidCrsShow', 'rb') as fp2:
    coordinatesToShow = pickle.load(fp2)

coordinates = coordinates[:-1]
coordinatesToShow = coordinatesToShow[:-1]

ret0, frame0 = cap.read()

img_canny0 = cv2.Canny(frame0, 100, 200)

img_gray0 = cv2.cvtColor(img_canny0, cv2.COLOR_BAYER_BG2GRAY)

(thresh0, img) = cv2.threshold(img_canny0, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

red = []
green = []
checkRed = []
checkGreen = []
checkRedSec = []
checkGreenSec = []
spots = {}

i = 1
for coords in coordinates:
    spots[i] = coords
    i += 1

print(spots)

for coords in coordinates:
    print("\n")
    non = cv2.countNonZero(img[coords[0]:coords[1], coords[2]:coords[3]])  # (y1, y2, x1, x2)
    if non < 300:
        green.append([coords[0], coords[1], coords[2], coords[3]])
        #print(coords)
        spot = list(spots.keys())[list(spots.values()).index(coords)]
        print("spot ")
        print(spot)
        print("added to green at")
        print(round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0))
    else:
        red.append([coords[0], coords[1], coords[2], coords[3]])
        #print(coords)
        spot = list(spots.keys())[list(spots.values()).index(coords)]
        print("spot ")
        print(spot)
        print("added to red at")
        print(round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0))

while cap.isOpened():
    ret, frame = cap.read()

    img_canny = cv2.Canny(frame, 100, 200)

    img_gray = cv2.cvtColor(img_canny, cv2.COLOR_BAYER_BG2GRAY)

    (thresh, img) = cv2.threshold(img_canny, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    for coords in red:
        if coords not in checkRed:
            non = cv2.countNonZero(img[coords[0]:coords[1], coords[2]:coords[3]])
            if non < 300:
                checkRedSec.append([coords, round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)])
                checkRed.append(coords)

    for coords in green:
        if coords not in checkGreen:
            non = cv2.countNonZero(img[coords[0]:coords[1], coords[2]:coords[3]])
            if non > 300:
                checkGreenSec.append([coords, round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)])
                checkGreen.append(coords)

    if checkRedSec:      # To check whether spots that are currently in Red are still Red, if not move to Green
        if round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0) == checkRedSec[0][1] + 1:
            coords = checkRedSec[0][0]
            non = cv2.countNonZero(img[coords[0]:coords[1], coords[2]:coords[3]])
            if non < 300:
                green.append(coords)
                print("\n")
                print(coords)
                print("added to green at")
                print(checkRedSec[0][1] + 1)
                red.remove(coords)
                checkRedSec.remove([coords, checkRedSec[0][1]])
                checkRed.remove(coords)

    if checkGreenSec:
        if round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0) == checkGreenSec[0][1] + 10:
            coords = checkGreenSec[0][0]
            non = cv2.countNonZero(img[coords[0]:coords[1], coords[2]:coords[3]])
            if non > 300:
                red.append(coords)
                print("\n")
                print(coords)
                print("added to red at")
                print(checkGreenSec[0][1] + 10)
                green.remove(coords)
                checkGreenSec.remove([coords, checkGreenSec[0][1]])
                checkGreen.remove(coords)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()