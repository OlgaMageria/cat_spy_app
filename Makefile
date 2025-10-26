.PHONY: migrate run build dev

build:
	docker compose up --build -d

run:
	docker compose up

down:
	docker compose down

migrate:
	docker compose exec fastapi-app uv run alembic upgrade head

dev: build migrate