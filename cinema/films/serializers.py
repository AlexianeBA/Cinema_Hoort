from rest_framework import serializers
from .models import Users, Movie, Rating, Favorite

class UserSerializer(serializers.ModelSerializer):
    favorite_movies = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'role', 'bio', 'avatar', 'source', 'favorite_movies', 'password']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def get_favorite_movies(self, obj):
        favorites = Favorite.objects.filter(spectator=obj)
        return MovieSerializer([fav.movie for fav in favorites], many=True).data


class MovieSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'overview', 'release_date', 'rating', 'status', 'author', 'source', 'genres', 'original_title', 'original_language']
        read_only_fields = ['id', 'author']


class RatingSerializer(serializers.ModelSerializer):
    spectator = UserSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'spectator', 'movie', 'author', 'rating']
        read_only_fields = ['id', 'spectator', 'movie', 'author']


class FavoriteSerializer(serializers.ModelSerializer):
    spectator = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'spectator', 'movie']
        read_only_fields = ['id', 'spectator', 'movie']
        unique_together = ('spectator', 'movie')

