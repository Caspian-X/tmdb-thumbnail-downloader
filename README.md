# TV Show Thumbnail Downloader

Download episode thumbnails from The Movie Database (TMDB) or TheTVDB for your favorite TV shows.

<div align="">
  <img src="assets/tmdb-logo-long.svg" alt="TMDB Logo" width="800">
  <br><br>
  <img src="assets/thetvdb-logo-light.png" alt="TheTVDB Logo" width="200">
  <br><br>
  Made possible by <a href="https://www.themoviedb.org/">The Movie DB</a> and <a href="https://thetvdb.com/">TheTVDB</a>
</div>

## Features

- Download episode thumbnails for entire TV series
- Support for both TMDB and TheTVDB APIs
- Organized output by season

## Quick Start

### First Time Setup

1. Copy the example environment file and add your API keys:

    ```bash
    cp .env.example .env
    ```

2. Edit `.env` and add your API keys:
    - Get a TMDB API key from [themoviedb.org](https://www.themoviedb.org/settings/api)
    - Get a TheTVDB API key from [thetvdb.com](https://thetvdb.com/dashboard/account/apikey)

3. Install dependencies:

    ```bash
    uv sync
    ```

    Or use just to do both steps automatically:

    ```bash
    just init  # Copies .env.example if needed and runs uv sync
    ```

### Configuration

Edit the `.env` file to configure each downloader:

#### TMDB Configuration
- `TMDB_API_KEY` - Your TMDB API key (required)
- `TMDB_TV_SHOW_ID` - The TV show ID (default: 1570)
- `TMDB_OUTPUT_DIR` - Output directory (default: thumbnails)

#### TheTVDB Configuration
- `THETVDB_API_KEY` - Your TheTVDB API key (required)
- `THETVDB_SERIES_ID` - The series ID (default: 72474)
- `THETVDB_OUTPUT_DIR` - Output directory (default: thetvdb_thumbnails)

### Running

Choose which downloader to use:

```bash
# Download from TMDB
uv run python tmdb_thumbnail_downloader.py

# Download from TheTVDB
uv run python thetvdb_thumbnail_downloader.py
```

#### Using Just

If you have [just](https://github.com/casey/just) installed:

```bash
# First time setup
just init

# Run TMDB downloader
just run-tmdb

# Run TheTVDB downloader
just run-thetvdb
```

## Output Structure

Downloaded thumbnails are organized by season:

```
output_directory/
├── Season 01/
│   ├── s01e01 Episode Name-thumb.jpg
│   ├── s01e02 Episode Name-thumb.jpg
│   └── ...
├── Season 02/
│   └── ...
└── Season 00/
    └── ...
```

## Finding TV Show IDs

### TMDB
1. Visit [themoviedb.org](https://www.themoviedb.org/)
2. Search for your TV show
3. The ID is in the URL: `https://www.themoviedb.org/tv/[ID]-show-name`

### TheTVDB
1. Visit [thetvdb.com](https://thetvdb.com/)
2. Search for your series
3. The ID will be under the name next to the year: `Series #[ID]`. You can also find it under the `General` tab as the `TheTVDB.com Series ID` value.
