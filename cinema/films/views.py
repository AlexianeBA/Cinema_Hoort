from urllib import request
from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Users, Movie, Rating, Favorite
from .serializers import UserSerializer, MovieSerializer, RatingSerializer, FavoriteSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission

# Create your views here.

class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'author'
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=False, methods=['get'], url_path='by-status')
    def get_movies_by_status(self, request):
        status_param = request.query_params.get('status')
        movies = self.queryset.filter(status=status_param) if status_param else self.queryset
        serializer = self.get_serializer(movies, many=True)
        return Response({
            "count": len(serializer.data),
            "results": serializer.data
        })
    
    def retrieve(self, request, pk=None):
        try:
            movie = self.get_object()
            serializer = self.get_serializer(movie)
            return Response({"movie": serializer.data})
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def update(self, request, pk=None):
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Movie updated", "movie": serializer.data})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @action(
        detail=True,
        methods=['patch'],
        url_path='archive',
        permission_classes=[IsAuthenticated, IsAuthor]
    )
    def archive_movie(self, request, pk=None):
        movie = self.get_object()
        movie.state = 'archived'
        movie.save()
        return Response({
            "message": f"Movie '{movie.title}' archived successfully",
            "movie_id": movie.id,
            "new_state": movie.state
        }, status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.filter(role='author')
    serializer_class = UserSerializer


    def retrieve(self, request, pk=None):
        author = self.get_object()
        serializer = self.get_serializer(author)
        return Response({"author": serializer.data})

    def update(self, request, pk=None):
        author = self.get_object()
        serializer = self.get_serializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Author updated", "author": serializer.data})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        author = self.get_object()
        if Movie.objects.filter(author=author).exists():
            return Response(
                {"error": "Impossible de supprimer cet auteur : des films lui sont associés."},
                status=status.HTTP_400_BAD_REQUEST
            )
        author.delete()
        return Response({"message": "Author deleted"}, status=status.HTTP_204_NO_CONTENT)

class SpectatorViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.filter(role='spectator')
    serializer_class = UserSerializer
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(role='spectator')
            return Response({"message": "Spectator registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def refresh_token(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('username')
            return Response({"message": "Token refreshed successfully", "user": user}, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    @action(detail=True, methods=['post'], url_path='add', permission_classes=[IsAuthenticated])
    def add_movie_to_favorites(self, request, pk=None):
        movie = Movie.objects.get(pk=pk)
        favorite, created = Favorite.objects.get_or_create(spectator=request.user, movie=movie)
        if created:
            return Response({"message": "Movie added to favorites"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Movie is already in favorites"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], url_path='remove', permission_classes=[IsAuthenticated])
    def remove_from_favorites(self, request, pk=None):
        movie = self.get_object()
        favorite = Favorite.objects.filter(spectator=request.user, movie=movie).first()
        if favorite:
            favorite.delete()
            return Response({"message": "Movie removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Movie is not in favorites"}, status=status.HTTP_404_NOT_FOUND)

    def get_favorite_movies(self, request):
        favorites = Favorite.objects.filter(spectator=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response({"favorites": serializer.data}, status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def add_rating_to_movie():
        pass
    def add_rating_to_author():
        pass

