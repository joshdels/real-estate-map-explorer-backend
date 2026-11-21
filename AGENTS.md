# Open Lot Plans Backend

## Stack

- Python 3.12, Django 5.2, Django REST Framework, PostgreSQL, uv, and Ruff.
- `django-allauth` and `dj-rest-auth` provide email, Google, and Facebook authentication.

## Architecture

- `config/` contains Django configuration only.
- `core/` contains shared templates and project resources. It is not a Django app.
- Every Django application belongs under `apps/`.
- `apps/accounts/` owns the user model, profiles, roles, and authentication endpoints.
- `apps/datasets/` owns the temporary whole-dataset API used during the Supabase migration.
- `static/` contains shared frontend assets.

## Rules

- Keep views thin and put validation close to serializers and models.
- Use named URLs and version API routes under `/api/v1/`.
- Keep OAuth secrets, database credentials, and `DJANGO_SECRET_KEY` in environment variables.
- Never commit real listing contacts, OAuth credentials, or production data.
- Keep the blob dataset endpoint until the normalized-table migration is complete.
- Add tests for permissions, validation, and public API behavior.
- Do not add deployment infrastructure until it is requested.

## Commands

Use the Makefile: `make run`, `make migrate`, `make migrations`, `make check`, `make test`, and `make lint`.

## Workflow

Read this file first, make the smallest coherent change, run the relevant checks, and document environment or behavior changes in `README.md`.
