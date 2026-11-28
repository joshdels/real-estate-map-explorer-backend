# API reference

The backend exposes a versioned REST API for the Open Lot Plans Next.js application.

## Interactive documentation

With the development server running at `http://127.0.0.1:8000`:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

The documentation routes are public. Swagger's **Authorize** action can describe protected
operations, but browser authentication is normally supplied by the HTTP-only cookies created by
the login endpoints.

## Frontend connection

The frontend repository is expected at the sibling path
`../real-estate-map-explorer`. Set this in its local environment:

```dotenv
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

The backend already allows `http://localhost:3000` by default for credentialed CORS and CSRF.
When the frontend is opened as `http://127.0.0.1:3000`, add that exact origin to both
`CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`; origins are not interchangeable.

## Stage 1 dataset contract

`GET /api/v1/dataset` is public and returns the whole validated dataset JSON document.

`PUT /api/v1/dataset` replaces that document. Administrators and employees may replace all of it.
During this blob migration stage, a client request is accepted only when changes are limited to its
assigned provider plus properties and groups with the same `providerId`. Shared settings, reviews,
and other providers' records must remain byte-for-byte equivalent. The body and response use the
same shape:

```json
{
  "properties": [],
  "providers": [],
  "groups": [],
  "reviews": []
}
```

Optional top-level data such as `metadata`, `utilities`, and `agent` is preserved. Listings must
contain the required fields enforced by `apps/datasets/serializers.py`, two coordinates, and at
least three polygon points.

This blob endpoint remains available until the normalized-table migration is complete, as required
by the frontend migration plan in `../real-estate-map-explorer/docs/MIGRATION_DJANGO_DRF.md`.

## Authentication paths

Authentication lives below `/api/v1/auth/` and is provided by `dj-rest-auth` and `django-allauth`.
Email/password is the active first-stage login method. The API includes login, logout, user details,
password reset, token refresh, registration, and email verification routes.

Google and Facebook are parked. Their implementation remains in the project, but these routes are
only added when `ENABLE_SOCIAL_AUTH=true`:

- `POST /api/v1/auth/google/`
- `POST /api/v1/auth/facebook/`

JWT access and refresh tokens use HTTP-only cookies. Production secrets, OAuth credentials, and
database credentials belong only in backend environment variables.

## Local test identities

After `make migrate`, run `make seed-local`. It imports the sibling frontend's fictional dataset and
creates three repeatable local accounts with password `LocalDemo123!`:

- `admin@example.test`, administrator
- `staff@example.test`, employee
- `provider@example.test`, client assigned to `provider-coastal`

These identities and their password are development fixtures, not production defaults.
