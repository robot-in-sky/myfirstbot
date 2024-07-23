.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run		Start the bot (for docker-compose usage)"
	@echo "  project-start Start with docker-compose"
	@echo "  project-stop  Stop docker-compose"


.PHONY:	mypy
mypy:
	poetry run mypy --strict --pretty --no-implicit-reexport --install-types app/ tests/

.PHONY: ruff
ruff:
	poetry run ruff check app/ tests/ --fix --respect-gitignore

.PHONY: run
run:
	migrate
	poetry run python -m app.bot

# Alembic utils
.PHONY: generate
generate:
	poetry run alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

# Docker utils
.PHONY: project-start
project-start:
	docker compose up --force-recreate ${MODE}

.PHONY: project-stop
project-stop:
	docker compose down --remove-orphans ${MODE}
