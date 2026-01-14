# AGENTS.md

## Project Overview

Django project template.
It uses Django 5.2.7 with Django REST Framework, PostgreSQL, Redis, and modern Python tooling.

## Project Structure

- All REST API related code placed in `./david/api/`
- Django apps with models, admin classes, migrations and management commands in `./david/apps/`
- Tests in `./david/tests/`
- Static files like images, CSS and JS in `./david/static/`
- Django templates in `./david/templates/`

## Development Commands

### Package Management

```bash
uv sync                    # Install dependencies
uv sync --upgrade          # Upgrade dependencies
```

### Django Management

```bash
uv run manage.py runserver                  # Start development server
uv run manage.py migrate                    # Run database migrations
uv run manage.py makemigrations             # Create new migrations
uv run manage.py collectstatic --no-input   # Collect static files
```

### Testing

```bash
# Run all tests
uv run pytest --create-db --disable-warnings --ds=david.settings.test david/

# Run single test file
uv run pytest --create-db --disable-warnings --ds=david.settings.test david/tests/api/test_sensors.py

# Run single test method
uv run pytest --create-db --disable-warnings --ds=david.settings.test david/tests/api/test_sensors.py::TestSensorsAPI::test_sensors__list

# Run with coverage (if available)
uv run pytest --cov=david --cov-report=term-missing david/
```

### Code Quality

```bash
# Run all pre-commit hooks
uv run pre-commit run

# Individual tools
uv run ruff check .                 # Lint
uv run ruff format .                # Format
uv run bandit -c pyproject.toml .   # Security analysis
```

### Database Operations

```bash
# Django checks
uv run manage.py makemigrations --dry-run --check --verbosity=3 --settings=david.settings.sqlite
uv run manage.py check --fail-level WARNING --settings=david.settings.sqlite
```

## Language & Environment

- Follow PEP 8 style guidelines, use Ruff for formatting (120 char line length)
- Use type hints for all function parameters and return values
- Prefer f-strings for string formatting over .format() or %
- Use list/dict/set comprehensions over map/filter when readable
- Prefer Pathlib over os.path for file operations
- Follow PEP 257 for docstrings (simple summary line plus detailed explanation)
- Use structural pattern matching (match/case) for complex conditionals
- Prefer EAFP (try/except) over LBYL (if checks) for Python idioms

## Django Framework

- Follow Django best practices and the MVT pattern
- Use Django ORM effectively, avoid raw SQL
- Use select_related and prefetch_related to avoid N+1 queries
- Never modify migrations after deployment
- Class-based views for API, function-based views for Django apps views
- Put business logic to services, prefer functions, models and views should be short and clean

### Background Tasks

- Use Celery for long-running or resource-intensive operations
- Define jobs as additional functions with prefix `queue_`
- Configure queue names for different priority levels

```python
from celery import shared_task


def process_data(data_id: str):
    # Long-running sync operation
    return data_id


@shared_task(name="queue_process_data")
def queue_process_data(caller_name: str):
    process_data(data_id="test")
```

### Periodic Jobs

- Use Celery Beat for scheduled tasks
- Every scheduled task should be queued
- Define jobs in `david/apps/core/tasks.py` within the app
- Use `PeriodicTask` for scheduling and a data migration to add it to a database

```python
from django_celery_beat.models import CrontabSchedule, PeriodicTask

schedule, _ = CrontabSchedule.objects.get_or_create(
    minute="30",
    hour="*",
    day_of_week="*",
    day_of_month="*",
    month_of_year="*",
)

PeriodicTask.objects.create(
    crontab=schedule,
    name="Importing contacts",
    task="david.apps.core.services.tasks.queue_process_data",
)
```

## Code Style Guidelines

### Python Standards

- Python version 3.13+ with type hints encouraged
- Ensure code style consistency using Ruff
- Line length 120 characters
- Indentation 4 spaces

### Import Organization

Use Ruff isort with this order:

1. `__future__` imports
2. Standard library imports
3. Third-party imports
4. First-party imports
5. Django imports
6. david imports

```python
from __future__ import annotations

import os
from decimal import Decimal

from django.db import models
from rest_framework import serializers

from david.apps.core.models import Log
```

### Naming Conventions

- **Models**: `PascalCase` (e.g., `DataLog`)
- **Functions/Variables**: `snake_case` (e.g., `get_data`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_COUNT`)
- **File Names**: `snake_case.py` (e.g., `data_utils.py`)
- **Classes**: `PascalCase` (e.g., `DataService`)

### Type Hints

Use type hints for function signatures and complex variables:

```python
from decimal import Decimal


def get_data(data_id: str) -> dict[str, Decimal] | None:
    # Implementation here
    return None
```

### Django Patterns

#### Models

- Use `__future__ import annotations` for forward references
- Include `created_at` and `updated_at` timestamp fields
- Use `verbose_name` and `verbose_name_plural` with translation support
- Implement custom QuerySets and Managers for complex queries
- Use `TextChoices` for enum fields

```python
from django.db import models
from django.utils.translation import gettext_lazy as _


class DataModel(models.Model):
    data_id = models.CharField(max_length=32, verbose_name=_("Data ID"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("data")
        verbose_name_plural = _("data")
```

#### Views and ViewSets

- Use GenericAPIView with mixins for REST APIs, e.g. `LogsView`
- Include proper type hints for Request/Response
- Use `lookup_field` for custom URL parameters
- Implement `perform_create`/`perform_update` for custom logic

#### Serializers

- Use explicit field definitions for clarity
- Include validation constraints
- Use `ChoiceField` for enum fields
- Do not use a ModelSerializer, just a bare Serializer

#### API Versioning

- URL-based versioning: `/api/v1/...`
- Include version in DRF router namespace: `api:v1:code:logs`
- Increment version for breaking changes only

## Dependency Management

- Manage dependencies via **[uv](https://github.com/astral-sh/uv)** and **virtual environments**.

## Testing

- Focus testing on APIs and critical code paths
- Write integration tests for API endpoints and external integrations
- Use mocks for external services and slow dependencies
- Test error handling and validation logic
- Use meaningful test names that describe the scenario

### Testing Patterns

#### Test Structure

- Use pytest with pytest-django
- Create descriptive test method names with double underscores
- Use Factory Boy for test data
- Test both success and error cases
- Use parametrized tests for similar scenarios

```python
import pytest

from david.tests.factories import UserFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestLogsView:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.url = reverse("api:v1:core:logs")

    @pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
    def test_logs__not_allowed_methods(self, method):
        self.client.force_authenticate(self.user)

        test_client_callable = getattr(self.client, method)
        response = test_client_callable(self.url, format="json")

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
```

#### Test Data

- Use Factory Boy for creating test instances
- Use meaningful default values in factories
- Test with different data variations

## Logging and Error Handling

### Logging

- Use Python's `logging` module, not print statements
- Create logger at module level: `logger = logging.getLogger(__name__)`
- Use appropriate log levels:
    - `DEBUG`: Detailed debug information
    - `INFO`: Confirmation of expected behavior
    - `WARNING`: Unexpected but handled issues
    - `ERROR`: Failures that need attention

```python
import logging

from david.apps.core.services import get_data_hash

logger = logging.getLogger(__name__)


def process_file(file: str):
    logger.info(f"Processing file {file}")
    try:
        music, _ = get_data_hash(data={}, secret_key="secret_key")
        logger.info(f"{file}: [{music.album}] {music.artist} - {music.title} - {music.year}")
    except RuntimeError as e:
        logger.error(f"{file}: {e}")
```

### Error Handling

- Use custom exception classes for domain-specific errors
- Log exceptions with context before re-raising

```python
class DataError(Exception):
    """Base exception for data-related errors."""


class DataNotFoundError(DataError):
    """Raised when data cannot be found."""


class DataConnectionError(DataError):
    """Raised when connection to data fails."""
```

## Environment Configuration

### Settings Files

- `base.py`: Common settings
- `dev.py`: Development (DEBUG=True, ALLOWED_HOSTS="*")
- `test.py`: Testing (DEBUG=False, minimal logging)
- `prod.py`: Production settings
- `sqlite.py`: SQLite settings for Django checks

### Database

- **Development/Production**: PostgreSQL
- **Testing**: SQLite (configured in test settings)

## Security Guidelines

- Never commit secrets or API keys
- Use environment variables for sensitive configuration
- Run `bandit` security analysis before commits
- Validate all user inputs

## Pre-commit Hooks

The project uses pre-commit hooks for code quality:

- Ruff (linting and formatting)
- Bandit (security analysis)
- pyupgrade (Python 3.13+ syntax)
- curlylint (HTML linting)

## Deployment

- Services: gunicorn, worker, scheduler, nginx
- Use systemd for service management

## Common Issues

### Testing

- Always use `@pytest.mark.django_db` for database tests
- Use `--create-db` flag for a fresh test database

### Migrations

- Check for pending migrations: `make django-checks`
- Create migrations after model changes

## Performance Optimization

- Use `select_related` and `prefetch_related` for query optimization
- Implement proper database indexing
- Cache frequently accessed data with Redis

## AI Behavior

Response style - Concise and minimal:

- Provide minimal, working code without unnecessary explanation
- Omit comments unless absolutely essential for understanding
- Skip boilerplate and obvious patterns unless requested
- Use type inference and shorthand syntax where possible
- Focus on the core solution, skip tangential suggestions
- Assume familiarity with language idioms and framework patterns
- Let code speak for itself through clear naming and structure
- Avoid over-explaining standard patterns and conventions
- Provide just enough context to understand the solution
- Trust the developer to handle obvious cases independently
