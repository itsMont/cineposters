from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
    
    title = models.CharField(max_length=200, verbose_name="Título")
    year = models.IntegerField(verbose_name="Año de estreno")
    director = models.CharField(max_length=100, verbose_name="Director")
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, verbose_name="Género")
    poster_url = models.URLField(max_length=500, blank=True, verbose_name="URL del Poster")
    imdb_id = models.CharField(max_length=20, blank=True, verbose_name="ID de IMDB")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Agregado por")
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de agregado")
    
    class Meta:
        ordering = ['-added_date']
        verbose_name = "Película"
        verbose_name_plural = "Películas"
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'movie_id': self.id})