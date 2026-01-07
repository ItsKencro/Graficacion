import cv2 as cv
import numpy as np


def centroide_global_sin_contornos(img_bin):
    ys, xs = np.where(img_bin == 255)
    if xs.size == 0:
        return None
    cx = int(xs.mean())
    cy = int(ys.mean())
    return (cx, cy)


def centroides_por_conectividad(img_bin, area_min=200):
    trabajo = img_bin.copy()
    h, w = trabajo.shape
    centroides = []
    areas = []
    n = 1

    for y in range(h):
        for x in range(w):
            if trabajo[y, x] != 255:
                continue

            mask = np.zeros((h + 2, w + 2), np.uint8)
            cv.floodFill(trabajo, mask, (x, y), 128)

            ys, xs = np.where(trabajo == 128)
            area = xs.size

            if area >= area_min:
                cx = int(xs.mean())
                cy = int(ys.mean())
                centroides.append((cx, cy))
                areas.append(area)
                n += 1

            trabajo[trabajo == 128] = 0

    return centroides, areas


canvas = np.zeros((500, 600), np.uint8)

cv.circle(canvas, (100, 100), 40, 255, -1)
cv.rectangle(canvas, (250, 150), (350, 250), 255, -1)
tri = np.array([[450, 80], [550, 150], [480, 180]], np.int32)
cv.fillPoly(canvas, [tri], 255)
irr = np.array([[150, 350], [200, 320], [280, 360], [250, 420], [180, 400]], np.int32)
cv.fillPoly(canvas, [irr], 255)

original = cv.cvtColor(canvas, cv.COLOR_GRAY2BGR)

cg = centroide_global_sin_contornos(canvas)
vista_global = original.copy()
if cg is not None:
    cv.circle(vista_global, cg, 9, (0, 0, 255), -1)
    cv.circle(vista_global, cg, 3, (255, 255, 255), -1)
    cv.putText(vista_global, f"Global {cg}", (cg[0] - 60, cg[1] - 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

centroides, areas = centroides_por_conectividad(canvas, area_min=200)
vista_sep = original.copy()

for i, (c, a) in enumerate(zip(centroides, areas), start=1):
    cv.circle(vista_sep, c, 8, (255, 0, 0), -1)
    cv.circle(vista_sep, c, 3, (255, 255, 255), -1)
    cv.putText(vista_sep, f"Fig{i} {c} A:{a}", (c[0] - 60, c[1] - 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

cv.imshow("Figuras", original)
cv.imshow("Centroide Global", vista_global)
cv.imshow("Centroides por Conectividad", vista_sep)

cv.waitKey(0)
cv.destroyAllWindows()
