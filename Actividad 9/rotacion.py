import math
import cv2 as cv
import numpy as np

# Cargar imagen en escala de grises
img = cv.imread("Actividad 9/tr.png", 0)
if img is None:
    print("Error al cargar la imagen")
    exit()

h, w = img.shape

# Crear canvas más grande para evitar recortes
rotated_img = np.zeros((h * 2, w * 2), dtype=np.uint8)
H, W = rotated_img.shape

# Centro de la imagen original
cx, cy = w // 2, h // 2

# Centro del canvas destino
Cx, Cy = W // 2, H // 2

# Ángulo de rotación
angle = 45
theta = math.radians(angle)

cos_t = math.cos(theta)
sin_t = math.sin(theta)

# Rotación manual
for y in range(h):          # fila
    for x in range(w):      # columna
        # Coordenadas relativas al centro
        xr = x - cx
        yr = y - cy

        # Rotación
        x_rot = int(xr * cos_t - yr * sin_t)
        y_rot = int(xr * sin_t + yr * cos_t)

        # Trasladar al centro del nuevo canvas
        X = x_rot + Cx
        Y = y_rot + Cy

        # Verificar límites
        if 0 <= X < W and 0 <= Y < H:
            rotated_img[Y, X] = img[y, x]

# Mostrar resultados
cv.imshow("Imagen Original", img)
cv.imshow("Imagen Rotada (manual)", rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()
