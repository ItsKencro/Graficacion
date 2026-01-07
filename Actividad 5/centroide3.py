import cv2 as cv
import numpy as np


def centroides_manual(imagen_binaria, area_min=200):
    # imagen_binaria: fondo negro (0) y figuras blancas (255)

    contornos, _ = cv.findContours(imagen_binaria, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    centroides = []

    for contorno in contornos:
        if cv.contourArea(contorno) < area_min:
            continue

        # máscara SOLO de esa figura
        mask = np.zeros_like(imagen_binaria)
        cv.drawContours(mask, [contorno], -1, 255, -1)

        # coordenadas de pixeles blancos (manual sin for-for)
        ys, xs = np.where(mask == 255)
        if len(xs) == 0:
            continue

        cx = int(xs.mean())
        cy = int(ys.mean())
        centroides.append((cx, cy))

    return centroides


# ====== FIGURAS DE PRUEBA ======
canvas = np.zeros((600, 800), np.uint8)

cv.circle(canvas, (150, 150), 60, 255, -1)
cv.rectangle(canvas, (300, 100), (450, 200), 255, -1)

puntos_triangulo = np.array([[500, 100], [650, 200], [550, 250]], np.int32)
cv.fillPoly(canvas, [puntos_triangulo], 255)

cv.ellipse(canvas, (150, 350), (80, 40), 0, 0, 360, 255, -1)

puntos_irregular = np.array([[350, 300],[420, 280],[480, 320],[470, 380],[400, 400],[340, 370],[320, 340]], np.int32)
cv.fillPoly(canvas, [puntos_irregular], 255)

cv.rectangle(canvas, (550, 350), (580, 450), 255, -1)
cv.rectangle(canvas, (580, 420), (650, 450), 255, -1)


# ====== CALCULAR Y DIBUJAR ======
centroides = centroides_manual(canvas, area_min=200)

out = cv.cvtColor(canvas, cv.COLOR_GRAY2BGR)
for i, (cx, cy) in enumerate(centroides, start=1):
    cv.circle(out, (cx, cy), 7, (0, 0, 255), -1)
    cv.putText(out, f"{i} ({cx},{cy})", (cx + 10, cy - 10),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv.imshow("Original", canvas)
cv.imshow("Centroides manual", out)
cv.waitKey(0)
cv.destroyAllWindows()
