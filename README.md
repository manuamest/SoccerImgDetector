# Esquema Global del Método

## Introducción:
Este documento presenta un esquema detallado del sistema de detección de objetos en imágenes de partidos de fútbol, cabe destacar que la evaluación se ha hecho únicamente con las 20 imágenes de prueba que se han proporcionado.

## Objetivo Principal:
Desarrollar un sistema avanzado para la detección de objetos (campo, balón, jugadores), líneas de siega y el campo en imágenes de partidos de fútbol, abordando subproblemas.

![Ejemplo imagen original y resultado](https://github.com/manuamest/SoccerImgDetector/blob/main/ORIGINALRESULTADO.png)

## Subproblemas y Metodologías:

### 1. Metodología y Evaluación de la Detección del Terreno de Juego:
- **Metodología:** Implementación de la transformación de color a espacio HSV y filtrado por color para aislar el césped (esto debido a que el césped es de color verde siempre), utilizando una máscara basada en el contorno más grande de la imagen (el contorno del campo siempre va a ser el más grande en todas las imágenes).
- **Evaluación:** Se logró una identificación precisa del área del césped en la mayoría de los casos. Sin embargo, en algunas imágenes, los carteles fueron erróneamente identificados como parte del campo, afectando la detección de objetos.

#### Resultados de la Predicción:
- **Campo de Fútbol**:
  - Predicción: Campo de Fútbol
  - Real: Campo de Fútbol 15 1
  - Real: No Campo de Fútbol 4 0
  - Precisión: 78.95%. Recall (Sensibilidad): 93.75%.
- **Problema:** Mala detección en los bordes del campo.
- **Mejora Sugerida:** Ajustar más los valores para la captura del verde y utilizar operadores morfológicos para deshacerse de el área sobrante o capturar la restante. Otra opción sería usar una detección más precisa de los bordes del campo y calcular la media de los bordes para ajustarlos a rectas.

### 2. Análisis de la Localización y orientación de las Líneas de Siega:
- **Metodología:** Uso de filtros gaussiano y Sobel (para aumentar el contraste de las líneas y detectar los bordes, que corresponden a las líneas y otros), junto con la transformada de Hough (con el fin de detectar la forma de las líneas para unirlas), optimizados con otras funciones (como la detección de colisiones entre líneas y la longitud).
- **Evaluación:** Las líneas detectadas ofrecen una comprensión clara de la perspectiva del campo. Los errores principales se derivan de la falta de detección de algunas líneas.

#### Resultados de la Predicción:
- **Línea de Siega**:
  - Predicción: Línea de Siega
  - Real: Línea de Siega 150 17
  - Real: No Línea de Siega 2 0
  - Precisión: 98.68%. Recall (Sensibilidad): 89.82%.
- **Problema:** Líneas demasiado cortas o falta de líneas.
- **Mejora Sugerida:** Implementar funciones que alarguen las líneas y las corten en los bordes del campo, añadir también funciones que se aseguren de dibujar líneas cuando hay dos líneas separadas a una distancia mucho mayor a la media, ajustar más los parámetros de la detección de líneas.

### 3. Estrategias para la Detección de Objetos en el Campo:
- **Metodología:** Combinación de técnicas de detección de bordes (Canny para detectar los bordes en la imagen que se corresponden a los jugadores) y contornos (findContours para iterar sobre los jugadores y dibujar sobre ellos), optimizadas para evitar superposiciones.
- **Evaluación:** La metodología resultó eficaz para identificar jugadores, árbitros y el balón, aunque requiere mejoras para una distinción más precisa de estos elementos.

#### Resultados de la Predicción:
- **Jugador**:
  - Predicción: Jugador
  - Real: Jugador 255 23
  - Real: No Jugador 30 0
  - Precisión: 89.47%. Recall (Sensibilidad): 91.73%.
- **Problema:** Dificultades en la detección precisa de jugadores y balones.
- **Mejora Sugerida:** Implementación de algoritmos de reconocimiento de patrones y aprendizaje automático para una clasificación más precisa de los jugadores y la pelota

## Ejecucion
Se pueden ejecutar los scripts independientemente con el objetivo de evaluar los subproblemas o ejecutar el programa general.
```
git clone git@github.com:manuamest/SoccerImgDetector.git
cd SoccerImgDetector
python3 main.py
```

---

*Visión Artificial 2023-2024*  
*Memoria VA Detección de campo, balón y jugadores de fútbol*  
*José Manuel Amestoy López*  
*manuel.amestoy@udc.es*
