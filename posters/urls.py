from django.urls import path
from . import views

app_name = 'posters'

urlpatterns = [
    
    # READ
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    
    # CREATE
    path('add/', views.add_movie, name='add_movie'),
    
    # UPDATE
    path('movie/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    
    # DELETE
    path('movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
]



