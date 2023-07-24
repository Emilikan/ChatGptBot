DOCKER_COMPOSE := deploy/docker-compose.yml
DOCKER_ENV := deploy/.env
DOCKER_COMPOSE_RUNNER := docker compose
PROJECT_NAME := chat_gpt

ifneq ($(ENV),)
	DOCKER_COMPOSE := deploy/dev.docker-compose.yml
	DOCKER_COMPOSE_RUNNER := docker compose
	ifeq ($(ENV),docker)
		DOCKER_ENV := deploy/.env.dev
		include deploy/.env.dev
		export $(shell sed 's/=.*//' deploy/.env.dev)
	else ifeq ($(ENV),local)
		DOCKER_ENV := deploy/.env.dev.local
		include deploy/.env.dev.local
		export $(shell sed 's/=.*//' deploy/.env.dev.local)
	endif
endif


.PHONY: run-tg-bot
run-tg-bot:
	poetry run python -m chat_gpt.presentation.bot

.PHONY: migrate-create
migrate-create:
	poetry run alembic -c deploy/alembic.ini revision --autogenerate

.PHONY: migrate-up
migrate-up:
	poetry run alembic -c deploy/alembic.ini upgrade head

.PHONY: compose-up
compose-up:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) up

.PHONY: compose-build
compose-build:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) build

.PHONY: compose-pull
compose-pull:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) pull

.PHONY: compose-down
compose-down:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) down

.PHONY: compose-logs
compose-logs:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) -p $(PROJECT_NAME) logs -f

.PHONY: compose_create_pyrogram_session
compose_create_pyrogram_session:
	docker exec -it $(PROJECT_NAME)_tg_bot create_pyrogram_session