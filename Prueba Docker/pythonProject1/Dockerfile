# Usa la imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto de PyCharm al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Exponer el puerto 5000
EXPOSE 5000

# Comando por defecto para ejecutar tu aplicación
CMD ["python", "app.py"]