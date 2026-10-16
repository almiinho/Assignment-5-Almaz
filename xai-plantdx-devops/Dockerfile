FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --no-cache-dir --upgrade pip && python -m pip install --no-cache-dir .
COPY tests ./tests
RUN python -m pip install --no-cache-dir pytest && useradd --create-home appuser
USER appuser
ENTRYPOINT ["plant-dataset-audit"]
CMD ["--help"]
