migrate:
	venv/Scripts/python manage.py makemigrations
	venv/Scripts/python manage.py migrate

entry-point:
    $env:DJANGO_SETTINGS_MODULE="vkr.settings" && venv\Scripts\python entrypoint.py

build:
	docker compose up -d --build
	docker compose exec django python manage.py makemigrations
	docker compose exec django python manage.py migrate
	docker compose exec django python manage.py load_statuses
	docker compose exec django python manage.py load_divisions
	docker compose exec django python manage.py load_categories
	docker compose exec django python manage.py load_admin

logs:
	docker compose logs

stop:
	docker compose stop




