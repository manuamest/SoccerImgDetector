# José Manue Amestoy Lopez manuel.amestoy@udc.es
import cv2
import numpy as np
from matplotlib import pyplot as plt
from campo2 import campo
from perspectiva import detectar_lineas_siega

def is_collision(rect1, rect2):
    # Verifica si hay colisión entre dos rectángulos
    # rect1 y rect2 son tuplas de la forma (x, y, w, h)
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    # Verificar si algún lado de un rectángulo está más allá del lado correspondiente del otro
    if x1 > x2 + w2 or x2 > x1 + w1:
        return False
    if y1 > y2 + h2 or y2 > y1 + h1:
        return False
    return True

def remove_field_lines(image):
    # Detectar líneas con Hough
    lines = cv2.HoughLinesP(image, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Dibujar líneas en la imagen con el color del césped
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 0), 5)

    return image

def players(inImage, inImage2):

    image = inImage2.copy()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Aplicar deteccion de bordes
    edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)

    # Eliminar las lineas blancas
    playerContours = remove_field_lines(edges)

    # Encontrar contornos (jugadores, pelota y arbitro)
    contours, _ = cv2.findContours(playerContours.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow('Player Contours', playerContours)

    # Lista para mantener los rectángulos ya dibujados
    drawn_rectangles = []
    
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        
        # Detectar jugadores y arbitros
        if h > w and w >= 5 and h > 5 and w < 100 and h < 100:

            if h < 2 * w:
                # Ajustar la altura para mantener la proporción
                h = int(2 * w)  

            # Ajustar el tamaño del rectángulo
            padding = 16
            new_x = max(x - padding, 0)
            new_y = max(y - padding, 0)
            new_w = min(w + 2 * padding, image.shape[1] - new_x)
            new_h = min(h + 2 * padding, image.shape[0] - new_y)
            
            # Crear un nuevo rectángulo candidato
            new_rect = (new_x, new_y, new_w, new_h)

            # Comprobar si el nuevo rectángulo colisiona con los rectángulos existentes
            collision = any(is_collision(new_rect, r) for r in drawn_rectangles)
            
            if not collision:
                # Si no hay colisión, dibujar el rectángulo y añadirlo a la lista
                cv2.rectangle(image, (new_x, new_y), (new_x + new_w, new_y + new_h), (255, 0, 0), 2)
                drawn_rectangles.append(new_rect)
        else:
            # Comprobar si el rectángulo actual está dentro de algún rectángulo de jugador
            current_rect = (x, y, w, h)
            inside_another = any(is_collision(current_rect, r) for r in drawn_rectangles)
            
            # Detectar pelota
            if not inside_another and w < 8 and h < 7 and w > 3 and h > 3:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)

    return image

def run_players(inImage):

    imagen, mask = campo(inImage)
    
    imagen2 = detectar_lineas_siega(imagen, mask)

    resultado = players(imagen, imagen2)

    # Mostrar la imagen con las detecciones
    cv2.imshow("Original", inImage)
    cv2.imshow("Campo", imagen)
    cv2.imshow("lineassiega", imagen2)
    cv2.imshow('Player Detection', resultado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":

    inImage = cv2.imread("Material_Futbol/99.jpg")

    imagen, mask = campo(inImage)
    
    imagen2 = detectar_lineas_siega(imagen, mask)

    resultado = players(imagen, imagen2)

    # Mostrar la imagen con las detecciones
    cv2.imshow("Original", inImage)
    cv2.imshow("Campo", imagen)
    cv2.imshow("lineassiega", imagen2)
    cv2.imshow('Player Detection', resultado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()