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

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system app && adduser --system --group app

COPY --from=builder /install /usr/local

COPY . .

ARG SECRET_KEY=test
ARG DJANGO_SETTINGS_MODULE=myproject.settings 
ARG DEBUG=False

ENV SECRET_KEY=${SECRET_KEY}
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
ENV DEBUG=${DEBUG}
ENV POSTGRES_DB=placeholder
ENV POSTGRES_USER=placeholder
ENV POSTGRES_PASSWORD=placeholder
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432

RUN python manage.py collectstatic --noinput





RUN python manage.py collectstatic --noinput

RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["gunicorn", "products.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
