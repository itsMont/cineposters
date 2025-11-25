from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'director', 'genre', 'added_by', 'added_date']
    list_filter = ['genre', 'year', 'added_date']
    search_fields = ['title', 'director']
    date_hierarchy = 'added_date'
