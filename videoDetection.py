import numpy as np
import cv2
import pickle

cap = cv2.VideoCapture('vid.mp4')

vacant = []
with open ('vidCrs', 'rb') as fp:
    coordinates = pickle.load(fp)

with open ('vidCrsShow', 'rb') as fp2:
    coordinatesToShow = pickle.load(fp2)

coordinates = coordinates[:-1]
coordinatesToShow = coordinatesToShow[:-1]


while(cap.isOpened()):
    ret, frame = cap.read()

    #out.write(frame)

    img_canny = cv2.Canny(frame, 100, 200)

    img_gray = cv2.cvtColor(img_canny, cv2.COLOR_BAYER_BG2GRAY)

    (thresh, img) = cv2.threshold(img_canny, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    spots = []
    rowAshow = coordinatesToShow[:3]

    i = 0
    for item in coordinates:
        row = "A"
        non = cv2.countNonZero(img[item[0]:item[1], item[2]:item[3]])
        if non < 200:
            #vacant.append(row + str(i + 1))
            pts = np.array(
                [[rowAshow[i][2], rowAshow[i][0]], [rowAshow[i][3], rowAshow[i][0]], [rowAshow[i][3], rowAshow[i][1]],
                 [rowAshow[i][2], rowAshow[i][1]]], np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        else:
            pts = np.array(
                [[rowAshow[i][2], rowAshow[i][0]], [rowAshow[i][3], rowAshow[i][0]], [rowAshow[i][3], rowAshow[i][1]],
                 [rowAshow[i][2], rowAshow[i][1]]], np.int32)
            cv2.polylines(frame, [pts], True, (0, 0, 255), 2)
        i += 1
        print(non)
    print("\n")

    cv2.imshow('frame', frame)
    #cv2.imshow('canny',img_canny)
    #cv2.imshow('gray',img_gray)
    #cv2.imshow('thresh',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
