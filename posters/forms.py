from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'year', 'director', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la película'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Año de estreno',
                'min': 1888,
                'max': 2030
            }),
            'director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Director'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year < 1888 or year > 2030:
            raise forms.ValidationError("Por favor ingresa un año válido (1888-2030)")
        return year
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise forms.ValidationError("El título debe tener al menos 2 caracteres")
        return title
