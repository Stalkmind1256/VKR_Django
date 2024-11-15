migrate:
	venv/Scripts/python manage.py makemigrations
	venv/Scripts/python manage.py migrate

entry-point:
    $env:DJANGO_SETTINGS_MODULE="vkr.settings" && venv\Scripts\python entrypoint.py






