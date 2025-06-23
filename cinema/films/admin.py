from django.contrib import admin
from django.contrib.admin import SimpleListFilter

# Register your models here.
from .models import Author, Favorite, Movie, Rating, Spectator, Users


class HasMoviesFilter(SimpleListFilter):
    """
    Admin filter to show authors with or without at least one movie.
    """

    title = "has at least one movie"
    parameter_name = "has_movies"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(movies__isnull=False).distinct()
        if self.value() == "no":
            return queryset.filter(movies__isnull=True)
        return queryset


class MovieAuthorsInline(admin.TabularInline):
    """
    Inline for displaying authors of a movie.
    """

    model = Movie.authors.through
    extra = 0
    verbose_name = "Film"
    verbose_name_plural = "Films"
    fields = ["movie"]
    show_change_link = True


class MovieRatingInline(admin.TabularInline):
    """
    Inline for displaying ratings related to a movie.
    """

    model = Rating
    fk_name = "movie"
    extra = 0
    fields = ["spectator", "rating"]
    show_change_link = True

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "spectator":
            kwargs["queryset"] = Users.objects.filter(role="spectator")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AuthorInline(admin.TabularInline):
    """
    Inline for displaying authors in movie admin.
    """

    model = Movie.authors.through
    extra = 0
    verbose_name = "Author"
    verbose_name_plural = "Authors"
    fields = ["users"]


class FavoriteInline(admin.TabularInline):
    """
    Inline for displaying favorite movies of a spectator.
    """

    model = Favorite
    fk_name = "spectator"
    extra = 0
    fields = ["movie"]
    show_change_link = True

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Limit spectator choices to users with role 'spectator'.
        """
        if db_field.name == "spectator":
            kwargs["queryset"] = Users.objects.filter(role="spectator")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Author proxy model.
    Shows only users with role 'author'.
    """

    list_display = ["username", "email", "is_staff", "date_of_birth"]
    list_filter = [HasMoviesFilter]
    inlines = [MovieAuthorsInline]

    search_fields = ["username", "email"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role="author")


@admin.register(Spectator)
class SpectatorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Spectator proxy model.
    Shows only users with role 'spectator'.
    """

    list_display = ["username", "email", "is_staff"]
    inlines = [FavoriteInline]
    search_fields = ["username", "email"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role="spectator")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Admin configuration for Movie model.
    """

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
        """
        Returns a comma-separated list of author usernames for a movie.
        """
        return ", ".join([a.username for a in obj.authors.all()])

    get_authors.short_description = "Authors movie"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Rating model.
    """

    list_display = ["spectator", "movie", "rating"]
    list_filter = ["rating"]
    search_fields = ["spectator__username", "movie__title"]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Admin configuration for Favorite model.
    """

    list_display = ["spectator", "movie"]
    search_fields = ["spectator__username", "movie__title"]
