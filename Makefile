.DEFAULT_GOAL := run

ifneq (,$(wildcard .env))
include .env
export
endif

.PHONY: run migrate migrations seed-local test lint check

run:
	uv run python manage.py runserver

migrate:
	uv run python manage.py migrate

migrations:
	uv run python manage.py makemigrations

seed-local:
	uv run python manage.py seed_dataset ../real-estate-map-explorer/public/data/data.json
	uv run python manage.py seed_local_accounts

test:
	uv run python manage.py test

lint:
	uv run ruff check .

check:
	uv run python manage.py check
