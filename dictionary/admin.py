from django.contrib import admin

from .models import Category, Source, Term, UserSuggestion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year")
    search_fields = ("title", "author")


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("term", "category", "source", "updated_at")
    list_filter = ("category",)
    search_fields = ("term", "short_definition", "full_definition", "synonyms")
    prepopulated_fields = {"slug": ("term",)}


@admin.register(UserSuggestion)
class UserSuggestionAdmin(admin.ModelAdmin):
    list_display = ("candidate_term", "contact_email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("candidate_term", "candidate_definition", "contact_email")
