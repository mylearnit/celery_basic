# Migrate and Run

	./manage.py migrate
	celery -A mysite beat -l INFO



```
celery -A mysite worker --loglevel=info -Q high_priority
celery -A mysite worker --loglevel=info -Q default
```