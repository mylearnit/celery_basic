# Migrate and Run

	./manage.py migrate
	celery -A mysite worker -l INFO -B
