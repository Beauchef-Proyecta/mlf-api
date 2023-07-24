# MLF API
Esta api está dirigida a facilitar la comunicación con el robot del curso My Little Factory.
Con esta api se puede iniciar una comunicación para recibir un video mediante webRTC, mover el robot y activar los diferentes actuadores del robot.

## Instalación
Para el correcto uso de esta api es necesaria la version de python 3.9.2

Para la instalación se recomienda clonar este repo y crear un entorno virtual siguiendo los siguientes pasos:

1. Clonar el repo:

        git clone https://github.com/Beauchef-Proyecta/mlf-api

2. Crear un entorno virtual:

        python -m venv mlfApi

3. Activar el entorno virtual:

        .\mlfApi\Scripts\activate
4. Instalar los requirements:

        pip install -r requirements.txt


### Prueba correr los ejemplos para verificar que todo funciona:


    python moveRobotExample.py

Debería mover el robot de lado a lado
 

    python videoExample.py

Debería mostrarte lo que ve el robot!
