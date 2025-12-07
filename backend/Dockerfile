FROM python:3.12-slim

#Instala dependencias y librerias necesarias para GIS y PostGIS en Django, ojo esto es pesado ya que usa apt-get ya que estas no se encuentran en pip. XD (ahi van como 2gb)
RUN apt-get update && apt-get install -y \
    gcc \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    proj-bin \
    libgeos-dev \
    libpq-dev \
    python3-dev \
    binutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
