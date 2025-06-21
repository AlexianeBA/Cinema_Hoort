from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class Users(AbstractUser):
    ROLE_CHOICES = [
        ('spectator', 'Spectator'),
        ('author', 'Author'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
  
    def is_author(self):
        return self.role == 'author'
    def is_spectator(self):
        return self.role == 'spectator'
    

class Movie(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('released', 'Released'),
        ('archived', 'Archived'),
    ]
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    status = models.CharField(choices=STATUS_CHOICES)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='movies', limit_choices_to={'role': 'author'})

    def __str__(self):
        return self.title
    

class Rating(models.Model):
    spectator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='spectator_ratings', limit_choices_to={'role': 'spectator'})
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='author_ratings', limit_choices_to={'role': 'author'})
    rating = models.IntegerField(choices=Movie.RATING_CHOICES)

class Favorite(models.Model):
    spectator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='spectator_favorite', limit_choices_to={'role': 'spectator'})
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorite')

    class Meta:
        unique_together = ('spectator', 'movie')

    def __str__(self):
        return f"{self.spectator.username} - {self.movie.title}"