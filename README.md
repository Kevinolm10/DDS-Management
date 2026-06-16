# DDS-Management

## Development setup

This project now supports local development defaults:

- Database: SQLite (no PostgreSQL required)
- Media storage: local filesystem (no Cloudinary required)

### 1) Create a .env file (optional for dev)

You can run locally with only these values:

DEBUG=True
SECRET_KEY=dev-secret-key

### 2) Run migrations and start server

python manage.py migrate
python manage.py runserver

## Production setup

Use environment variables to switch to production services:

- USE_POSTGRES=True
- USE_CLOUDINARY=True
- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
- CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

Recommended production values:

- DEBUG=False