import cv2
import numpy as np

cap = cv2.VideoCapture(0)

canvas = None
puntos = []

KERNEL = np.ones((5, 5), np.uint8)
AREA_MIN = 400

# Rango HSV (elige el objeto que usarás, por ejemplo uno VERDE)
# Si usas otro color, cambia estos valores
LOW = np.array([40, 50, 50])
HIGH = np.array([80, 255, 255])

paleta = {
    1: (0, 0, 255),     # rojo
    2: (255, 0, 0),     # azul
    3: (0, 255, 0),     # verde
    4: (0, 255, 255),   # amarillo
}
color_actual = 3  # verde por defecto


def detectar_punta(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, LOW, HIGH)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return None, mask

    c = max(contornos, key=cv2.contourArea)
    area = cv2.contourArea(c)
    if area < AREA_MIN:
        return None, mask

    M = cv2.moments(c)
    if M["m00"] == 0:
        return None, mask

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    cv2.drawContours(frame, [c], -1, (255, 255, 255), 2)
    cv2.circle(frame, (cx, cy), 8, (255, 255, 255), -1)

    return (cx, cy), mask


ret, frame = cap.read()
if ret:
    canvas = np.zeros_like(frame)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = np.zeros_like(frame)

    punto, mask = detectar_punta(frame)

    if punto is not None:
        puntos.append(punto)

        # Limitar historial
        if len(puntos) > 80:
            puntos.pop(0)

        # Dibujar trazo suave
        if len(puntos) > 1:
            cv2.line(canvas, puntos[-2], puntos[-1], paleta[color_actual], 8, cv2.LINE_AA)
    else:
        # Si se pierde, no cortamos de inmediato: dejamos “pausa”
        if len(puntos) > 0:
            puntos.pop(0)

    resultado = cv2.addWeighted(frame, 0.75, canvas, 0.9, 0)

    cv2.putText(resultado, "1 Rojo  2 Azul  3 Verde  4 Amarillo", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(resultado, "c Limpiar | q Salir", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    cv2.imshow("Varita Magica", resultado)
    cv2.imshow("Mascara", mask)

    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        break
    if k == ord("c"):
        canvas = np.zeros_like(frame)
        puntos = []
    if k in [ord("1"), ord("2"), ord("3"), ord("4")]:
        color_actual = int(chr(k))

cap.release()
cv2.destroyAllWindows()
