FROM python:3.12 as builder
WORKDIR /app
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev # Установка без зависимостей для разработки


FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app ./
CMD ["python", "main.py"]
