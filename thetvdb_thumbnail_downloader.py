import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - loaded from environment variables
API_KEY = os.getenv("THETVDB_API_KEY")
SERIES_ID = int(os.getenv("THETVDB_SERIES_ID", "72474"))
OUTPUT_DIR = os.getenv("THETVDB_OUTPUT_DIR", "thetvdb_thumbnails")

if not API_KEY:
    raise ValueError(
        "THETVDB_API_KEY not found in environment variables. Please create a .env file with your API key."
    )

# TheTVDB API base URLs
BASE_URL = "https://api4.thetvdb.com/v4"
IMAGE_BASE_URL = "https://artworks.thetvdb.com"


def get_auth_token():
    """Authenticate and get bearer token."""
    url = f"{BASE_URL}/login"
    payload = {"apikey": API_KEY}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["data"]["token"]


def get_series_details(token, series_id):
    """Get TV series details."""
    url = f"{BASE_URL}/series/{series_id}/extended"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]


def get_series_episodes(token, series_id, season_type="default", page=0):
    """Get all episodes for a specific series and season type."""
    url = f"{BASE_URL}/series/{series_id}/episodes/{season_type}"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def download_image(image_path, save_path):
    """Download an image from TheTVDB."""
    if not image_path:
        return False

    # TheTVDB image paths can be full URLs or relative paths
    if image_path.startswith("http"):
        url = image_path
    else:
        url = f"{IMAGE_BASE_URL}{image_path}"

    response = requests.get(url)
    response.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(response.content)
    return True


def main():
    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    print("Authenticating with TheTVDB API...")
    token = get_auth_token()
    print("Authentication successful!\n")

    print(f"Fetching TV series details...")
    series_details = get_series_details(token, SERIES_ID)
    series_name = series_details["name"]

    print(f"Series: {series_name}")
    print(f"Series ID: {SERIES_ID}\n")

    total_downloaded = 0
    total_skipped = 0

    # Get all episodes (paginated)
    page = 0
    episodes_by_season = {}

    print("Fetching all episodes...")
    while True:
        try:
            episodes_data = get_series_episodes(token, SERIES_ID, page=page)
            episodes = episodes_data.get("data", {}).get("episodes", [])

            if not episodes:
                break

            # Group episodes by season
            for episode in episodes:
                season_num = episode.get("seasonNumber")
                if season_num is not None:
                    if season_num not in episodes_by_season:
                        episodes_by_season[season_num] = []
                    episodes_by_season[season_num].append(episode)

            # Check if there are more pages
            links = episodes_data.get("links", {})
            if not links.get("next"):
                break

            page += 1

        except Exception as e:
            print(f"  Error fetching page {page}: {e}")
            break

    print(f"Found {len(episodes_by_season)} seasons\n")

    # Process each season
    for season_num in sorted(episodes_by_season.keys()):
        if season_num == 0:
            print(f"Processing Specials...")
            season_dir = os.path.join(OUTPUT_DIR, "Season 00")
        else:
            print(f"Processing Season {season_num}...")
            season_dir = os.path.join(OUTPUT_DIR, f"Season {season_num:02d}")

        Path(season_dir).mkdir(parents=True, exist_ok=True)

        episodes = episodes_by_season[season_num]

        # Download each episode thumbnail
        for episode in episodes:
            episode_num = episode.get("number", 0)
            episode_name = episode.get("name", "Unknown")
            image_path = episode.get("image")

            if image_path:
                # Get file extension from the image_path
                ext = os.path.splitext(image_path)[1] or ".jpg"
                # Clean episode name - remove invalid filename characters and replace colons
                clean_name = "".join(
                    c for c in episode_name if c.isalnum() or c in (" ", "_", "-", ":")
                ).rstrip()
                # Replace colons with hyphens
                clean_name = clean_name.replace(":", "-")
                filename = (
                    f"s{season_num:02d}e{episode_num:02d} {clean_name}-thumb{ext}"
                )
                save_path = os.path.join(season_dir, filename)

                # Create display name with colons replaced for logging
                display_name = episode_name.replace(":", "-")

                try:
                    download_image(image_path, save_path)
                    print(
                        f"  ✓ Downloaded: s{season_num:02d}e{episode_num:02d} {display_name}"
                    )
                    total_downloaded += 1
                except Exception as e:
                    print(
                        f"  ✗ Failed to download s{season_num:02d}e{episode_num:02d}: {e}"
                    )
            else:
                # Replace colons in episode name for logging
                display_name = episode_name.replace(":", "-")
                print(
                    f"  - No thumbnail for s{season_num:02d}e{episode_num:02d} - {display_name}"
                )
                total_skipped += 1

    print(f"\n{'=' * 50}")
    print(f"Download complete!")
    print(f"Total downloaded: {total_downloaded}")
    print(f"Total skipped (no thumbnail): {total_skipped}")
    print(f"Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
