FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt


#----------------------------------------
FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=products.settings \
    DEBUG=False

ARG SECRET_KEY=dummy-key
ARG POSTGRES_HOST=dummy-key
ARG POSTGRES_DB=key
ARG POSTGRES_USER=key
ARG POSTGRES_HOST=key
ARG POSTGRES_PORT=5432
ARG POSTGRES_PASSWORD=key

ENV SECRET_KEY=${SECRET_KEY}
ENV POSTGRES_HOST=${POSTGRES_HOST}
ENV POSTGRES_DB=${POSTGRES_DB}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_HOST=${POSTGRES_HOST}
ENV POSTGRES_PORT=${POSTGRES_PORT}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

RUN addgroup --system app && adduser --system --group app

COPY --from=builder /install /usr/local

COPY . .

COPY entrypoint.sh /entrypoint.sh

# Make it executable
RUN chmod +x /entrypoint.sh

# Use the script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

RUN python manage.py collectstatic --noinput

RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["gunicorn", "products.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
