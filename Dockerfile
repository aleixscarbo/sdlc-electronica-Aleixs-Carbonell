# 1. El sustrato de silicio base: Usamos una versión oficial y ligera de Python.
FROM python:3.12-slim

# 2. El área de trabajo en el chip: Crea una carpeta interna llamada /app y nos mueve allí.
WORKDIR /app

# 3. La Lista de Materiales (BOM): Copiamos SOLO el archivo de dependencias primero.
COPY requirements.txt .

# 4. Soldar los componentes: Instalamos las librerías. 
# (--no-cache-dir evita guardar archivos temporales de instalación para que la imagen pese menos).
RUN pip install --no-cache-dir -r requirements.txt

# 5. Ruteo de pistas (El código fuente): Ahora sí, copiamos todo el resto de tu código a la carpeta /app.
COPY . .

# 6. Definir el Pin de Salida: Le decimos a Docker que este contenedor emitirá señales por el puerto 8000.
EXPOSE 8000

# 7. Energizar el chip: El comando exacto que se ejecutará cuando el contenedor se encienda.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]