# Open Lot Plans Backend

Django REST Framework backend for the Open Lot Plans Next.js application. The first migration stage keeps the current whole-dataset JSON contract so data can move away from Supabase before the domain is normalized into PostgreSQL tables.

## Setup

```bash
uv sync
cp .env.example .env
make migrate
make run
```

The Makefile loads the ignored local `.env` automatically. Direct `uv run python manage.py ...`
commands do not load it, so either use the documented `make` targets or export the variables first.

Seed the Stage 1 blob and local-only email accounts from the frontend repository:

```bash
make seed-local
```

This imports all fictional listing data, coordinates, and polygons. It also creates
`admin@example.test`, `staff@example.test`, and `provider@example.test`; each uses the local-only
password `LocalDemo123!`. The provider account is assigned to `provider-coastal`.

## API

- `GET /api/v1/dataset` is public and returns the current dataset JSON.
- `PUT /api/v1/dataset` lets staff replace the document. During this temporary blob stage, a client may change only its assigned provider record and records whose `providerId` matches the account. On every save the listing polygons are mirrored into the PostGIS `datasets_lotgeometry` table (one real `Polygon` geometry per listing, SRID 4326), so saved and edited plot points persist as spatial data, not only inside the JSON blob.
- `GET /api/v1/lots.geojson` is public and returns every stored lot boundary from PostGIS as a GeoJSON FeatureCollection.

This app now requires **PostgreSQL with the PostGIS extension** (GeoDjango). `DATABASE_URL` must point at a PostGIS-enabled database; the `postgis` extension and the geometry table are created by the `datasets` migrations. GDAL and GEOS must be available on the host.
- `POST /api/v1/media/images` accepts authenticated JPEG, PNG, and WebP property images up to 10 MB. Local development stores them under `media/`; production stores them in S3.
- `/api/v1/auth/` provides login, logout, password reset, user details, and refresh-cookie endpoints.
- `/api/v1/auth/registration/` provides email registration and verification.
- Email/password registration and login are the active authentication path.
- Google and Facebook login are parked by default. Set `ENABLE_SOCIAL_AUTH=true` later to expose their provider-token endpoints.

JWT access and refresh tokens are stored in HTTP-only cookies. For production, use the frontend and API on same-site subdomains when possible.

Production media storage requires `AWS_STORAGE_BUCKET_NAME`. Configure `AWS_S3_REGION_NAME` and optionally `AWS_S3_CUSTOM_DOMAIN`; AWS credentials use the standard boto3 environment or instance-role chain. The S3 bucket must allow the resulting public media URLs to be read by buyers.

### API documentation

Start the server with `make run`, then open:

- Swagger UI: <http://127.0.0.1:8000/api/docs/>
- ReDoc: <http://127.0.0.1:8000/api/redoc/>
- OpenAPI JSON/YAML: <http://127.0.0.1:8000/api/schema/>

The detailed contract and frontend connection notes are in [docs/API.md](docs/API.md).

## Connect the Next.js frontend

For the sibling frontend repository at `../real-estate-map-explorer`, add the backend origin to its
local environment:

```dotenv
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Run the backend on port 8000 and the frontend on port 3000. The default backend settings allow
`http://localhost:3000`; if the frontend uses `127.0.0.1`, configure that exact origin in both
`CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`. The current endpoint shape follows the frontend
plan at `../real-estate-map-explorer/docs/MIGRATION_DJANGO_DRF.md`.

## Parked Google and Facebook login

Social login code remains available but its routes are disabled unless `ENABLE_SOCIAL_AUTH=true`.
When enabling it later, add OAuth credentials either through the environment variables in
`.env.example` or through Django admin as `SocialApp` records. Do not configure the same provider
in both places. Provider callback URLs and allowed domains still need to be registered in the Google
and Meta consoles before sign-in can work.

## Commands

- `make migrations` and `make migrate`
- `make seed-local`
- `make check`
- `make test`
- `make lint`

## Migration sequence

1. Serve the validated dataset blob from Django and add a Django repository to the frontend.
2. Normalize listings, providers, groups, reviews, reports, and assisted cases into PostgreSQL tables.
3. Switch frontend auth and roles to the endpoints in this project.
4. Remove Supabase only after data and auth cutover have been verified in production.
