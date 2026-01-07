import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# ===== Ajustes rápidos =====
AREA_MIN = 800          # sube/baja según tu cámara
SOLO_MAYOR = False      # True = solo el objeto más grande
KERNEL = np.ones((5, 5), np.uint8)

def encontrar_centroides(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # Limpieza para quitar puntitos/ruido
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, KERNEL, iterations=1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, KERNEL, iterations=2)

    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar por área
    contornos = [c for c in contornos if cv2.contourArea(c) >= AREA_MIN]

    # Si quieres solo el más grande
    if SOLO_MAYOR and len(contornos) > 0:
        contornos = [max(contornos, key=cv2.contourArea)]

    resultado = frame.copy()

    for idx, contorno in enumerate(contornos, start=1):
        area = cv2.contourArea(contorno)
        M = cv2.moments(contorno)
        if M["m00"] == 0:
            continue

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Contorno
        cv2.drawContours(resultado, [contorno], -1, (0, 255, 0), 2)

        # Centroide (punto)
        cv2.circle(resultado, (cx, cy), 8, (255, 0, 0), -1)
        cv2.circle(resultado, (cx, cy), 3, (255, 255, 255), -1)

        # Texto
        cv2.putText(resultado, f"ID {idx}", (cx + 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.putText(resultado, f"({cx},{cy})", (cx + 10, cy + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.putText(resultado, f"Area: {int(area)}", (cx + 10, cy + 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    return resultado, thresh


print("Presiona 'q' para salir")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar video")
        break

    frame = cv2.flip(frame, 1)

    resultado, thresh = encontrar_centroides(frame)

    cv2.imshow("Detector de Centroides", resultado)
    cv2.imshow("Umbralizacion", thresh)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()