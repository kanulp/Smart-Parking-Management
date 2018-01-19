import cv2
import numpy as np
import pickle

image = cv2.imread("park2.jpg")

img_canny = cv2.Canny(image, 100, 200)

img_gray = cv2.cvtColor(img_canny, cv2.COLOR_BAYER_BG2GRAY)

(thresh, img) = cv2.threshold(img_canny, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

with open ('Park2crs', 'rb') as fp:
    coordinates = pickle.load(fp)

with open ('Park2crsShow', 'rb') as fp2:
    coordinatesToShow = pickle.load(fp2)

coordinates = coordinates[:-1]
coordinatesToShow = coordinatesToShow[:-1]
#print(coordinates)

rowA = []
rowB = []
rowC = []
rowD = []

for item in coordinates[:14]:
    rowA.append(img[item[0]:item[1], item[2]:item[3]])

for item in coordinates[14:26]:
    rowB.append(img[item[0]:item[1], item[2]:item[3]])

for item in coordinates[26:34]:
    rowC.append(img[item[0]:item[1], item[2]:item[3]])

for item in coordinates[34:]:
    rowD.append(img[item[0]:item[1], item[2]:item[3]])

vacant = []
rowAshow = coordinatesToShow[:14]
rowBshow = coordinatesToShow[14:26]
rowCshow = coordinatesToShow[26:34]
rowDshow = coordinatesToShow[34:]

i = 0
for spot in rowA:
    row = "A"
    non = cv2.countNonZero(spot)
    if non < 50:
        vacant.append(row + str(i+1))
        pts = np.array(
            [[rowAshow[i][2], rowAshow[i][0]], [rowAshow[i][3], rowAshow[i][0]], [rowAshow[i][3], rowAshow[i][1]],
             [rowAshow[i][2], rowAshow[i][1]]], np.int32)
        cv2.polylines(image, [pts], True, (0, 255, 0), 2)
    else:
        pts = np.array(
            [[rowAshow[i][2], rowAshow[i][0]], [rowAshow[i][3], rowAshow[i][0]], [rowAshow[i][3], rowAshow[i][1]],
             [rowAshow[i][2], rowAshow[i][1]]], np.int32)
        cv2.polylines(image, [pts], True, (0, 0, 255), 2)
    i += 1
    print (non)
print ("\n")

i = 0
for spot in rowB:
    row = "B"
    non = cv2.countNonZero(spot)
    if non < 50:
        vacant.append(row + str(i+1))
        pts = np.array(
            [[rowBshow[i][2], rowBshow[i][0]], [rowBshow[i][3], rowBshow[i][0]], [rowBshow[i][3],
                rowBshow[i][1]], [rowBshow[i][2], rowBshow[i][1]]], np.int32)
        cv2.polylines(image, [pts], True, (0, 255, 0), 2)
    else:
        pts = np.array(
            [[rowBshow[i][2], rowBshow[i][0]], [rowBshow[i][3], rowBshow[i][0]], [rowBshow[i][3],
                    rowBshow[i][1]], [rowBshow[i][2], rowBshow[i][1]]], np.int32)
        cv2.polylines(image, [pts], True, (0, 0, 255), 2)
    i += 1
    print (non)
print ("\n")

i = 0
for spot in rowC:
    row = "C"
    non = cv2.countNonZero(spot)
    if non < 50:
        vacant.append(row + str(i+1))
        pts = np.array(
            [[rowCshow[i][2], rowCshow[i][0]], [rowCshow[i][3], rowCshow[i][0]], [rowCshow[i][3], rowCshow[i][1]],
             [rowCshow[i][2], rowCshow[i][1]]], np.int32)
        cv2.polylines(image, [pts], True, (0, 255, 0), 2)
    else:
        pts = np.array(
            [[rowCshow[i][2], rowCshow[i][0]], [rowCshow[i][3], rowCshow[i][0]], [rowCshow[i][3], rowCshow[i][1]],
             [rowCshow[i][2], rowCshow[i][1]]], np.int32)
        cv2.polylines(image, [pts], True, (0, 0, 255), 2)
    i += 1
    print (non)
print ("\n")

i = 0
for spot in rowD:
    row = "D"
    non = cv2.countNonZero(spot)
    if non < 50:
        vacant.append(row + str(i+1))
        pts = np.array(
            [[rowDshow[i][2], rowDshow[i][0]], [rowDshow[i][3], rowDshow[i][0]], [rowDshow[i][3], rowDshow[i][1]],
             [rowDshow[i][2], rowDshow[i][1]]], np.int32)
        cv2.polylines(image, [pts], True, (0, 255, 0), 2)
    else:
        pts = np.array(
            [[rowDshow[i][2], rowDshow[i][0]], [rowDshow[i][3], rowDshow[i][0]], [rowDshow[i][3], rowDshow[i][1]],
             [rowDshow[i][2], rowDshow[i][1]]], np.int32)
        cv2.polylines(image, [pts], True, (0, 0, 255), 2)
    i += 1
    print (non)
print ("\n")

print("Vacant spaces: ")
print(vacant)

cv2.imwrite('park2_thresh.jpg', img)

cv2.imshow('Result', image)
cv2.imwrite('Result.jpg', image)
cv2.imshow('Canny', img_canny)
cv2.imshow('Gray', img_gray)
cv2.imshow('Threshold', img)

cv2.waitKey(0)
cv2.destroyAllWindows()