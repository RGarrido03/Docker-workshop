FROM ghcr.io/astral-sh/uv:python3.13-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV ENV=development

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
RUN apk add --no-cache patch

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen

EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
