from django.urls import path
from . import views

app_name = 'posters'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('add/', views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
]
