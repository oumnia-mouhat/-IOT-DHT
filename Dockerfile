FROM python:3.12-slim

WORKDIR /app

COPY projet/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY projet/ .

# Collecte des fichiers statiques pour prod
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "projet.wsgi:application", "--bind", "0.0.0.0:8000"]
