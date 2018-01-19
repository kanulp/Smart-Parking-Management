import numpy as np
import cv2

park = cv2.imread('park.jpg')
park2 = cv2.imread('park2.jpg')
park3 = cv2.imread('park3.jpg')
park5 = cv2.imread('frame.jpg')

edges = cv2.Canny(park, 200, 300)
edges2 = cv2.Canny(park2, 100, 200)
edges3 = cv2.Canny(park3, 100, 200)
edges5 = cv2.Canny(park5, 200, 300)

cv2.imshow('Edges', edges)
cv2.imshow('Edges2', edges2)
cv2.imshow('Edges3', edges3)
cv2.imshow('Edges5', edges5)

cv2.imwrite('edges1.jpg', edges)
cv2.imwrite('edges2.jpg', edges2)
cv2.imwrite('edges3.jpg', edges3)
cv2.imwrite('frameThresh.jpg', edges5)

cv2.waitKey(0)
cv2.destroyAllWindows()