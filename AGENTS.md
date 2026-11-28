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
- Make targets load the ignored local `.env`. Never copy its credentials into tracked documentation, tests, `.env.example`, or command output.
- Never commit real listing contacts, OAuth credentials, or production data.
- Keep the blob dataset endpoint until the normalized-table migration is complete.
- During the blob stage, staff may replace the dataset. Clients may change only properties, groups, and the provider record matching `request.user.provider_id`; enforce this in DRF before saving.
- Local integration uses the sibling `real-estate-map-explorer` on `http://localhost:3000`. Test cookie auth, credentialed CORS, the dataset feed, and an owned client write with both servers running.
- `make seed-local` is the repeatable setup for fictional accounts and the frontend dummy dataset. Never use its documented passwords outside local development.
- Add tests for permissions, validation, and public API behavior.
- Do not add deployment infrastructure until it is requested.

## Commands

Use the Makefile: `make run`, `make migrate`, `make migrations`, `make seed-local`, `make check`, `make test`, and `make lint`.

## Workflow

Read this file first, make the smallest coherent change, run the relevant checks, and document environment or behavior changes in `README.md`.
