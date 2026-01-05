# David - Django template

Big things have small beginnings.

[![Python 3.14](https://img.shields.io/badge/python-3.14-green.svg)](https://www.python.org/downloads/release/python-3142/)
[![Code style: ruff](https://img.shields.io/badge/ruff-enabled-informational?logo=ruff)](https://astral.sh/ruff)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/manti-by/pdw/master/LICENSE)

**Maintainer:** Alex Chaika <manti.by@gmail.com>

**Source:** [https://github.com/manti-by/david/](https://github.com/manti-by/david/)

## Features

- Django REST Framework API
- Celery for background tasks
- APScheduler for scheduled jobs
- PostgreSQL database
- Redis caching
- RabbitMQ message broker
- Comprehensive API documentation (Swagger/OpenAPI)

## Requirements

- Python 3.14
- PostgreSQL 18+
- Redis 7+
- RabbitMQ 4+
- UV package manager

## Development Setup

### 1. Install Prerequisites

Install [Python 3.14](https://www.python.org/downloads/release/python-3142/) and [UV tool](https://docs.astral.sh/uv/getting-started/installation/).

### 2. Clone Repository

```shell
git clone https://github.com/manti-by/david.git && cd david/

```

### 3. Setup environment and install project dependencies

```shell
uv sync --all-extras --dev
```

### 4. Configure Environment Variables

Create a `.env` file (optional for development):

```ini
# Database
POSTGRES_NAME=david
POSTGRES_USER=david
POSTGRES_PASS=david
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis
REDIS_HOST=localhost

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_USER=david
RABBITMQ_PASS=david

# Django
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=david.settings.dev
```

### 5. Setup Database

Ensure PostgreSQL is running, then:

```shell
# Run migrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Collect static files
uv run python manage.py collectstatic --no-input
```

### 6. Start Services

**Option A: Using Docker Compose (Recommended)**

```shell
# Build Docker image
make docker-build

# Start all services
docker compose up -d

# Run migrations
make docker-migrate

# Collect static files
make docker-static
```

**Option B: Manual Setup**

Start services in separate terminals:

```shell
# Terminal 1: Django development server
make run

# Terminal 2: Celery worker
make worker

# Terminal 3: Scheduler
make scheduler
```

### 7. Access Application

- **Web Interface:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **API Documentation (Swagger):** http://localhost:8000/api/docs/
- **API Documentation (ReDoc):** http://localhost:8000/api/redoc/
- **API Schema (OpenAPI):** http://localhost:8000/api/schema/

## Production Deployment

### Environment Variables

Set the following environment variables in production:

```ini
# Django
DJANGO_SETTINGS_MODULE=david.settings.prod
SECRET_KEY=<generate-secure-secret-key>
ALLOWED_HOSTS=david.local,your-domain.com

# Database
POSTGRES_NAME=david
POSTGRES_USER=<secure-username>
POSTGRES_PASS=<secure-password>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_USER=<secure-username>
RABBITMQ_PASS=<secure-password>

# CSRF
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://api.your-domain.com
```

### Docker Deployment

1. **Build Production Image:**

```shell
docker build -t david:latest .
```

2. **Update docker-compose.yml:**

Set `DJANGO_SETTINGS_MODULE=david.settings.prod` in the django service environment.

3. **Start Services:**

```shell
docker compose up -d
```

4. **Run Migrations:**

```shell
docker exec -it david-django uv run python manage.py migrate
```

5. **Collect Static Files:**

```shell
docker exec -it david-django uv run python manage.py collectstatic --no-input
```

### Systemd Service Deployment

1. **Copy service files:**

```shell
sudo cp configs/gunicorn.service /etc/systemd/system/
sudo cp configs/worker.service /etc/systemd/system/
sudo cp configs/scheduler.service /etc/systemd/system/
```

2. **Update service files** with correct paths and environment variables.

3. **Enable and start services:**

```shell
sudo systemctl daemon-reload
sudo systemctl enable gunicorn.service worker.service scheduler.service
sudo systemctl start gunicorn.service worker.service scheduler.service
```

4. **Configure Nginx:**

```shell
sudo cp configs/nginx.conf /etc/nginx/sites-available/david
sudo ln -s /etc/nginx/sites-available/david /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Deployment Workflow

Use the Makefile for deployment:

```shell
make deploy
```

This will:
1. Pull latest code
2. Sync dependencies
3. Run migrations
4. Collect static files
5. Reload systemd services
6. Reload nginx

## API Documentation

The API is fully documented using OpenAPI 3.0:

- **Swagger UI:** `/api/docs/` - Interactive API documentation
- **ReDoc:** `/api/redoc/` - Alternative API documentation
- **OpenAPI Schema:** `/api/schema/` - Raw OpenAPI JSON schema

### API Endpoints

- `GET /api/v1/core/healthcheck/` - Health check endpoint
- `POST /api/v1/core/logs/` - Create log entry

See the Swagger documentation for complete API details.

## Development Commands

```shell
# Run development server
make run

# Run Celery worker
make worker

# Run scheduler
make scheduler

# Run tests
make test

# Run linting and checks
make check

# Run Django system checks
make django-checks

# Create migrations
make migrations

# Apply migrations
make migrate

# Collect static files
make static
```

## Project Structure

```
david/
├── api/              # API endpoints
│   └── v1/
│       └── core/     # Core API views and serializers
├── apps/
│   └── core/         # Core Django app
│       ├── models.py
│       ├── views.py
│       ├── tasks.py  # Celery tasks
│       └── scheduler.py  # APScheduler jobs
├── settings/         # Django settings
│   ├── base.py       # Base settings
│   ├── dev.py        # Development settings
│   ├── prod.py       # Production settings
│   └── test.py       # Test settings
└── templates/        # HTML templates
```

## Testing

```shell
# Run all tests
make test

# Run with coverage (if configured)
uv run pytest --cov=david
```

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running
- Check environment variables are set correctly
- Ensure database exists and user has permissions

### Celery Worker Not Processing Tasks

- Verify RabbitMQ is running and accessible
- Check worker logs: `make worker` or `docker logs david-worker`
- Verify `CELERY_BROKER_URL` is correct

### Static Files Not Loading

- Run `make static` or `make docker-static`
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify nginx configuration for static file serving

## License

BSD License - see LICENSE file for details.
