import cv2
import numpy as np
import pickle

if __name__ == '__main__':
    im = cv2.imread("park2.jpg")

roiToShow = []

while True:
    fromCenter = False
    r = cv2.selectROI(im, fromCenter)

    imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    roiToShow.append([int(r[1]),int(r[1] + r[3]), int(r[0]),int(r[0] + r[2])])
    #print(int(r[1]),int(r[1] + r[3]), int(r[0]),int(r[0] + r[2]))

    key = cv2.waitKey(0) & 0xFF
    if key == ord("c"):
        break

#print(roi)

with open('Park2crsShow', 'wb') as fp:
    pickle.dump(roiToShow, fp)

with open ('Park2crsShow', 'rb') as fp:
    itemlist = pickle.load(fp)

itemlist = itemlist[:-1]
print(itemlist)


cv2.waitKey(0)
cv2.destroyAllWindows()