#!/bin/bash -e

# Echo colored text function
echo_green() {
    local message=$1

    local green="\x1b[32m"
    local clear="\x1b[0m"

    echo -e "${green}${message}${clear}"
}

#### Post generation script  ####

# Set environment variables
cp src/app/.env.ci src/app/.env

# Install dependencies and fail if dependencies not in sync
# https://docs.astral.sh/uv/concepts/projects/sync/#automatic-lock-and-sync
uv sync --locked

# Setup Django
uv run python src/manage.py collectstatic
uv run python src/manage.py makemigrations --name "initial"
uv run python src/manage.py migrate

# Run linters and tests
make lint
make test

# Echo success message
echo
echo       "============================================="
echo
echo_green "=== Project setup completed successfully! ==="
echo
echo       "Current config uses SQLite in-memory DB for fast development."
echo       "To switch to PostgreSQL:"
echo       "   1. Start PostgreSQL using your preferred method (see 'compose.yml' for a Docker example)"
echo       "   2. Set DATABASE_URL in 'src/app/.env' to your connection string"
echo       "      e.g. DATABASE_URL=postgres://username:password@localhost:5432/dbname"
echo
echo       "============================================="
