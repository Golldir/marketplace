# Команды для работы с проектом
start:
	docker compose up -d --build
	docker exec app sh -c "cd src && alembic upgrade head"
