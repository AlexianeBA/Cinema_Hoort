from django.core.management.base import BaseCommand

from config.utils import get_tmdb_data
from films.models import Movie, Users


class Command(BaseCommand):
    help = "Import movies from TMDB"

    def handle(self, *args, **kwargs):
        """
        Imports popular movies from TMDb, creates or updates authors (directors) and movies in the database.
        For each movie:
            - Fetches details and genres from TMDb.
            - Fetches director info and date of birth.
            - Creates or updates the author (director) in the database.
            - Creates or updates the movie and links it to the author.
        """
        try:
            # Clear existing movies
            Movie.objects.filter(source="tmdb").delete()
            # Get popular movies from TMDB
            data = get_tmdb_data("movie/popular", params={"page": 1})
            movies = data.get("results", [])

            for movie in movies:
                # Fetch movie details from TMDB
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

                # Fetch director information
                credits = get_tmdb_data(f"movie/{movie_id}/credits")
                crew = credits.get("crew", [])
                directors = [person for person in crew if person["job"] == "Director"]

                users = []
                if directors:
                    director = directors[0]
                    director_name = director["name"]
                    director_id = director["id"]
                    username = director_name.lower().replace(" ", "_")

                    # Fetch director details for date of birth
                    director_details = get_tmdb_data(f"person/{director_id}")
                    date_of_birth = director_details.get("birthday") or "1970-01-01"

                    # Create or update the author (director)
                    user, created_user = Users.objects.get_or_create(
                        username=username,
                        defaults={
                            "role": "author",
                            "source": "tmdb",
                            "bio": "",
                            "avatar": None,
                            "email": f"{username}@tmdb.local",
                            "date_of_birth": date_of_birth,
                        },
                    )
                    if not created_user and user.date_of_birth != date_of_birth:
                        user.date_of_birth = date_of_birth
                        user.save()
                    users.append(user)
                    if created_user:
                        self.stdout.write(
                            self.style.SUCCESS(f"Created author: {director_name}")
                        )
                    # Create or update the movie and link to author
                    movie_obj, created_movie = Movie.objects.get_or_create(
                        title=title,
                        status=status,
                        release_date=release_date,
                        original_title=original_title,
                        original_language=original_language,
                        overview=overview,
                        rating=vote_average,
                        genres=", ".join(genre_names),
                        defaults={
                            "source": "tmdb",
                        },
                    )
                    movie_obj.authors.add(*users)
                    # Log creation messages
                    if created_movie:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Created movie: {title} (Director: {', '.join([d['name'] for d in directors])})"
                            )
                        )

                print(
                    f"Title: {title}, Release Date: {release_date}, Overview: {overview}, Vote Average: {vote_average}, Directors: {', '.join([d['name'] for d in directors])}, User: {user.username}, Movie source: {movie_obj.source}, Status: {movie_obj.status}, genres: {', '.join(genre_names)}, date_of_birth: {date_of_birth}"
                )

        except Exception as e:
            self.stderr.write(f"Error importing movies: {e}")
