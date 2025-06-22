from django.core.management.base import BaseCommand

from config.utils import get_tmdb_data
from films.models import Movie, Users


class Command(BaseCommand):
    help = "Import movies from TMDB"

    def handle(self, *args, **kwargs):
        try:
            # Clear existing movies
            Movie.objects.all().delete()
            # Get popular movies from TMDB
            data = get_tmdb_data("movie/popular", params={"page": 1})
            movies = data.get("results", [])

            for movie in movies:
                # Get movie details from TMDB
                movie_id = movie.get("id")
                movie_details = get_tmdb_data(f"movie/{movie_id}")
                title = movie_details.get("title")
                release_date = movie_details.get("release_date")
                overview = movie_details.get("overview")
                vote_average = movie_details.get("vote_average", 0)
                tmdb_status = get_tmdb_data(f"movie/{movie_id}").get("status")
                status_map = {
                    "Released": "released",
                    "Post Production": "post_production",
                    "Planned": "planned",
                }
                status = status_map.get(tmdb_status, "released")
                genres = get_tmdb_data(f"movie/{movie_id}").get("genres", [])
                genre_names = [g["name"] for g in genres]
                original_title = get_tmdb_data(f"movie/{movie_id}").get(
                    "original_title", title
                )
                original_language = get_tmdb_data(f"movie/{movie_id}").get(
                    "original_language"
                )

                # Get director information
                credits = get_tmdb_data(f"movie/{movie_id}/credits")
                crew = credits.get("crew", [])
                directors = [
                    person["name"] for person in crew if person["job"] == "Director"
                ]

                # Create or get the user and movie objects
                if directors:
                    director_name = directors[0]
                    username = director_name.lower().replace(" ", "_")
                    user, created_user = Users.objects.get_or_create(
                        username=username,
                        defaults={
                            "role": "author",
                            "source": "tmdb",
                            "bio": "",
                            "avatar": None,
                            "email": f"{username}@tmdb.local",
                        },
                    )
                    # Create or get the movie object
                    movie_obj, created_movie = Movie.objects.get_or_create(
                        title=title,
                        status=status,
                        release_date=release_date,
                        author=user,
                        original_title=original_title,
                        original_language=original_language,
                        overview=overview,
                        rating=vote_average,
                        genres=", ".join(genre_names),
                        defaults={
                            "source": "tmdb",
                        },
                    )
                    # Log creation messages
                    if created_user:
                        self.stdout.write(
                            self.style.SUCCESS(f"Created author: {director_name}")
                        )
                    if created_movie:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Created movie: {title} (Director: {director_name})"
                            )
                        )

                print(
                    f"Title: {title}, Release Date: {release_date}, Overview: {overview}, Vote Average: {vote_average}, Directors: {', '.join(directors)}, User: {user.username}, Movie source: {movie_obj.source}, Status: {movie_obj.status}, genres: {', '.join(genre_names)}"
                )

        except Exception as e:
            self.stderr.write(f"Error importing movies: {e}")
