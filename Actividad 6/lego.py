import cv2 as cv
import numpy as np

# Canvas blanco
img = np.ones((900, 700, 3), np.uint8) * 255

# =========================
# CABEZA
# =========================
cv.rectangle(img, (250, 80), (450, 280), (0, 255, 255), -1)   # Cabeza
cv.rectangle(img, (310, 40), (390, 80), (0, 255, 255), -1)   # Cuello LEGO

# Ojos
cv.circle(img, (310, 160), 18, (0, 0, 0), -1)
cv.circle(img, (390, 160), 18, (0, 0, 0), -1)

# Sonrisa
cv.ellipse(img, (350, 200), (45, 25), 0, 0, 180, (0, 0, 0), 4)

# =========================
# CUERPO
# =========================
cv.rectangle(img, (220, 280), (480, 520), (0, 0, 255), -1)

# Botones
cv.circle(img, (350, 330), 10, (255, 255, 255), -1)
cv.circle(img, (350, 380), 10, (255, 255, 255), -1)
cv.circle(img, (350, 430), 10, (255, 255, 255), -1)

# =========================
# BRAZOS
# =========================
cv.rectangle(img, (170, 300), (220, 480), (0, 0, 200), -1)
cv.rectangle(img, (480, 300), (530, 480), (0, 0, 200), -1)

# Manos
cv.circle(img, (195, 500), 25, (0, 255, 255), -1)
cv.circle(img, (505, 500), 25, (0, 255, 255), -1)

# =========================
# PIERNAS
# =========================
cv.rectangle(img, (260, 520), (330, 820), (255, 0, 0), -1)
cv.rectangle(img, (370, 520), (440, 820), (255, 0, 0), -1)

# =========================
# TEXTO (opcional)
# =========================
cv.putText(img, "LEGO - Primitivas OpenCV",
           (160, 870),
           cv.FONT_HERSHEY_SIMPLEX,
           0.9,
           (0, 0, 0),
           2)

# Mostrar resultado
cv.imshow("Lego con primitivas", img)
cv.waitKey(0)
cv.destroyAllWindows()
