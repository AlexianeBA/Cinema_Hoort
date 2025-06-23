from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Users(AbstractUser):
    """
    Custom user model with roles (author, spectator), bio, avatar, source, and date of birth.
    """
    ROLE_CHOICES = [
        ("spectator", "Spectator"),
        ("author", "Author"),
    ]
    SOURCE_CHOICES = [
        ("manual", "Manual"),
        ("tmdb", "TMDb"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, default="tmdb")
    date_of_birth = models.DateField(null=True, blank=True)

    def is_author(self):
        """Return True if the user is an author."""
        return self.role == "author"

    def is_spectator(self):
        """Return True if the user is a spectator."""
        return self.role == "spectator"


class Movie(models.Model):
    """
    Model representing a movie, with title, overview, release date, rating, status, authors, and other metadata.
    """
    STATUS_CHOICES = [
        ("released", "Released"),
        ("post_production", "Post Production"),
        ("planned", "Planned"),
    ]
    RATING_CHOICES = [
        [(i, str(i)) for i in range(1, 11)]
    ]
    SOURCE_CHOICES = [
        ("manual", "Manual"),
        ("tmdb", "TMDb"),
    ]

    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    status = models.CharField(choices=STATUS_CHOICES)
    authors = models.ManyToManyField(
        Users,
        related_name="movies",
        limit_choices_to={"role": "author"},
        blank=True,
    )
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, default="tmdb")
    genres = models.CharField(max_length=100, null=True, blank=True)
    original_title = models.CharField(max_length=100, null=True, blank=True)
    original_language = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=20, default="active")

    class Meta:
        unique_together = ("title", "status", "release_date")

    def __str__(self):
        return self.title


class Rating(models.Model):
    """
    Model representing a rating given by a spectator to a movie.
    """
    spectator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="spectator_ratings",
        limit_choices_to={"role": "spectator"},
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="ratings", null=True, blank=True
    )

    rating = models.IntegerField(choices=Movie.RATING_CHOICES)

    def __str__(self):
        return f"{self.spectator.username} rated {self.movie.title}: {self.rating}"


class AuthorRating(models.Model):
    """
    Model representing a rating and comment given by a spectator to an author.
    """
    spectator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="author_ratings_given",
        limit_choices_to={"role": "spectator"},
    )
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="author_ratings_received",
        limit_choices_to={"role": "author"},
    )
    rating = models.IntegerField(choices=Movie.RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("spectator", "author")

    def __str__(self):
        return f"{self.spectator.username} → {self.author.username}: {self.rating}"


class Favorite(models.Model):
    """
    Model representing a favorite movie for a spectator.
    """
    spectator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="spectator_favorite",
        limit_choices_to={"role": "spectator"},
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorite")

    class Meta:
        unique_together = ("spectator", "movie")

    def __str__(self):
        return f"{self.spectator.username} - {self.movie.title}"


class Author(Users):
    """
    Proxy model for authors (users with role 'author').
    """
    class Meta:
        proxy = True
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Spectator(Users):
    """
    Proxy model for spectators (users with role 'spectator').
    """
    class Meta:
        proxy = True
        verbose_name = "Spectator"
        verbose_name_plural = "Spectators"
