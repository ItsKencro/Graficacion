import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Esperar a que la cámara se estabilice
cv2.waitKey(2000)

# Capturar el fondo
ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo")
    cap.release()
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango de color verde (capa)
    lower_green = np.array([80, 40, 40])
    upper_green = np.array([145, 255, 255])

    # Máscara del color verde
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_inv = cv2.bitwise_not(mask)

    # Parte visible del cuerpo
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Parte del fondo que reemplaza el color verde
    res2 = cv2.bitwise_and(background, background, mask=mask)

    # Combinar ambas imágenes
    final_output = cv2.add(res1, res2)

    cv2.imshow("Capa de Invisibilidad", final_output)
    cv2.imshow("Mascara", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
