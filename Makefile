docker_up:
	docker compose -f docker-compose-local.yaml up -d

docker_down:
	docker compose -f docker-compose-local.yaml down --remove-orphans

upgrade_alembic_src:
	set PYTHONPATH=./src && alembic -c src/alembic.ini upgrade heads

upgrade_alembic_tests:
	set PYTHONPATH=./src && alembic -c tests/alembic.ini upgrade heads
