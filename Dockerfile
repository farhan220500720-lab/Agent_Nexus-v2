FROM python:3.11-slim

# Install system dependencies (postgres client for db interaction and build tools for C extensions)
RUN apt-get update && apt-get install -y --no-install-recommends     postgresql-client     gcc     libpq-dev     git     && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# --- Dependency Installation using requirements.txt ---
# Copy dependency files only (leverages Docker caching)
COPY pyproject.toml poetry.lock* /usr/src/app/
COPY requirements.txt /usr/src/app/

# CRITICAL FIX: Install Poetry (package manager) and then the runtime deps via pip
RUN pip install --upgrade pip setuptools wheel     && pip install poetry     && pip install -r requirements.txt

# --- Application Copy and Run ---
# Copy the rest of the application code
COPY . /usr/src/app/

# Expose the application port
EXPOSE 8000

# Use the installed dependencies to run the FastAPI application
CMD ["uvicorn", "common.main:app", "--host", "0.0.0.0", "--port", "8000"]
