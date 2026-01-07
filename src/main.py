import cv2 as cv
import numpy as np

img = cv.imread("assets/image.png", cv.IMREAD_COLOR)

if img is None:
    raise FileNotFoundError("assets/image.png")

img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("img2a", img2)

h, w = img2.shape[:2]
print(h, w)

lut = np.arange(256, dtype=np.uint8)
lut = 255 - lut
img2 = cv.LUT(img2, lut)

cv.imshow("img2b", img2)

img3 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img4 = cv.cvtColor(img, cv.COLOR_BGR2BGRA)

cv.imshow("img", img)
cv.imshow("img2", img2)
cv.imshow("img3", img3)
cv.imshow("img4", img4)

cv.waitKey(0)
cv.destroyAllWindows()