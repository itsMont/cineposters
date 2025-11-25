from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Acción'),
        ('adventure', 'Aventura'),
        ('comedy', 'Comedia'),
        ('drama', 'Drama'),
        ('fantasy', 'Fantasía'),
        ('horror', 'Terror'),
        ('sci-fi', 'Ciencia Ficción'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('animation', 'Animación'),
        ('documentary', 'Documental'),
        ('other', 'Otro'),
    ]
    
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    poster_url = models.URLField(max_length=500, blank=True)
    imdb_id = models.CharField(max_length=20, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_date']
    
    def __str__(self):
        return f"{self.title} ({self.year})"
