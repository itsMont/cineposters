import requests
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Movie
from .forms import MovieForm
from dotenv import dotenv_values

def movie_list(request):
    movies = Movie.objects.all()
    
    genre = request.GET.get('genre')
    if genre:
        movies = movies.filter(genre=genre)
    
    search = request.GET.get('search')
    if search:
        movies = movies.filter(title__icontains=search)
    
    return render(request, 'posters/list.html', {
        'movies': movies,
        'genres': Movie.GENRE_CHOICES
    })

config = dotenv_values(".env")
# Obtener API key de OMDB
OMDB_API_KEY = config["OMDB_API_KEY"]
@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            
            try:
                api_key = "tu-api-key-aqui"
                response = requests.get(
                    f"http://www.omdbapi.com/?t={movie.title}&y={movie.year}&apikey={api_key}"
                )
                data = response.json()
                
                if data.get('Response') == 'True':
                    movie.poster_url = data.get('Poster', '')
                    movie.imdb_id = data.get('imdbID', '')
            except Exception as e:
                print(f"Error al conectar con OMDB: {e}")
            
            movie.save()
            messages.success(request, 'Película agregada exitosamente!')
            return redirect('movie_list')
    else:
        form = MovieForm()
    
    return render(request, 'posters/add.html', {'form': form})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'posters/detail.html', {'movie': movie})
