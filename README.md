# MAX_MIN_APP

# Configuración del Proyecto Django

Pasos para configurar y ejecutar el proyecto Django "MAX_MIN_APP".

1. Crear una nueva carpeta principal: `django-project`.
2. Abrir Git Bash o Windows CMD en la carpeta creada `django-project`.
3. Ejecutar: `git clone link-repositorio-github`.
4. Ejecutar: `cd MAX_MIN_APP/` en git-bash o `cd .\MAX_MIN_APP\` en Windows.
5. Ejecutar: `python -m venv .venv` para crear un entorno virtual.
6. Activar el entorno virtual:
   - Git Bash: Ejecutar: `source .venv/Scripts/activate`.
   - Windows CMD: Ejecutar: `.\.venv\Scripts\activate.bat`.
7. Instalar Django y otras librerías ejecutando: `pip install -r requirements.txt`.
8. Generar una `SECURE_KEY` de Django y configurarla:
   - Ejecutar: `python manage.py shell`.
   - Ejecutar: `from django.core.management.utils import get_random_secret_key`.
   - Ejecutar: `get_random_secret_key()`.
   - *COPIAR LA NUEVA CLAVE GENERADA*.
   - Ejecutar: `exit()`.
   - Abrir VSCode en la carpeta `C:..django-project/MAX_MIN_APP/`.
   - Crear un archivo llamado `.env` en la carpeta.
   - Abrir el archivo `.env` y agregar la nueva clave generada: `SECRET_KEY=KEY-GENERADA`.
9. Configurar la base de datos:
   - Abrir MySQL Workbench y conectarse usando un usuario existente (puede ser root/admin).
   - Crear la base de datos `Max_Min_App` con la siguiente consulta SQL: 
      ```
      CREATE DATABASE Max_Min_App;
      ```
   - En el archivo `.env` abierto anteriormente, agregar las credenciales de la base de datos y la conexión, el archivo .env ahora contiene:
     ```
     SECRET_KEY=KEY-GENERADA
     DB_NAME=Max_Min_App
     DB_USER=*usuario de la base de datos, root/admin u otro.
     DB_PASSWORD=*contraseña del usuario de la base de datos
     DB_HOST=localhost
     DB_PORT=3306
     ```
10. En Git Bash o Windows CMD, ejecutar: `python manage.py migrate`.
11. Ejecutar: `python manage.py createsuperuser` para crear un superusuario.
    - Ingresar un nombre de usuario, correo electrónico y contraseña (dos veces) para el usuario administrador de la aplicación.
12. Ejecutar: `python manage.py runserver` para iniciar el servidor de desarrollo.
13. Abrir el navegador web y visitar: `http://127.0.0.1:8000/`.
14. Iniciar sesión con el nombre de usuario y contraseña del usuario administrador recién creado.
15. También se puede acceder a `http://127.0.0.1:8000/admin` con las mismas credenciales para administrar otros usuarios desde la interfaz de administración de Django.
