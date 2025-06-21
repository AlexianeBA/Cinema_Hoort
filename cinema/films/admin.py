from django.contrib import admin
from .models import Users, Movie, Rating, Favorite
# Register your models here.
admin.site.register(Users)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Favorite)