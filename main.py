# José Manue Amestoy Lopez manuel.amestoy@udc.es
import cv2
import os
from campo2 import campo, run_campo
from players import run_players
from perspectiva import run_perspectiva

def process_images_in_folder(folder_path):
    # Obtener la lista de archivos en la carpeta
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Iterar sobre cada archivo en la carpeta
    for image_file in image_files:
        # Construir la ruta completa de la imagen
        image_path = os.path.join(folder_path, image_file)

        # Leer la imagen
        inImage = cv2.imread(image_path)

        # Ejecutar las funciones
        #run_campo(inImage)
        #run_perspectiva(inImage)
        run_players(inImage)

if __name__ == "__main__":
    # Ruta de la carpeta
    folder_path = "Material_Futbol"

    # Ruta de la imagen
    inImage = cv2.imread('Material_Futbol/2.jpg')

    # Procesa todas las imágenes en la carpeta
    process_images_in_folder(folder_path)

    # Procesa la imagen
    #run_campo(inImage)
    #run_perspectiva(inImage)
    #run_players(inImage)


