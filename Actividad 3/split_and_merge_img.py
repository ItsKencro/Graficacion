import cv2 as cv
import numpy as np

img = cv.imread("Actividad 3/cube.jpg", 1)

if img is None:
    print("No se pudo cargar la imagen")
    exit()

img2 = np.zeros(img.shape[:2], dtype=np.uint8)

b, g, r = cv.split(img)

r2 = cv.merge([img2, img2, r])
g2 = cv.merge([img2, g, img2])
b2 = cv.merge([b, img2, img2])

img3 = cv.merge([b, r, g])

cv.imshow("original", img)
cv.imshow("rojo", r2)
cv.imshow("verde", g2)
cv.imshow("azul", b2)
cv.imshow("reordenado", img3)

cv.waitKey(0)
cv.destroyAllWindows()
