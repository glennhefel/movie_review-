import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from media.models import Media

class Command(BaseCommand):
    help = "Fetches top anime from Jikan API and adds them to Media model."

    def handle(self, *args, **kwargs):
        url = "https://api.jikan.moe/v4/top/anime"
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Failed to fetch data from API."))
            return

        data = response.json().get("data", [])

        for anime in data:
            title = anime.get("title")
            date_str = anime.get("aired", {}).get("from")
            release_date = datetime.strptime(date_str[:10], "%Y-%m-%d").date() if date_str else datetime.today().date()
            description = anime.get("synopsis", "No description available.")
            poster = anime.get("images", {}).get("jpg", {}).get("image_url", "")
            genre = "action"  # Replace with smarter logic if needed

            if not Media.objects.filter(title=title).exists():
                Media.objects.create(
                    title=title,
                    release_date=release_date,
                    media="Anime",
                    genre=genre,
                    director="Unknown",
                    description=description,
                    poster=poster
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Added: {title}"))
            else:
                self.stdout.write(f"Skipped (already exists): {title}")