FROM python:3.9-slim

# Instalar las dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libxcursor1 \
    libxss1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgtk-3-0 \
    chromium-driver \
    google-chrome-stable

WORKDIR /app

# Copiar los archivos
COPY . .

# Instalar las dependencias de Python
RUN pip install -r requirements.txt

# Exponer el puerto para la aplicación Flask
EXPOSE 5001

# Ejecutar la aplicación
CMD ["python", "app.py"]
