from django.contrib import admin

# Register your models here.
from .models import Users, Movie, Rating, Favorite



class MovieInline(admin.TabularInline):
    model = Movie
    extra = 0
    fields = ['title', 'release_date', 'status', 'rating']
    show_change_link = True

class RatingInline(admin.TabularInline):
    model = Rating
    fk_name = 'spectator'
    extra = 0
    fields = ['movie', 'rating']
    show_change_link = True

class FavoriteInline(admin.TabularInline):
    model = Favorite
    fk_name = 'spectator'
    extra = 0
    fields = ['movie']
    show_change_link = True


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff']
    
    inlines = []

    def get_inlines(self, request, obj):
        """Retourne dynamiquement les inlines selon le rôle"""
        if obj and obj.role == 'author':
            return [MovieInline]
        elif obj and obj.role == 'spectator':
            return [RatingInline, FavoriteInline]
        return []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = self.get_inlines(request, self.model.objects.get(pk=object_id))
        return super().change_view(request, object_id, form_url, extra_context)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'release_date', 'status', 'rating', 'genres', 'original_title', 'original_language']
    list_filter = ['status', 'release_date', 'author']
    search_fields = ['title', 'description']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['spectator', 'movie', 'rating']
    list_filter = ['rating']
    search_fields = ['spectator__username', 'movie__title']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['spectator', 'movie']
    search_fields = ['spectator__username', 'movie__title']
