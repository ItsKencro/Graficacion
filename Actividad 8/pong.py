import cv2 as cv
import numpy as np
import math

# Canvas
img = np.ones((500, 500, 3), np.uint8) * 255

# Pelota
pos_x, pos_y = 100, 100
vel_x, vel_y = 4, 6
radio = 6

# Obstáculo circular (centro)
obs_x, obs_y = 250, 250
obs_radio = 60

while True:
    img[:] = 255

    # Dibujar obstáculo
    cv.circle(img, (obs_x, obs_y), obs_radio, (200, 200, 200), 2)

    # Dibujar pelota
    cv.circle(img, (pos_x, pos_y), radio, (0, 0, 255), -1)

    # Actualizar posición
    pos_x += vel_x
    pos_y += vel_y

    # Rebote con bordes
    if pos_x - radio <= 0 or pos_x + radio >= img.shape[1]:
        vel_x *= -1
    if pos_y - radio <= 0 or pos_y + radio >= img.shape[0]:
        vel_y *= -1

    # ===== DISTANCIA EUCLIDIANA =====
    dist = math.sqrt((pos_x - obs_x) ** 2 + (pos_y - obs_y) ** 2)

    # Colisión con obstáculo circular
    if dist <= obs_radio + radio:
        vel_x *= -1
        vel_y *= -1

    # Mostrar distancia (para demostrar concepto)
    cv.putText(
        img,
        f"Distancia: {int(dist)}",
        (10, 20),
        cv.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 0),
        2
    )

    cv.imshow("Pong - Distancia Euclidiana", img)
    key = cv.waitKey(30)
    if key == 27:
        break

cv.destroyAllWindows()
