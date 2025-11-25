from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from posters import views as poster_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', poster_views.movie_list, name='movie_list'),
    path('add/', poster_views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/', poster_views.movie_detail, name='movie_detail'),
    # UPDATE - 🆕 ESTA ES LA QUE FALTA
    path('movie/<int:movie_id>/edit/', poster_views.edit_movie, name='edit_movie'),
    
    # DELETE - 🆕 Y ESTA TAMBIÉN
    path('movie/<int:movie_id>/delete/', poster_views.delete_movie, name='delete_movie'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', TemplateView.as_view(template_name='registration/register.html'), name='register'),
]
