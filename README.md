# TMDB Thumbnail Downloader

Made possible by [The Movie DB](https://www.themoviedb.org/)
<div align="">
  <img src="assets/tmdb-logo.svg" alt="TMDB Logo" width="200">
</div>

## Quick Start

### First Time Setup

1. Copy the example environment file and add your API key:

    ```bash
    # Copy the example file
    cp .env.example .env

    # Then edit .env and add your TMDB API key
    ```

2. Install dependencies and create virtual environment:

    ```bash
    uv sync
    ```

Or use just to do both steps automatically:

```bash
just init  # This will copy .env.example if needed and run uv sync
```

### Configuration

Edit the `.env` file to configure:
- `TMDB_API_KEY` - Your TMDB API key (required)
- `TMDB_TV_SHOW_ID` - The TV show ID to download thumbnails from (default: 1570)
- `TMDB_OUTPUT_DIR` - Output directory for thumbnails (default: thumbnails)

### Running

```bash
# Run the main script
uv run python tmdb_thumbnail_downloader.py
```

### Using Just

If you have [just](https://github.com/casey/just) installed:

```bash
# First time setup
just init

# Run the application
just start
```
