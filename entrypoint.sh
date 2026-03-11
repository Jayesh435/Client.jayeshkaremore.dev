#!/bin/sh
set -e

python manage.py migrate --noinput

# Ensure an admin account can be bootstrapped on platforms without SSH access.
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if username and email and password:
	User = get_user_model()
	user, created = User.objects.get_or_create(
		username=username,
		defaults={"email": email, "is_staff": True, "is_superuser": True},
	)

	# Keep credentials/flags in sync on subsequent deploys.
	user.email = email
	user.is_staff = True
	user.is_superuser = True
	user.set_password(password)
	user.save()

	status = "created" if created else "updated"
	print(f"Superuser {status}: {username}")
else:
	print("Skipping superuser bootstrap: DJANGO_SUPERUSER_* vars are not fully set.")
PY

python manage.py collectstatic --noinput

exec gunicorn jk_client_portal.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3
