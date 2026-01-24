# lists available commands
default:
    @just --list --unsorted

# Setup environment file if it doesn't exist
setup-env:
    @test -f .env || (cp .env.example .env && echo "Created .env file. Please edit it with your API key.")
    @test -f .env && echo ".env file already exists"

# Install dependencies and create virtual environment
init: setup-env
    uv sync

# Download thumbnails from tmdb for the given show id
run-tmdb:
    uv run python tmdb_thumbnail_downloader.py

# Download thumbnails from thetvdb for the given show id
run-thetvdb:
    uv run python thetvdb_thumbnail_downloader.py
