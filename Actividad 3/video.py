import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break

    cv.imshow("video", img)

    # NEGATIVO (invertir colores)
    negativo = 255 - img
    cv.imshow("negativo", negativo)

    # SPLIT & MERGE (reordenar canales)
    b, g, r = cv.split(img)
    img3 = cv.merge([b, r, g])  # B R G (cambio de orden)
    cv.imshow("img3", img3)

    k = cv.waitKey(1) & 0xFF
    if k == 27:  # ESC
        break

cap.release()
cv.destroyAllWindows()
