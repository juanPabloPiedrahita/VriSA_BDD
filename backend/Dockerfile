FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin gcc python3-dev musl-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
