# Setup environment file if it doesn't exist
setup-env:
    @test -f .env || (cp .env.example .env && echo "Created .env file. Please edit it with your API key.")
    @test -f .env && echo ".env file already exists"

# Install dependencies and create virtual environment
init: setup-env
    uv sync

# Run the main script
start:
    uv run python tmdb_thumbnail_downloader.py
