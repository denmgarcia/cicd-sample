
### Added .env
for purpose testing only, in prod secret should be kept confidential and it should not be commit in version control.

### Run in local env

~$ uv run manage.py migrate
~$ uv run manage.py runserver

### To create superuser
~$ uv run manage.py createsuperuser


### API Resource
django.http

### Create Test data
POST http://localhost:8000/insurance/test/