dev: uv run python manage.py runserver

dev0: uv run python manage.py runserver 0.0.0.0:8000

migrate: uv run python manage.py migrate

makemigrations: uv run python manage.py makemigrations

superuser: uv run python manage.py createsuperuser

shell: uv run python manage.py shell

test: uv run python manage.py test

app name: uv run python manage.py startapp {{name}}
