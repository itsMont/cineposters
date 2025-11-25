# posters/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Movie
from .forms import MovieForm

class MovieModelTest(TestCase):
    """Pruebas unitarias para el modelo Movie"""
    
    def setUp(self):
        """Configuración inicial para todas las pruebas"""
        self.user = User.objects.create_user(
            username='jmontanaa',
            password='aus12345'
        )
        
        self.movie_data = {
            'title': 'The Matrix',
            'year': 1999,
            'director': 'Lana Wachowski, Lilly Wachowski',
            'genre': 'sci-fi',
            'poster_url': 'https://example.com/matrix.jpg',
            'imdb_id': 'tt0133093'
        }
    
    def test_create_movie(self):
        """Prueba la creación básica de una película"""
        movie = Movie.objects.create(
            added_by=self.user,
            **self.movie_data
        )
        
        self.assertEqual(movie.title, 'The Matrix')
        self.assertEqual(movie.year, 1999)
        self.assertEqual(movie.director, 'Lana Wachowski, Lilly Wachowski')
        self.assertEqual(movie.genre, 'sci-fi')
        self.assertEqual(movie.poster_url, 'https://example.com/matrix.jpg')
        self.assertEqual(movie.imdb_id, 'tt0133093')
        self.assertEqual(movie.added_by, self.user)
        self.assertIsNotNone(movie.added_date)
    
    
    def test_movie_genre_choices(self):
        """Prueba los choices del campo género"""
        movie = Movie.objects.create(
            added_by=self.user,
            **self.movie_data
        )
        
        # Verificar que el género sea válido
        valid_genres = [choice[0] for choice in Movie.GENRE_CHOICES]
        self.assertIn(movie.genre, valid_genres)


    def test_movie_max_length_constraints(self):
        """Prueba las restricciones de longitud máxima"""
        # Título muy largo
        long_title = "M" * 201  # Excede el máximo de 200
        movie = Movie(
            title=long_title,
            year=2020
        )
        
        # Verificar que se respeta el max_length
        with self.assertRaises(Exception):
            movie.full_clean()  # Esto debería fallar por validación
    
    def test_movie_year_validation(self):
        """Prueba la validación del año"""
        # Año muy antiguo
        movie = Movie(
            title="Probar Movie Antigua",
            year=1800,  # Muy antiguo
            director="Director",
            genre="action", 
            added_by=self.user
        )
        
        # Año muy futuro
        movie_future = Movie(
            title="Probar Movie Futuro",
            year=2050,  # Año muy futuro
            director="Director",
            genre="action",
            added_by=self.user
        )

# Prueba unitaria formulario Movie FOrm
class MovieFormTest(TestCase):
    """Pruebas para el formulario MovieForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='formuser',
            password='testpass123'
        )
    
    def test_valid_form(self):
        """Prueba formulario válido"""
        form_data = {
            'title': 'Interstellar',
            'year': 2014
        }
        
        form = MovieForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_year_too_old(self):
        """Prueba año inválido (demasiado antiguo)"""
        form_data = {
            'title': 'Movie Vieja',
            'year': 1800 # Demasiado antiguo
        }
        
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('year', form.errors)
    
    def test_invalid_year_too_future(self):
        """Prueba año inválido (demasiado futuro)"""
        form_data = {
            'title': 'Movie Futurra',
            'year': 2050  # Demasiado futuro
        }
        
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('year', form.errors)
    
    def test_invalid_title_too_short(self):
        """Prueba título inválido (demasiado corto)"""
        form_data = {
            'title': 'A',  # Demasiado corto
            'year': 2020
        }
        
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_missing_required_fields(self):
        """Prueba campos requeridos faltantes"""
        form_data = {
            'title': '',  # Campo requerido faltante
            'year': 2020
        }
        
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
