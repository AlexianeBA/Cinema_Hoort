"""
URL configuration for the Django project.

This module defines the URL patterns for the project, including:
- Admin interface
- JWT authentication endpoints (token obtain and refresh)
- API endpoints for movies, authors, favorites, spectators, ratings, and users via DRF viewsets
- API authentication via browsable API login/logout
- Logout endpoint

Routers from Django REST Framework are used to automatically generate routes for the registered viewsets.

Imports:
    - Django admin and URL utilities
    - DRF router and JWT views
    - Application viewsets for films app

Example:
    Access the movies API at /api/movies/
    Obtain JWT token at /api/token/


URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from films.views import (AuthorViewSet, FavoriteViewSet, LogoutView,
                         MovieViewSet, RatingViewSet, SpectatorViewSet,
                         UserViewSet)

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"spectators", SpectatorViewSet, basename="spectator")
router.register(r"rating", RatingViewSet, basename="rating")
router.register(r"users", UserViewSet, basename="user")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/logout/", LogoutView.as_view(), name="logout"),
]
