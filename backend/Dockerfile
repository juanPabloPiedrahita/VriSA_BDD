# ------------------------------------------------------------------------------
# Dockerfile for VRISA Django Backend
#
# This container provides a fully configured environment for running the Django
# backend with support for:
# - GDAL / GEOS / PROJ (required for GIS and PostGIS features)
# - PostgreSQL utilities and headers
# - Python 3.12 (slim base image)
#
# Notes:
# - Installing GIS dependencies through apt-get is heavy (≈2GB), as these
#   libraries are not available via pip.
# - The container automatically applies migrations and runs the Django server.
# ------------------------------------------------------------------------------

FROM python:3.12-slim

# System dependencies required for Django GIS and PostGIS integrations.
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

# Application directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project
COPY . .

# Default command: apply migrations and start Django server
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]