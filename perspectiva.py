# José Manue Amestoy Lopez manuel.amestoy@udc.es
import cv2 as cv
import numpy as np
from campo2 import campo

def lines_cross(line1, line2):
    # Determina si dos líneas se cruzan
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0: return 0  # Colineal
        return 1 if val > 0 else 2  # Sentido horario(positivo) o antihorario(negativo  )

    p1, q1 = (line1[0], line1[1]), (line1[2], line1[3])
    p2, q2 = (line2[0], line2[1]), (line2[2], line2[3])

    # Encontrar las cuatro orientaciones necesarias para el caso general y especial
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # Caso general
    # o1 es diferente de o2: Esto indica que los puntos p2 y q2 (los extremos de line2) están en lados opuestos de line1.
    # o3 es diferente de o4: Esto indica que los puntos p1 y q1 (los extremos de line1) están en lados opuestos de line2.
    if o1 != o2 and o3 != o4:
        return True

    return False

def is_line_collision(line1, line2, line_thickness=10):
    # Determina si hay colisión entre dos líneas
    if lines_cross(line1, line2):
        return True
    
    dist = line_distance(line1, line2)
    return dist < line_thickness

def line_distance(line1, line2):
    # Calcula la distancia mínima entre dos líneas
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    # Línea 1
    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])
    d1 = p2 - p1

    # Línea 2
    p3 = np.array([x3, y3])
    p4 = np.array([x4, y4])
    d2 = p4 - p3

    # Calcular la distancia del punto a la línea si las líneas no se cruzan
    distances = []

    # Area del paralelogramo formado por el vector dirección de la línea y el vector
    # desde un punto extremo de la otra línea hasta un punto de la primera línea entre la 
    # longitud del vector direccion, asi se calcula la altura del paralelogramo
    distances.append(np.abs(np.cross(d1, p1 - p3)) / np.linalg.norm(d1))
    distances.append(np.abs(np.cross(d1, p1 - p4)) / np.linalg.norm(d1))
    distances.append(np.abs(np.cross(d2, p3 - p1)) / np.linalg.norm(d2))
    distances.append(np.abs(np.cross(d2, p3 - p2)) / np.linalg.norm(d2))

    return min(distances)

def detectar_lineas_siega(inImage, mask):
    # Copiar imagen de entrada para evitar modificar la original
    campo_image = inImage.copy()
    height, width = campo_image.shape[:2]

    # Límite para considerar un borde en la imagen
    border_limit = 1

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    mask_refined = cv.morphologyEx(mask, cv.MORPH_ERODE, kernel)
    gray_image = cv.cvtColor(campo_image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray_image, (21, 21), 0)

    # Ecuializar histograma para mejorar el contraste
    equalized = cv.equalizeHist(blurred)

    # Aplicar filtro Sobel en el eje X para detectar bordes verticales
    sobelx = cv.Sobel(equalized, cv.CV_64F, 1, 0, ksize=7)

    # Negar valores de Sobel para detectar bordes en ambas direcciones
    sobelx_neg = -sobelx
    #cv.imshow("Resulta", sobelx)

    # Umbralizar la imagen para resaltar bordes fuertes
    _, thresholded_pos = cv.threshold(np.abs(sobelx), 200, 255, cv.THRESH_BINARY)
    _, thresholded_neg = cv.threshold(np.abs(sobelx_neg), 200, 255, cv.THRESH_BINARY)

    # Combinar umbralizaciones y aplicar máscara refinada
    thresholded_combined = cv.bitwise_or(thresholded_pos, thresholded_neg, mask=mask_refined)
    thresholded_combined = cv.bitwise_and(thresholded_combined, thresholded_combined, mask=mask_refined)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (13,13))
    closing = cv.morphologyEx(thresholded_combined, cv.MORPH_ERODE, kernel)

    # Detectar líneas usando la transformada de Hough
    lines = cv.HoughLinesP(closing.astype(np.uint8), 1, np.pi / 180, threshold=200, minLineLength=100, maxLineGap=200)

    # Lista para mantener las líneas ya dibujadas
    drawn_lines = []

    # Procesar cada línea detectada
    if lines is not None:
        for line in lines:
            current_line = line[0]
            collision_found = False

            # Verificar si la línea está en el borde de la imagen
            if (current_line[0] <= border_limit or current_line[2] >= width - border_limit or
                current_line[1] <= border_limit or current_line[3] >= height - border_limit):
                continue

            # Verificar si la línea actual choca con líneas ya dibujadas
            for existing_line in drawn_lines:
                if is_line_collision(current_line, existing_line, line_thickness=10):
                    collision_found = True
                    break

            # Si no hay colisión, añadir la línea a la lista de líneas dibujadas
            if not collision_found:
                drawn_lines.append(current_line)

    # Dibujar las líneas finales en la imagen
    for line in drawn_lines:
        x1, y1, x2, y2 = line
        cv.line(campo_image, (x1, y1), (x2, y2), (0, 255, 255), 3)

    return campo_image

def run_perspectiva(inImage):
    imagen, mask = campo(inImage)
    resultado = detectar_lineas_siega(imagen, mask)
    #cv.imshow("Original", inImage)
    cv.imshow("Resultado perspectiva", resultado)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":

    inImage = cv.imread("Material_Futbol/174.jpg")

    imagen, mask = campo(inImage)
    resultado = detectar_lineas_siega(imagen, mask)

    #cv.imshow('Original', inImage)
    cv.imshow("Perspectiva", resultado)

    cv.waitKey(0)
    cv.destroyAllWindows()