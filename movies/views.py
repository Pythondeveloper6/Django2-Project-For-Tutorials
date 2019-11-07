from django.shortcuts import render
from .models import Movie


def movies_list(request):
    movie_list = Movie.objects.all()
    template_name = 'movies/movie_list.html'
    context = {'movie_list' : movie_list }
    return render(request , template_name , context)



def movies_detail(request , id):
    movie_detail = Movie.objects.get(id=id)
    template_name = 'movies/movie_detail.html'
    context = {'movie_detail' : movie_detail }
    return render(request , template_name , context)