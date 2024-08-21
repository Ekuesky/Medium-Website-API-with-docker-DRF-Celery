# Define variables for container names
API_CONTAINER = django-api
REDIS_CONTAINER = redis-server
DB_CONTAINER = postgres-db


build:
	docker compose -f local-docker-compose.yml up --build -d --remove-orphans

config:
	 docker compose -f local-docker-compose.yml config

up:
	docker compose -f local-docker-compose.yml up -d

down:
	docker compose -f local-docker-compose.yml down

show-logs:
	docker compose -f local-docker-compose.yml logs

show-logs-api:
	docker compose -f local-docker-compose.yml logs api

show-logs-flower:
	docker compose -f local-docker-compose.yml logs flower

show-logs-celery:
	docker compose -f local-docker-compose.yml logs celery_worker

makemigrations:
	docker compose -f local-docker-compose.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local-docker-compose.yml run --rm api python manage.py migrate

collectstatic:
	docker compose -f local-docker-compose.yml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local-docker-compose.yml run --rm api python manage.py createsuperuser

down-v:
	docker compose -f local-docker-compose.yml down -v

volume:
	docker volume inspect local_postgres_data

api-db:
	docker compose -f local-docker-compose.yml exec postgres psql --username=ayiek --dbname=apipro

flake8:
	docker compose -f local-docker-compose.yml exec api flake8 .

black-check:
	docker compose -f local-docker-compose.yml exec api black --check --exclude=migrations .

black-diff:
	docker compose -f local-docker-compose.yml exec api black --diff --exclude=migrations .

black:
	docker compose -f local-docker-compose.yml exec api black --exclude=migrations .

isort-check:
	docker compose -f local-docker-compose.yml exec api isort . --check-only --skip venv --skip migrations

isort-diff:
	docker compose -f local-docker-compose.yml exec api isort . --diff --skip venv --skip migrations

isort:
	docker compose -f local-docker-compose.yml exec api isort . --skip venv --skip migrations

backup:
	 docker compose -f local-docker-compose.yml exec postgres backup

show-backups:
	 docker compose -f local-docker-compose.yml exec postgres backups

restore:
	 docker compose -f local-docker-compose.yml exec postgres restore

#############Personal usage##########################################################
shell:
	docker compose -f local-docker-compose.yml exec api python manage.py shell

rmi_dangling:
	@echo "Removing dangling images ..."
	docker images --filter "dangling=true" -q | xargs docker rmi

rmi_all:
	@echo "Removing all images ..."
	docker rmi $(docker images -q)

empty_docker:
	@echo "Emptying docker"
	docker system prune -a --volumes -f

signing_key:
	python -c "import secrets; print(secrets.token_urlsafe(38))"

test-cov-html:
	docker compose -f local-docker-compose.yml run --rm api pytest -p no:warnings --cov=. --cov-report html

test-cov-verbose:
	docker compose -f local-docker-compose.yml run --rm api pytest -p no:warnings --cov=. -v






