import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Movie
from .forms import MovieForm
from dotenv import dotenv_values
# registro
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

config = dotenv_values(".env")
OMDB_API = config["OMDB_API_KEY"]

# READ - Listar todas las películas
def movie_list(request):
    movies = Movie.objects.all()
    
    # Filtros
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

# READ - Detalle de una película (VERSIÓN ACTUALIZADA)
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Obtener películas relacionadas (mismo género, excluyendo la actual)
    related_movies = Movie.objects.filter(
        genre=movie.genre
    ).exclude(
        id=movie.id
    )[:6]  # Máximo 6 películas
    
    return render(request, 'posters/detail.html', {
        'movie': movie,
        'related_movies': related_movies
    })

# CREATE - Agregar nueva película
@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            
            # Buscar en OMDB API
            try:
                api_key = OMDB_API
                response = requests.get(
                    f"http://www.omdbapi.com/?apikey={api_key}&t={movie.title}&y={movie.year}"
                )
                data = response.json()
                
                if data.get('Response') == 'True':
                    movie.title = data.get('Title', '')
                    movie.poster_url = data.get('Poster', '')
                    movie.imdb_id = data.get('imdbID', '')
                    movie.director = data.get('Director', '')
                    # En caso de tener género, agrega el primero
                    movie.genre = data.get('Genre').split(",")[0]
                # En caso de error y no encontrar pelicula
                elif data.get('Response') == 'False':
                    messages.error(request, "Película no encontrada :(")
                    return redirect('add_movie')
            except Exception as e:
                print(f"Error al conectar con OMDB: {e}")
            
            movie.save()
            messages.success(request, 'Película agregada exitosamente!')
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm()
    
    return render(request, 'posters/movie_form.html', {
        'form': form,
        'title': 'Agregar Película',
        'submit_text': 'Agregar Película'
    })

# UPDATE - Editar película existente
@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Verificar permisos: solo el creador o superusuario puede editar
    if movie.added_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permisos para editar esta película")
    
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            updated_movie = form.save(commit=False)
            
            # Buscar poster actualizado en OMDB API
            try:
                api_key = OMDB_API
                response = requests.get(
                    f"http://www.omdbapi.com/?t={updated_movie.title}&y={updated_movie.year}&apikey={api_key}"
                )
                data = response.json()
                
                if data.get('Response') == 'True':
                    movie.title = data.get('Title', '')
                    movie.poster_url = data.get('Poster', '')
                    movie.imdb_id = data.get('imdbID', '')
                    movie.director = data.get('Director', '')
                    # En caso de tener género, agrega el primero
                    movie.genre = data.get('Genre').split(",")[0]
                elif data.get('Response') == 'False':
                    messages.error(request, "Película no encontrada :(")
            except Exception as e:
                print(f"Error al conectar con OMDB: {e}")
            
            updated_movie.save()
            messages.success(request, 'Película actualizada exitosamente!')
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    
    return render(request, 'posters/movie_form.html', {
        'form': form,
        'title': 'Editar Película',
        'submit_text': 'Actualizar Película',
        'movie': movie
    })

# DELETE - Eliminar película
@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Verificar permisos: solo el creador o superusuario puede eliminar
    if movie.added_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permisos para eliminar esta película")
    
    if request.method == 'POST':
        movie_title = movie.title
        movie.delete()
        messages.success(request, f'Película "{movie_title}" eliminada exitosamente!')
        return redirect('movie_list')
    
    return render(request, 'posters/delete_confirm.html', {'movie': movie})

# AGREGAR Registro Usuario

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Iniciar sesión automáticamente después del registro
            from django.contrib.auth import login
            login(request, user)
            
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenido a CinePosters.')
            return redirect('movie_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})