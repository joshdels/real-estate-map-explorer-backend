.PHONY: run migrate migrations test lint check

run:
	uv run python manage.py runserver

migrate:
	uv run python manage.py migrate

migrations:
	uv run python manage.py makemigrations

test:
	uv run python manage.py test

lint:
	uv run ruff check .

check:
	uv run python manage.py check
