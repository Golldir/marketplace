# Команды для работы с проектом
start:
	docker compose up -d
	docker exec app sh -c "cd src && alembic upgrade head"

run:
	poetry run uvicorn src.app.main:app --reload

migrate:
	poetry run alembic upgrade head

revision:
	poetry run alembic revision --autogenerate

docker-build:
	docker build -t fastapi-app ./src/app

docker-run:
	docker run -p 8000:8000 fastapi-app

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

test:
	poetry run pytest
