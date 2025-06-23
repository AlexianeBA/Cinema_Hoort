from django.contrib import admin

# Register your models here.
from .models import AuthorRating, Favorite, Movie, Rating, Users


class MovieInline(admin.TabularInline):
    model = Movie
    extra = 0
    fields = ["title", "release_date", "status", "rating", "state"]
    show_change_link = True
class MovieAuthorsInline(admin.TabularInline):
    model = Movie.authors.through
    extra = 0
    verbose_name = "Film"
    verbose_name_plural = "Films"
    fields = ["movie"]
    show_change_link = True

class MovieRatingInline(admin.TabularInline):
    model = Rating
    fk_name = "movie"
    extra = 0
    fields = ["spectator", "rating"]
    show_change_link = True
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "spectator":
            kwargs["queryset"] = Users.objects.filter(role="spectator")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class AuthorRatingInline(admin.TabularInline):
    model = AuthorRating
    fk_name = "author"
    extra = 0
    fields = ["spectator", "rating", "comment"]
    show_change_link = True

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "spectator":
            kwargs["queryset"] = Users.objects.filter(role="spectator")
        if db_field.name == "author":
            kwargs["queryset"] = Users.objects.filter(role="author")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class AuthorInline(admin.TabularInline):
    model = Movie.authors.through
    extra = 0
    verbose_name = "Author"
    verbose_name_plural = "Authors"
    fields = ["users"]

class FavoriteInline(admin.TabularInline):
    model = Favorite
    fk_name = "spectator"
    extra = 0
    fields = ["movie"]
    show_change_link = True
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "spectator":
            kwargs["queryset"] = Users.objects.filter(role="spectator")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "role", "is_staff"]
    list_filter = ["role", "is_staff"]

    inlines = []

    def get_inlines(self, request, obj):
        """Retourne dynamiquement les inlines selon le rôle"""
        if obj and obj.role == "author":
            return [MovieAuthorsInline]
        elif obj and obj.role == "spectator":
            return [AuthorRatingInline, FavoriteInline, MovieRatingInline]
        return []

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.inlines = self.get_inlines(request, self.model.objects.get(pk=object_id))
        return super().change_view(request, object_id, form_url, extra_context)
    def get_inlines(self, request, obj):
        if obj and obj.role == "author":
            return [MovieAuthorsInline]
        elif obj and obj.role == "spectator":
            return [AuthorRatingInline, FavoriteInline]
        return []


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "get_authors",
        "release_date",
        "status",
        "rating",
        "genres",
        "original_title",
        "original_language",
    ]
    list_filter = ["status", "release_date", "rating"]
    search_fields = ["title", "overview"]
    inlines = [MovieRatingInline, AuthorInline]

    def get_authors(self, obj):
        return ", ".join([a.username for a in obj.authors.all()])
    get_authors.short_description = "Authors movie"




@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["spectator", "movie", "rating"]
    list_filter = ["rating"]
    search_fields = ["spectator__username", "movie__title"]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["spectator", "movie"]
    search_fields = ["spectator__username", "movie__title"]
