run:
	uv run manage.py runserver

worker:
	uv run celery -A david.apps.core.celery worker -l INFO

scheduler:
	uv run celery -A david.apps.core.celery beat -l INFO

migrate:
	uv run manage.py migrate

create-migration:
	uv run manage.py makemigrations

static:
	uv run manage.py collectstatic --no-input

deploy:
	git pull
	uv sync
	uv run manage.py migrate
	uv run manage.py collectstatic --no-input
	sudo systemctl daemon-reload
	sudo systemctl restart worker.service
	sudo systemctl restart gunicorn.service
	sudo systemctl restart scheduler.service
	sudo service nginx reload

test:
	uv run pytest --create-db --disable-warnings --ds=david.settings.test david/

check:
	git add .
	uv run pre-commit run

django-checks:
	uv run manage.py makemigrations --dry-run --check --verbosity=3 --settings=david.settings.sqlite
	uv run manage.py check --fail-level WARNING --settings=david.settings.sqlite

pip:
	uv sync --all-extras --dev

update:
	uv sync --all-extras --dev --upgrade
	uv run pre-commit autoupdate

ci: pip check django-checks test docker-build

dump:
	pg_dump -h localhost -U david -d david > david.sql

restore:
	psql -h localhost -U david -d postgres -c "DROP DATABASE david;"
	psql -h localhost -U david -d postgres -c "CREATE DATABASE david;"
	psql -h localhost -U david -d david < david.sql

docker-build:
	docker build -t david:latest .

docker-static:
	docker exec -it david-django uv run python manage.py collectstatic --no-input

docker-migrate:
	docker exec -it david-django uv run python manage.py migrate