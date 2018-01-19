import numpy as np
import cv2
import pickle

from pymongo import MongoClient, ASCENDING

client = MongoClient('localhost', 27017)

db = client['parking1']

posts = db.posts

result = posts.create_index([('spot_id', ASCENDING)], unique=True)

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

for coords in coordinates:
    print("\n")
    non = cv2.countNonZero(img[coords[0]:coords[1], coords[2]:coords[3]])  # (y1, y2, x1, x2)
    if non < 300:
        green.append([coords[0], coords[1], coords[2], coords[3]])
        spot = list(spots.keys())[list(spots.values()).index(coords)]
        time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        print("spot " + str(spot) + " added to green at " + str(time) + " sec")
        posts.update_one({
            'spot_id': spot},
            {'$set': {
                'spot_id': spot,
                'status': 'vacant',
                'time': time
            }}, upsert=True)
    else:
        red.append([coords[0], coords[1], coords[2], coords[3]])
        spot = list(spots.keys())[list(spots.values()).index(coords)]
        time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        print("spot " + str(spot) + " added to red at " + str(time) + " sec")
        posts.update_one({
            'spot_id': spot},
            {'$set': {
                'spot_id': spot,
                'status': 'occupied',
                'time': time
            }}, upsert=True)

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

    if checkRedSec:  # To check whether spots that are currently in Red are still Red, if not move to Green
        time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        if time == checkRedSec[0][1] + 1:
            coords = checkRedSec[0][0]
            non = cv2.countNonZero(img[coords[0]:coords[1], coords[2]:coords[3]])
            if non < 300:
                green.append(coords)
                print("\n")
                spot = list(spots.keys())[list(spots.values()).index(coords)]
                print("spot " + str(spot) + " moved to green at " + str(time) + " sec")
                red.remove(coords)
                checkRedSec.remove([coords, checkRedSec[0][1]])
                checkRed.remove(coords)
                posts.update_one({
                    'spot_id': spot},
                    {'$set': {
                        'spot_id': spot,
                        'status': 'vacant',
                        'time': time
                    }}, upsert=True)

    if checkGreenSec:
        time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        if time == checkGreenSec[0][1] + 10:
            coords = checkGreenSec[0][0]
            non = cv2.countNonZero(img[coords[0]:coords[1], coords[2]:coords[3]])
            if non > 300:
                red.append(coords)
                print("\n")
                spot = list(spots.keys())[list(spots.values()).index(coords)]
                print("spot " + str(spot) + " moved to red at " + str(time) + " sec")
                green.remove(coords)
                checkGreenSec.remove([coords, checkGreenSec[0][1]])
                checkGreen.remove(coords)
                posts.update_one({
                    'spot_id': spot},
                    {'$set': {
                        'spot_id': spot,
                        'status': 'occupied',
                        'time': time
                    }}, upsert=True)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()