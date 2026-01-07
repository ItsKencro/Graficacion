import cv2 as cv
import numpy as np

# =========================
# CONFIG
# =========================
RUTA_IMAGEN = "Actividad 5/assets/figura.png"  # <-- cambia esto si tu imagen se llama distinto
UMBRAL = 120  # umbral para binarizar (ajústalo si tu imagen sale mal)

# =========================
# 1) Cargar imagen
# =========================
img = cv.imread(RUTA_IMAGEN)
if img is None:
    raise FileNotFoundError(f"No se pudo cargar: {RUTA_IMAGEN}")

# Convertir a gris
gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# =========================
# 2) Binarizar (figura blanca, fondo negro)
# =========================
# Si tu figura sale al revés, cambia THRESH_BINARY por THRESH_BINARY_INV
_, binaria = cv.threshold(gris, UMBRAL, 255, cv.THRESH_BINARY)

# Limpieza opcional (quita ruido)
kernel = np.ones((3, 3), np.uint8)
binaria = cv.morphologyEx(binaria, cv.MORPH_OPEN, kernel, iterations=1)

# =========================
# 3) Contornos y centroides
# =========================
contornos, _ = cv.findContours(binaria, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

resultado = img.copy()
contador = 0

for c in contornos:
    area = cv.contourArea(c)
    if area < 200:   # ignora cositas pequeñas (ruido)
        continue

    M = cv.moments(c)
    if M["m00"] == 0:
        continue

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Dibujar contorno
    cv.drawContours(resultado, [c], -1, (0, 255, 0), 2)

    # Dibujar centroide
    cv.circle(resultado, (cx, cy), 7, (0, 0, 255), -1)
    cv.putText(
        resultado,
        f"C{contador}: ({cx},{cy})",
        (cx + 10, cy - 10),
        cv.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv.LINE_AA,
    )
    contador += 1

# =========================
# 4) Mostrar
# =========================
cv.imshow("Original", img)
cv.imshow("Binaria", binaria)
cv.imshow("Centroides", resultado)

print(f"Objetos detectados: {contador}")
cv.waitKey(0)
cv.destroyAllWindows()
