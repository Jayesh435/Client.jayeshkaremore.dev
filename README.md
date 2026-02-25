# Client.jayeshkaremore.dev

## Deploy on Render with Docker

This project now includes Docker and Render Blueprint files:

- `Dockerfile`
- `entrypoint.sh`
- `.dockerignore`
- `render.yaml`
- `.env.render.example`

### Option A: Blueprint deploy (recommended)

1. Push this repository to GitHub.
2. In Render, open **New +** -> **Blueprint**.
3. Select your repository.
4. Render reads `render.yaml` and creates:
	- One Docker web service (`jk-client-portal`)
	- One PostgreSQL database (`jk-client-portal-db`)
5. Click **Apply** to deploy.

### Option B: Manual Docker web service

1. In Render, create **New +** -> **Web Service**.
2. Connect your repo.
3. Choose **Runtime: Docker**.
4. Add environment variables from `.env.render.example`.
5. Set at minimum:
	- `DEBUG=False`
	- `ALLOWED_HOSTS=<your-render-domain>`
	- `SECRET_KEY=<strong-secret>`
	- PostgreSQL `DB_*` variables

### Important notes

- The container startup runs:
  - `python manage.py migrate --noinput`
  - `python manage.py collectstatic --noinput`
  - `gunicorn jk_client_portal.wsgi:application --bind 0.0.0.0:$PORT`
- SQLite is not recommended for Render production. Use PostgreSQL.
- Update `ALLOWED_HOSTS` with your final Render/custom domain.