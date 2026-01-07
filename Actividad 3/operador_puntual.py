import cv2 as cv

# Cargar imagen en escala de grises
img = cv.imread("Actividad 3/cube.png", 0)

# Verificar que la imagen cargó correctamente
if img is None:
    print("Error: no se pudo cargar la imagen")
    exit()

# Mostrar imagen original
cv.imshow('Original', img)

# Obtener dimensiones
x, y = img.shape

# Operador puntual (umbral)
for i in range(x):
    for j in range(y):
        if img[i, j] > 150:
            img[i, j] = 255
        else:
            img[i, j] = 0

# Mostrar imagen procesada
cv.imshow('Salida binaria', img)

print("Dimensiones:", img.shape)
print("Filas:", x, "Columnas:", y)

cv.waitKey(0)
cv.destroyAllWindows()
