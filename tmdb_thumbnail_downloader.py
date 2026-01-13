import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - loaded from environment variables
API_KEY = os.getenv("TMDB_API_KEY")
TV_SHOW_ID = int(os.getenv("TMDB_TV_SHOW_ID", "1570"))
OUTPUT_DIR = os.getenv("TMDB_OUTPUT_DIR", "thumbnails")

if not API_KEY:
    raise ValueError(
        "TMDB_API_KEY not found in environment variables. Please create a .env file with your API key."
    )

# TMDB API base URLs
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/original"


def get_tv_show_details(show_id):
    """Get TV show details including number of seasons."""
    url = f"{BASE_URL}/tv/{show_id}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_season_episodes(show_id, season_number):
    """Get all episodes for a specific season."""
    url = f"{BASE_URL}/tv/{show_id}/season/{season_number}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def download_image(image_path, save_path):
    """Download an image from TMDB."""
    if not image_path:
        return False

    url = f"{IMAGE_BASE_URL}{image_path}"
    response = requests.get(url)
    response.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(response.content)
    return True


def main():
    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    print(f"Fetching TV show details...")
    show_details = get_tv_show_details(TV_SHOW_ID)
    show_name = show_details["name"]
    num_seasons = show_details["number_of_seasons"]

    print(f"Show: {show_name}")
    print(f"Total seasons: {num_seasons}\n")

    total_downloaded = 0
    total_skipped = 0

    # Iterate through all seasons
    for season_num in range(1, num_seasons + 1):
        print(f"Processing Season {season_num}...")

        try:
            season_data = get_season_episodes(TV_SHOW_ID, season_num)
            episodes = season_data["episodes"]

            # Create season directory
            season_dir = os.path.join(OUTPUT_DIR, f"Season_{season_num:02d}")
            Path(season_dir).mkdir(parents=True, exist_ok=True)

            # Download each episode thumbnail
            for episode in episodes:
                episode_num = episode["episode_number"]
                episode_name = episode["name"]
                still_path = episode["still_path"]

                if still_path:
                    filename = f"S{season_num:02d}E{episode_num:02d}_{episode_name}.jpg"
                    # Remove invalid filename characters
                    filename = "".join(
                        c for c in filename if c.isalnum() or c in (" ", "_", "-", ".")
                    ).rstrip()
                    save_path = os.path.join(season_dir, filename)

                    try:
                        download_image(still_path, save_path)
                        print(
                            f"  ✓ Downloaded: S{season_num:02d}E{episode_num:02d} - {episode_name}"
                        )
                        total_downloaded += 1
                    except Exception as e:
                        print(
                            f"  ✗ Failed to download S{season_num:02d}E{episode_num:02d}: {e}"
                        )
                else:
                    print(
                        f"  - No thumbnail for S{season_num:02d}E{episode_num:02d} - {episode_name}"
                    )
                    total_skipped += 1

        except Exception as e:
            print(f"  Error processing season {season_num}: {e}")

    print(f"\n{'=' * 50}")
    print(f"Download complete!")
    print(f"Total downloaded: {total_downloaded}")
    print(f"Total skipped (no thumbnail): {total_skipped}")
    print(f"Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
