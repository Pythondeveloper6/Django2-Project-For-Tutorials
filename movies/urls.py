from django.urls import path 
from . import views

app_name = 'movies'

urlpatterns = [
    path('' ,views.movies_list , name='movies_list'),
    path('<int:id>' ,views.movies_detail , name='movies_detail'),

]
