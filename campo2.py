# José Manue Amestoy Lopez manuel.amestoy@udc.es
import cv2 as cv
import numpy as np

def campo(imagen):
    inImage = imagen.copy()

    # Convertir imagen al espacio de color HSV
    hsvImage = cv.cvtColor(inImage, cv.COLOR_BGR2HSV)

    # Definir el rango de color para el césped verde
    lower_region = np.array([25, 40, 40])
    upper_region = np.array([70, 255, 255])

    # Crear una máscara para identificar el césped
    mask = cv.inRange(hsvImage, lower_region, upper_region)

    # Operación de cierre para eliminar ruido y huecos en la máscara
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # Detectar contornos en la máscara
    contours, _ = cv.findContours(closing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Si se encuentran contornos, seleccionar el más grande
    if contours:
        largest_contour = max(contours, key=cv.contourArea)
        epsilon = 0.015 * cv.arcLength(largest_contour, True)
        approx = cv.approxPolyDP(largest_contour, epsilon, True)

        # Dibujar el polígono aproximado en una máscara en blanco
        blank = np.zeros(inImage.shape[:2], dtype='uint8')
        cv.drawContours(blank, [approx], -1, 255, thickness=cv.FILLED)

        # Combinar con la imagen original para obtener solo el área del campo
        resultado = cv.bitwise_and(inImage, inImage, mask=blank)
        return resultado, closing

    # Devolver la imagen original si no se detecta césped
    return inImage


def run_campo(imagen):

    resultado, _ = campo(imagen)

    cv.imshow('Original', imagen)
    cv.imshow("Campo", resultado)
    cv.imwrite("SOLOCAMPO.jpg", resultado)

    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":

    imagen = cv.imread('Material_Futbol/2.jpg')

    resultado, _ = campo(imagen)

    cv.imshow('Original', imagen)
    cv.imshow("Campo", resultado)
    #cv.imwrite("SOLOCAMPO.jpg", resultado)

    cv.waitKey(0)
    cv.destroyAllWindows()