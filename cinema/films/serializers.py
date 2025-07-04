from rest_framework import serializers

from .models import AuthorRating, Favorite, Movie, Rating, Users


class FavoriteMovieSerializer(serializers.ModelSerializer):
    """Serializer for favorite movies of a spectator."""

    movie = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ["movie"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details, including favorite movies."""

    favorite_movies = FavoriteMovieSerializer(
        source="spectator_favorite", many=True, read_only=True
    )

    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "email",
            "role",
            "bio",
            "avatar",
            "source",
            "favorite_movies",
            "password",
            "date_of_birth",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movie details, including authors and genres."""

    authors = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "overview",
            "release_date",
            "rating",
            "status",
            "authors",
            "source",
            "genres",
            "original_title",
            "original_language",
        ]
        read_only_fields = ["id", "authors"]


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model, including spectator and movie details.
    """

    spectator = UserSerializer(read_only=True)

    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "spectator", "movie", "rating"]
        read_only_fields = ["id", "spectator", "movie"]


class RatingAuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the AuthorRating model, including spectator and author details.
    """

    spectator = UserSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = AuthorRating
        fields = ["id", "spectator", "author", "rating", "comment"]
        read_only_fields = ["id", "spectator", "author"]
        unique_together = ("spectator", "author")


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Favorite model, including spectator and movie details.
    """

    spectator = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "spectator", "movie"]
        read_only_fields = ["id", "spectator", "movie"]
        unique_together = ("spectator", "movie")
