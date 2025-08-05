docker_up:
	docker compose -f docker-compose-local.yaml up -d

docker_down:
	docker compose -f docker-compose-local.yaml down --remove-orphans

alembic_upgrade:
	set PYTHONPATH=./src && alembic -c src/alembic.ini upgrade heads

start:
	python src/main.py
