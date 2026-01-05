FROM python:3.14-slim

LABEL maintainer="Alex Chaika <manti.by@gmail.com>"

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/usr/local

RUN mkdir -p /srv/app/src/ /var/lib/app/static/ /var/lib/app/media/ /var/log/app/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

WORKDIR /srv/app/src/
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
